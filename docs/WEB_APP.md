# Web App

Agentic GenStudio includes a lightweight local web app built on Python's
standard library.

## Run

```powershell
.\scripts\run_web.bat
```

Open:

```text
http://127.0.0.1:8765
```

## Endpoints

- `GET /`: Browser UI.
- `POST /api/plan`: Convert a natural-language prompt into a planned job.
- `POST /api/run`: Plan and execute a prompt through the selected backend.
- `GET /api/jobs`: List recent job records.
- `GET /api/jobs/{job_id}`: Fetch a job and its result record.

## Current Behavior

The app uses the same backend routing as the CLI. With the default config, jobs
run through `dry_run`, which validates planning, routing, and persistence without
loading generation models.

