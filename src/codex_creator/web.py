from __future__ import annotations

import json
import mimetypes
import shutil
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .executor import Executor
from .planner import plan
from .schemas import SUPPORTED_TASKS, workspace_path


class CreatorWebApp:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or workspace_path()
        self.static_dir = self.root / "web"
        self.executor = Executor(self.root)
        self.job_tracker = WebJobTracker()

    def plan(self, prompt: str, task_type: str | None = None, input_images: list[str] | None = None) -> dict:
        job = plan(prompt, task_type_override=task_type)
        if input_images is not None:
            job.input_images = input_images
        _apply_job_overrides(job, {})
        return job.to_dict()

    def run(
        self,
        prompt: str,
        task_type: str | None = None,
        input_images: list[str] | None = None,
        resolution: str | None = None,
        outputs: int | None = None,
    ) -> dict:
        job = plan(prompt, task_type_override=task_type)
        if input_images is not None:
            job.input_images = input_images
        _apply_job_overrides(job, {"resolution": resolution, "outputs": outputs})
        result = self.executor.run(job)
        payload = result.to_dict()
        payload["output_urls"] = [self.public_output_url(path) for path in result.outputs]
        return {"job": job.to_dict(), "result": payload}

    def run_async(
        self,
        prompt: str,
        task_type: str | None = None,
        input_images: list[str] | None = None,
        resolution: str | None = None,
        outputs: int | None = None,
    ) -> dict:
        job = plan(prompt, task_type_override=task_type)
        if input_images is not None:
            job.input_images = input_images
        _apply_job_overrides(job, {"resolution": resolution, "outputs": outputs})
        self.job_tracker.register(job)
        worker = threading.Thread(target=self._run_job_async, args=(job,), daemon=True)
        worker.start()
        return self.job_tracker.snapshot(job.job_id)

    def list_jobs(self, limit: int = 20) -> list[dict]:
        job_dir = self.root / "jobs"
        items = sorted(job_dir.glob("*.job.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        jobs: list[dict] = []
        for path in items[:limit]:
            job = _read_json(path)
            result_path = self.root / "jobs" / f"{job['job_id']}.result.json"
            result = _read_json(result_path) if result_path.exists() else None
            if result:
                result["output_urls"] = [self.public_output_url(output) for output in result.get("outputs", [])]
            jobs.append(
                {
                    "job": job,
                    "result": result,
                    "preview_url": result["output_urls"][0] if result and result.get("output_urls") else None,
                }
            )
        return jobs

    def get_job(self, job_id: str) -> dict:
        job_path = self.root / "jobs" / f"{job_id}.job.json"
        result_path = self.root / "jobs" / f"{job_id}.result.json"
        if not job_path.exists():
            raise FileNotFoundError(job_id)
        result = _read_json(result_path) if result_path.exists() else None
        if result:
            result["output_urls"] = [self.public_output_url(path) for path in result.get("outputs", [])]
        payload = {
            "job": _read_json(job_path),
            "result": result,
        }
        tracked = self.job_tracker.get(job_id)
        if tracked:
            payload["progress"] = tracked["progress"]
            payload["state"] = tracked["state"]
        return payload

    def delete_job(self, job_id: str) -> dict:
        job_path = self.root / "jobs" / f"{job_id}.job.json"
        result_path = self.root / "jobs" / f"{job_id}.result.json"
        output_dir = self.root / "outputs" / job_id
        if not job_path.exists():
            raise FileNotFoundError(job_id)

        job_path.unlink(missing_ok=True)
        result_path.unlink(missing_ok=True)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        self.job_tracker.forget(job_id)
        return {"deleted": True, "job_id": job_id}

    def public_output_url(self, path_text: str) -> str:
        path = Path(path_text)
        if not path.is_absolute():
            path = (self.root / path).resolve()
        outputs_dir = (self.root / "outputs").resolve()
        if not str(path).startswith(str(outputs_dir)):
            raise ValueError(f"Output path is outside outputs directory: {path}")
        rel = path.relative_to(outputs_dir).as_posix()
        return f"/outputs/{rel}"

    def _run_job_async(self, job) -> None:
        try:
            result = self.executor.run(job, progress_callback=self.job_tracker.make_progress_callback(job.job_id))
            payload = result.to_dict()
            payload["output_urls"] = [self.public_output_url(path) for path in result.outputs]
            self.job_tracker.complete(job.job_id, payload)
        except Exception as exc:  # noqa: BLE001
            self.job_tracker.fail(job.job_id, str(exc))


class WebJobTracker:
    def __init__(self) -> None:
        self._items: dict[str, dict] = {}
        self._lock = threading.Lock()

    def register(self, job) -> None:
        with self._lock:
            self._items[job.job_id] = {
                "job": job.to_dict(),
                "state": "queued",
                "progress": {
                    "value": 0.0,
                    "percent": 0,
                    "stage": "queued",
                    "detail": "Queued",
                },
                "result": None,
            }

    def make_progress_callback(self, job_id: str):
        def callback(value: float, stage: str, detail: str | None = None) -> None:
            with self._lock:
                item = self._items.get(job_id)
                if not item:
                    return
                clamped = min(1.0, max(0.0, value))
                item["state"] = "running" if clamped < 1.0 else item["state"]
                item["progress"] = {
                    "value": clamped,
                    "percent": int(round(clamped * 100)),
                    "stage": stage,
                    "detail": detail or stage,
                }
        return callback

    def complete(self, job_id: str, result: dict) -> None:
        with self._lock:
            item = self._items.get(job_id)
            if not item:
                return
            state = result.get("status", "completed")
            item["progress"] = {
                "value": 1.0,
                "percent": 100,
                "stage": state,
                "detail": result.get("message") or ("Generation complete" if state == "completed" else state),
            }
            item["state"] = state
            item["result"] = result

    def fail(self, job_id: str, message: str) -> None:
        with self._lock:
            item = self._items.get(job_id)
            if not item:
                return
            item["state"] = "error"
            item["progress"] = {
                "value": 1.0,
                "percent": 100,
                "stage": "error",
                "detail": message,
            }
            item["result"] = {
                "status": "error",
                "message": message,
                "outputs": [],
                "output_urls": [],
            }

    def get(self, job_id: str) -> dict | None:
        with self._lock:
            item = self._items.get(job_id)
            if item is None:
                return None
            return json.loads(json.dumps(item, ensure_ascii=False))

    def snapshot(self, job_id: str) -> dict:
        item = self.get(job_id)
        if item is None:
            raise FileNotFoundError(job_id)
        return {
            "job": item["job"],
            "result": item["result"],
            "progress": item["progress"],
            "state": item["state"],
        }

    def forget(self, job_id: str) -> None:
        with self._lock:
            self._items.pop(job_id, None)


def make_handler(app: CreatorWebApp):
    class Handler(BaseHTTPRequestHandler):
        server_version = "AgenticGenstudio/0.1"

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            try:
                if parsed.path == "/api/jobs":
                    query = parse_qs(parsed.query)
                    limit = int(query.get("limit", ["20"])[0])
                    self._json({"jobs": app.list_jobs(limit=limit)})
                    return
                if parsed.path.startswith("/api/jobs/"):
                    job_id = parsed.path.rsplit("/", maxsplit=1)[-1]
                    self._json(app.get_job(job_id))
                    return
                if parsed.path.startswith("/outputs/"):
                    rel = parsed.path.removeprefix("/outputs/")
                    self._file((app.root / "outputs" / rel).resolve(), (app.root / "outputs").resolve())
                    return
                self._static(parsed.path)
            except FileNotFoundError:
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except Exception as exc:  # noqa: BLE001 - keep local app errors inspectable.
                self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self._read_body()
                prompt = str(payload.get("prompt", "")).strip()
                task_type = _parse_task_type(payload.get("task_type"))
                input_images = _collect_input_images(payload)
                resolution = _parse_resolution_override(payload.get("resolution"))
                outputs = _parse_outputs_override(payload.get("outputs"))
                if not prompt:
                    self._json({"error": "prompt is required"}, HTTPStatus.BAD_REQUEST)
                    return
                if self.path == "/api/plan":
                    job = plan(prompt, task_type_override=task_type)
                    if input_images is not None:
                        job.input_images = input_images
                    _apply_job_overrides(job, {"resolution": resolution, "outputs": outputs})
                    self._json({"job": job.to_dict()})
                    return
                if self.path == "/api/run":
                    self._json(app.run(prompt, task_type=task_type, input_images=input_images, resolution=resolution, outputs=outputs))
                    return
                if self.path == "/api/run_async":
                    self._json(
                        app.run_async(
                            prompt,
                            task_type=task_type,
                            input_images=input_images,
                            resolution=resolution,
                            outputs=outputs,
                        ),
                        HTTPStatus.ACCEPTED,
                    )
                    return
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except json.JSONDecodeError:
                self._json({"error": "invalid_json"}, HTTPStatus.BAD_REQUEST)
            except ValueError as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:  # noqa: BLE001
                self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def do_DELETE(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            try:
                if parsed.path.startswith("/api/jobs/"):
                    job_id = parsed.path.rsplit("/", maxsplit=1)[-1]
                    self._json(app.delete_job(job_id))
                    return
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except FileNotFoundError:
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except Exception as exc:  # noqa: BLE001
                self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def log_message(self, format: str, *args) -> None:  # noqa: A002
            print(f"{self.address_string()} - {format % args}")

        def _read_body(self) -> dict:
            length = int(self.headers.get("content-length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw or "{}")

        def _json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("content-type", "application/json; charset=utf-8")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _static(self, path: str) -> None:
            rel = "index.html" if path in {"", "/"} else path.lstrip("/")
            target = (app.static_dir / rel).resolve()
            self._file(target, app.static_dir.resolve(), rel)

        def _file(self, target: Path, root: Path, rel: str | None = None) -> None:
            label = rel or target.name
            if not str(target).startswith(str(root)) or not target.exists():
                raise FileNotFoundError(label)
            body = target.read_bytes()
            mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("content-type", mime)
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    app = CreatorWebApp()
    server = ThreadingHTTPServer((host, port), make_handler(app))
    print(f"Agentic GenStudio running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_task_type(value: object) -> str | None:
    if not value:
        return None
    task_type = str(value).strip()
    if task_type not in SUPPORTED_TASKS:
        raise ValueError(f"Unsupported task_type: {task_type}")
    return task_type


def _collect_input_images(payload: dict) -> list[str] | None:
    paths: list[str] = []
    for key in ["source_image", "mask_image"]:
        value = str(payload.get(key, "")).strip()
        if value:
            paths.append(value)
    return paths or None


def _parse_resolution_override(value: object) -> str | None:
    if value in {None, ""}:
        return None
    resolution = str(value).strip().lower()
    if not resolution:
        return None
    if not parse_qs(f"r={resolution}"):
        return None
    parts = resolution.split("x", maxsplit=1)
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError(f"Invalid resolution: {resolution}")
    return resolution


def _parse_outputs_override(value: object) -> int | None:
    if value in {None, ""}:
        return None
    outputs = int(value)
    if outputs < 1 or outputs > 12:
        raise ValueError("outputs must be between 1 and 12")
    return outputs


def _apply_job_overrides(job, overrides: dict) -> None:
    resolution = overrides.get("resolution")
    outputs = overrides.get("outputs")
    if resolution:
        job.resolution = resolution
    if outputs:
        job.outputs = outputs
