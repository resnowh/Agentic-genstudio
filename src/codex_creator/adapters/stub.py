from __future__ import annotations

from codex_creator.adapters.base import BackendAdapter
from codex_creator.schemas import ExecutionResult, Job


class StubAdapter(BackendAdapter):
    def __init__(self, root, name: str) -> None:
        super().__init__(root)
        self.name = name

    def execute(self, job: Job, progress_callback=None) -> ExecutionResult:
        if progress_callback:
            progress_callback(1.0, "blocked", f"Backend '{self.name}' is not implemented.")
        return ExecutionResult(
            job_id=job.job_id,
            backend=self.name,
            status="blocked",
            outputs=[],
            message=f"Backend '{self.name}' is selected but not implemented yet.",
        )
