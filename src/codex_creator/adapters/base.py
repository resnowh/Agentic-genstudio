from __future__ import annotations

from pathlib import Path

from codex_creator.schemas import ExecutionResult, Job


class BackendAdapter:
    name = "base"

    def __init__(self, root: Path) -> None:
        self.root = root

    def execute(self, job: Job) -> ExecutionResult:
        raise NotImplementedError

