from __future__ import annotations

import json

from codex_creator.adapters.base import BackendAdapter
from codex_creator.schemas import ExecutionResult, Job


class DryRunAdapter(BackendAdapter):
    name = "dry_run"

    def execute(self, job: Job, progress_callback=None) -> ExecutionResult:
        if progress_callback:
            progress_callback(0.2, "preparing", "Dry-run job created.")
        out_dir = self.root / "outputs" / job.job_id
        out_dir.mkdir(parents=True, exist_ok=True)
        metadata_path = out_dir / "dry_run_metadata.json"
        metadata = {
            "message": "Dry run completed. Real backend integration is pending.",
            "job": job.to_dict(),
            "next_step": "Wire this task type to a real backend adapter.",
        }
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        if progress_callback:
            progress_callback(1.0, "completed", "Dry-run finished.")
        return ExecutionResult(
            job_id=job.job_id,
            backend=self.name,
            status="completed",
            outputs=[],
            metadata_path=str(metadata_path),
            message="Planned and routed successfully in dry-run mode.",
        )
