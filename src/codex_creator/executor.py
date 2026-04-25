from __future__ import annotations

import json
from pathlib import Path

from .adapters import adapter_for
from .assets import AssetManager
from .router import choose_backend
from .schemas import ExecutionResult, Job, workspace_path


class Executor:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or workspace_path()
        self.assets = AssetManager(self.root)
        self.assets.ensure_workspace_dirs()

    def run(self, job: Job) -> ExecutionResult:
        job.backend = choose_backend(job, self.assets)
        self._write_job(job)
        adapter = adapter_for(job.backend, self.root)
        result = adapter.execute(job)
        self._write_result(result)
        return result

    def _write_job(self, job: Job) -> None:
        path = self.root / "jobs" / f"{job.job_id}.job.json"
        path.write_text(json.dumps(job.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def _write_result(self, result: ExecutionResult) -> None:
        path = self.root / "jobs" / f"{result.job_id}.result.json"
        path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

