from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import workspace_path


class AssetManager:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or workspace_path()
        self.manifest_dir = self.root / "manifests"

    def load_manifest(self, name: str) -> dict[str, Any]:
        path = self.manifest_dir / name
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def backend_capabilities(self) -> dict[str, Any]:
        return self.load_manifest("backends.json").get("backends", {})

    def models(self) -> list[dict[str, Any]]:
        return self.load_manifest("models.json").get("models", [])

    def find_model_for(self, task_type: str, backend: str) -> dict[str, Any] | None:
        for model in self.models():
            if not model.get("enabled", False):
                continue
            if model.get("type") != backend:
                continue
            if task_type in model.get("supports", []):
                if not self._model_is_available(model):
                    continue
                return model
        default_name = self.settings().get("default_models", {}).get(task_type)
        if default_name:
            return {
                "name": default_name,
                "type": backend,
                "path": default_name,
                "supports": [task_type],
            }
        return None

    def _model_is_available(self, model: dict[str, Any]) -> bool:
        if not model.get("require_local", False):
            return True
        path_text = model.get("path")
        if not path_text:
            return False
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        if not path.exists():
            return False
        required_files = model.get("required_files", [])
        for pattern in required_files:
            if not any(path.glob(pattern)):
                return False
        return True

    def settings(self) -> dict[str, Any]:
        settings_path = self.root / "config" / "settings.json"
        if not settings_path.exists():
            settings_path = self.root / "config" / "settings.example.json"
        if not settings_path.exists():
            return {}
        return json.loads(settings_path.read_text(encoding="utf-8"))

    def enabled_backends(self) -> set[str]:
        backends = self.settings().get("backends", {})
        return {name for name, cfg in backends.items() if cfg.get("enabled", False)}

    def ensure_workspace_dirs(self) -> None:
        for rel in [
            "inputs",
            "outputs",
            "jobs",
            "projects",
            "characters",
            "styles",
            "training",
            "logs",
            "models",
            "models/checkpoints",
            "models/loras",
            "models/controlnet",
            "models/clip_vision",
            "models/vae",
        ]:
            (self.root / rel).mkdir(parents=True, exist_ok=True)
