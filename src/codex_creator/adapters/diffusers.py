from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codex_creator.adapters.base import BackendAdapter
from codex_creator.assets import AssetManager
from codex_creator.schemas import ExecutionResult, Job


class DiffusersAdapter(BackendAdapter):
    name = "diffusers"

    def execute(self, job: Job) -> ExecutionResult:
        missing = self._missing_dependencies()
        if missing:
            return self._blocked(
                job,
                "Diffusers backend is enabled, but dependencies are missing: "
                + ", ".join(missing)
                + ". Create a local Python 3.11/3.12 environment and install requirements/diffusers.txt.",
            )

        assets = AssetManager(self.root)
        model = assets.find_model_for(job.task_type, self.name)
        if not model:
            return self._blocked(
                job,
                "No enabled diffusers model is configured for this task. Add one to manifests/models.json or config/settings.json.",
            )

        try:
            outputs = self._run_pipeline(job, model)
        except Exception as exc:  # noqa: BLE001 - keep backend errors user-visible.
            return self._blocked(job, f"Diffusers execution failed: {exc}")

        return ExecutionResult(
            job_id=job.job_id,
            backend=self.name,
            status="completed",
            outputs=outputs,
            metadata_path=str(self._write_metadata(job, model, outputs)),
            message="Generated images with diffusers.",
        )

    def _missing_dependencies(self) -> list[str]:
        missing = []
        for module in ["torch", "diffusers", "PIL"]:
            try:
                __import__(module)
            except ImportError:
                missing.append("Pillow" if module == "PIL" else module)
        return missing

    def _run_pipeline(self, job: Job, model: dict[str, Any]) -> list[str]:
        import torch
        from diffusers import AutoPipelineForImage2Image, AutoPipelineForInpainting, AutoPipelineForText2Image
        from PIL import Image

        model_path = model["path"]
        width, height = _parse_resolution(_effective_resolution(job, model))
        output_count = _effective_outputs(job, model)
        out_dir = self.root / "outputs" / job.job_id
        out_dir.mkdir(parents=True, exist_ok=True)

        common_kwargs: dict[str, Any] = {
            "torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32,
        }
        cache_dir = model.get("cache_dir") or self._settings().get("model_cache_dir") or "models/hf-cache"
        if cache_dir:
            common_kwargs["cache_dir"] = str(_resolve_model_cache(cache_dir, self.root))
        if model.get("disable_safety_checker", False):
            # Some local or tiny validation models ship an incompatible safety checker.
            common_kwargs["safety_checker"] = None
            common_kwargs["requires_safety_checker"] = False
        if "variant" in model:
            common_kwargs["variant"] = model["variant"]
        if "use_safetensors" in model:
            common_kwargs["use_safetensors"] = bool(model["use_safetensors"])
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if job.task_type in {"text_to_image", "batch_variation"}:
            pipe = AutoPipelineForText2Image.from_pretrained(model_path, **common_kwargs).to(device)
            result = pipe(
                prompt=job.prompt,
                negative_prompt=job.parameters.get("negative_prompt"),
                width=width,
                height=height,
                num_inference_steps=int(_recommended_value(job, model, "steps", 28)),
                guidance_scale=float(_recommended_value(job, model, "cfg", 5.0)),
                num_images_per_prompt=output_count,
            )
        elif job.task_type == "image_to_image":
            source = _load_first_image(job, self.root, Image)
            pipe = AutoPipelineForImage2Image.from_pretrained(model_path, **common_kwargs).to(device)
            result = pipe(
                prompt=job.prompt,
                image=source,
                negative_prompt=job.parameters.get("negative_prompt"),
                strength=float(job.parameters.get("denoise", 0.45)),
                num_inference_steps=int(_recommended_value(job, model, "steps", 28)),
                guidance_scale=float(_recommended_value(job, model, "cfg", 5.0)),
                num_images_per_prompt=output_count,
            )
        elif job.task_type == "inpaint":
            source = _load_first_image(job, self.root, Image)
            mask = _load_mask_image(job, self.root, Image)
            pipe = AutoPipelineForInpainting.from_pretrained(model_path, **common_kwargs).to(device)
            result = pipe(
                prompt=job.prompt,
                image=source,
                mask_image=mask,
                negative_prompt=job.parameters.get("negative_prompt"),
                strength=float(job.parameters.get("denoise", 0.6)),
                num_inference_steps=int(_recommended_value(job, model, "steps", 28)),
                guidance_scale=float(_recommended_value(job, model, "cfg", 5.0)),
                num_images_per_prompt=output_count,
            )
        else:
            raise ValueError(f"Task '{job.task_type}' is not supported by diffusers adapter.")

        output_paths = []
        for index, image in enumerate(result.images, start=1):
            path = out_dir / f"image_{index:03}.png"
            image.save(path)
            output_paths.append(str(path))
        return output_paths

    def _write_metadata(self, job: Job, model: dict[str, Any], outputs: list[str]) -> Path:
        out_dir = self.root / "outputs" / job.job_id
        path = out_dir / "diffusers_metadata.json"
        path.write_text(
            json.dumps({"job": job.to_dict(), "model": model, "outputs": outputs}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def _settings(self) -> dict[str, Any]:
        return AssetManager(self.root).settings()

    def _blocked(self, job: Job, message: str) -> ExecutionResult:
        out_dir = self.root / "outputs" / job.job_id
        out_dir.mkdir(parents=True, exist_ok=True)
        metadata_path = out_dir / "diffusers_blocked.json"
        metadata_path.write_text(json.dumps({"job": job.to_dict(), "message": message}, indent=2, ensure_ascii=False), encoding="utf-8")
        return ExecutionResult(
            job_id=job.job_id,
            backend=self.name,
            status="blocked",
            outputs=[],
            metadata_path=str(metadata_path),
            message=message,
        )


def _parse_resolution(resolution: str) -> tuple[int, int]:
    width, height = resolution.lower().split("x", maxsplit=1)
    return int(width), int(height)


def _resolve_input(path_text: str, root: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    candidate = root / path
    if candidate.exists():
        return candidate
    return root / "inputs" / path


def _resolve_model_cache(path_text: str, root: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return root / path


def _recommended_value(job: Job, model: dict[str, Any], name: str, default: Any) -> Any:
    recommended = model.get("recommended", {})
    if model.get("prefer_model_recommended", False):
        if name == "cfg" and "guidance_scale" in recommended:
            return recommended["guidance_scale"]
        if name in recommended:
            return recommended[name]
    if name in job.parameters:
        return job.parameters[name]
    if name == "cfg" and "guidance_scale" in recommended:
        return recommended["guidance_scale"]
    return recommended.get(name, default)


def _effective_resolution(job: Job, model: dict[str, Any]) -> str:
    recommended = model.get("recommended", {})
    if model.get("prefer_model_recommended", False) and "resolution" in recommended:
        return str(recommended["resolution"])
    return job.resolution


def _effective_outputs(job: Job, model: dict[str, Any]) -> int:
    recommended = model.get("recommended", {})
    if model.get("prefer_model_recommended", False) and "outputs" in recommended:
        return int(recommended["outputs"])
    return job.outputs


def _load_first_image(job: Job, root: Path, image_module):
    if not job.input_images:
        raise ValueError("This task requires an input image.")
    path = _resolve_input(job.input_images[0], root)
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {path}")
    return image_module.open(path).convert("RGB")


def _load_mask_image(job: Job, root: Path, image_module):
    mask_candidates = [p for p in job.input_images if "mask" in p.lower()]
    if not mask_candidates:
        raise ValueError("Inpaint tasks require a mask image path containing 'mask'.")
    path = _resolve_input(mask_candidates[0], root)
    if not path.exists():
        raise FileNotFoundError(f"Mask image not found: {path}")
    return image_module.open(path).convert("L")
