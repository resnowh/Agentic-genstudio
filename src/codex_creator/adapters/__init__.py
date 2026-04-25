from __future__ import annotations

from pathlib import Path

from .base import BackendAdapter
from .diffusers import DiffusersAdapter
from .dry_run import DryRunAdapter
from .stub import StubAdapter


def adapter_for(name: str, root: Path) -> BackendAdapter:
    if name == "dry_run":
        return DryRunAdapter(root)
    if name == "diffusers":
        return DiffusersAdapter(root)
    return StubAdapter(root, name)
