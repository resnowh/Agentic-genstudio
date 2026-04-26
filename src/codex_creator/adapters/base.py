from __future__ import annotations

from pathlib import Path
from typing import Callable

from codex_creator.schemas import ExecutionResult, Job


class BackendAdapter:
    name = "base"

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(
        self,
        job: Job,
        progress_callback: Callable[[float, str, str | None], None] | None = None,
    ) -> ExecutionResult:
        raise NotImplementedError
