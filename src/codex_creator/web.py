from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .executor import Executor
from .planner import plan
from .schemas import workspace_path


class CreatorWebApp:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or workspace_path()
        self.static_dir = self.root / "web"
        self.executor = Executor(self.root)

    def plan(self, prompt: str) -> dict:
        return plan(prompt).to_dict()

    def run(self, prompt: str) -> dict:
        job = plan(prompt)
        result = self.executor.run(job)
        return {"job": job.to_dict(), "result": result.to_dict()}

    def list_jobs(self, limit: int = 20) -> list[dict]:
        job_dir = self.root / "jobs"
        items = sorted(job_dir.glob("*.job.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        jobs: list[dict] = []
        for path in items[:limit]:
            jobs.append(_read_json(path))
        return jobs

    def get_job(self, job_id: str) -> dict:
        job_path = self.root / "jobs" / f"{job_id}.job.json"
        result_path = self.root / "jobs" / f"{job_id}.result.json"
        if not job_path.exists():
            raise FileNotFoundError(job_id)
        return {
            "job": _read_json(job_path),
            "result": _read_json(result_path) if result_path.exists() else None,
        }


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
                self._static(parsed.path)
            except FileNotFoundError:
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except Exception as exc:  # noqa: BLE001 - keep local app errors inspectable.
                self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self._read_body()
                prompt = str(payload.get("prompt", "")).strip()
                if not prompt:
                    self._json({"error": "prompt is required"}, HTTPStatus.BAD_REQUEST)
                    return
                if self.path == "/api/plan":
                    self._json({"job": app.plan(prompt)})
                    return
                if self.path == "/api/run":
                    self._json(app.run(prompt))
                    return
                self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            except json.JSONDecodeError:
                self._json({"error": "invalid_json"}, HTTPStatus.BAD_REQUEST)
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
            if not str(target).startswith(str(app.static_dir.resolve())) or not target.exists():
                raise FileNotFoundError(rel)
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

