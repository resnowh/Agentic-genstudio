from __future__ import annotations

from .assets import AssetManager
from .schemas import Job


PREFERRED_BACKENDS = {
    "text_to_image": ["diffusers", "dry_run"],
    "image_to_image": ["diffusers", "dry_run"],
    "inpaint": ["diffusers", "comfyui", "dry_run"],
    "character_reference": ["comfyui", "dry_run"],
    "pose_transfer": ["comfyui", "dry_run"],
    "style_training": ["training", "dry_run"],
    "character_training": ["training", "dry_run"],
    "image_to_3d": ["three_d", "comfyui", "dry_run"],
    "upscale": ["diffusers", "comfyui", "dry_run"],
    "batch_variation": ["diffusers", "dry_run"],
}


def choose_backend(job: Job, assets: AssetManager) -> str:
    capabilities = assets.backend_capabilities()
    enabled = assets.enabled_backends() or {"dry_run"}
    for backend in PREFERRED_BACKENDS.get(job.task_type, ["dry_run"]):
        if backend not in enabled:
            continue
        supported = capabilities.get(backend, {}).get("supports", [])
        if job.task_type in supported:
            if backend not in {"dry_run", "comfyui", "training", "three_d"} and not assets.find_model_for(job.task_type, backend):
                continue
            return backend
    return "dry_run"
