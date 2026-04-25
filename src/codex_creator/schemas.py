from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


SUPPORTED_TASKS = {
    "text_to_image",
    "image_to_image",
    "inpaint",
    "character_reference",
    "pose_transfer",
    "style_training",
    "character_training",
    "image_to_3d",
    "upscale",
    "batch_variation",
}


@dataclass
class Job:
    prompt: str
    task_type: str
    job_id: str = field(default_factory=lambda: uuid4().hex)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    input_images: list[str] = field(default_factory=list)
    preserve: list[str] = field(default_factory=list)
    change: list[str] = field(default_factory=list)
    style: str | None = None
    character: str | None = None
    outputs: int = 4
    resolution: str = "1024x1024"
    backend: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "created_at": self.created_at,
            "prompt": self.prompt,
            "task_type": self.task_type,
            "input_images": self.input_images,
            "preserve": self.preserve,
            "change": self.change,
            "style": self.style,
            "character": self.character,
            "outputs": self.outputs,
            "resolution": self.resolution,
            "backend": self.backend,
            "parameters": self.parameters,
        }


@dataclass
class ExecutionResult:
    job_id: str
    backend: str
    status: str
    outputs: list[str] = field(default_factory=list)
    metadata_path: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "backend": self.backend,
            "status": self.status,
            "outputs": self.outputs,
            "metadata_path": self.metadata_path,
            "message": self.message,
        }


def workspace_path() -> Path:
    return Path(__file__).resolve().parents[2]

