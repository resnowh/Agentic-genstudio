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

## What The UI Does

- accepts natural-language prompts
- allows manual task mode selection
- allows preset or custom resolution
- allows 1-12 output images
- shows async generation progress
- previews generated images
- shows recent job history with preview thumbnails
- lets the user delete job history and generated files

## Current Task Modes

- `text_to_image`
- `image_to_image`
- `inpaint`

Current status:

- `text_to_image` is the primary working path
- `image_to_image` and `inpaint` are wired but still need a stronger input UX

## Prompt Presentation

The task preview currently shows:

- original prompt
- input language
- adapted model prompt
- negative prompt
- resolution
- output count
- backend when assigned

This is intentional. The system keeps the original prompt for traceability while
also exposing the actual prompt text sent to the model.

## Endpoints

- `GET /`
  Browser UI.

- `POST /api/plan`
  Convert a natural-language request into a structured job.

- `POST /api/run`
  Synchronous plan-and-run path.

- `POST /api/run_async`
  Start execution and return an async job handle.

- `GET /api/jobs`
  List recent jobs with preview information.

- `GET /api/jobs/{job_id}`
  Fetch a job, result, and progress state.

- `DELETE /api/jobs/{job_id}`
  Delete the job record, result record, and output directory.

## Current Backend Behavior

With the current local setup:

- text-to-image routes to `diffusers`
- the preferred local production model is `animagine-xl-4.0`
- if that model is unavailable, routing may fall back depending on the enabled
  backend set and available models

## Known Gaps

- no browser-side image upload flow yet
- source images and mask images are still path-based
- no mask painting UI
- no integrated character card UI
- no direct pose-control UI

The current web app is a real local generation tool, but it is still an early
operator surface for the larger agentic system.
