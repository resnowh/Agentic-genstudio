# Architecture

Agentic GenStudio is a local orchestration layer. The user gives a creative
goal in natural language; the system plans a job, adapts prompts, chooses a
backend, runs generation, and records outputs.

## Flow

```text
Natural language input
  -> planner
  -> prompt adapter
  -> unified Job
  -> asset manager
  -> backend router
  -> executor
  -> backend adapter
  -> result persistence
  -> web/CLI presentation
```

## Main Components

- `planner`
  Converts user input into a structured `Job`.
  Decides task type, output count, resolution, and baseline parameters.

- `prompt_adapter`
  Applies local prompt adaptation rules.
  Current implementation converts Chinese prompts into English-style anime tags
  and injects default negative prompt tags.

- `assets`
  Loads manifests and local settings.
  Exposes enabled backends, configured models, and model availability checks.

- `router`
  Chooses a backend for a given job based on task type, enabled backends, and
  available models.

- `executor`
  Writes the job record, invokes the adapter, and writes the result record.

- `adapters`
  Backend-specific execution code.
  Current adapters are `diffusers`, `dry_run`, and `stub`.

- `web`
  Local standard-library HTTP app.
  Provides planning, async execution, progress polling, job history, preview,
  and deletion.

## Unified Job Contract

Core fields in `Job`:

- `prompt`: original user input
- `task_type`
- `input_images`
- `outputs`
- `resolution`
- `backend`
- `parameters`

Important `parameters` currently used:

- `steps`
- `cfg`
- `sampler`
- `denoise`
- `negative_prompt`
- `positive_prompt`
- `prompt_language`
- `prompt_adapter`

The original prompt is preserved. Model-specific prompt shaping happens through
`parameters`, not by overwriting the original user text.

## Backend Strategy

- `diffusers`
  Current production backend for local text-to-image.
  Also contains basic paths for image-to-image and inpaint.

- `dry_run`
  Validation backend used when a real backend is unavailable.

- `comfyui`
  Reserved for advanced workflows such as ControlNet, pose control, reference
  identity, and community pipelines.

- `training`
  Reserved for LoRA or equivalent local training.

- `three_d`
  Reserved for image-to-3D engines.

## Current Execution Model

Today, the practical path is:

```text
web/cli -> planner -> prompt_adapter -> router -> diffusers -> local model
```

Production model:

```text
models/diffusers/animagine-xl-4.0
```

The adapter loads the model locally through `diffusers.from_pretrained(...)`,
runs inference on the local GPU, saves PNG outputs, and writes metadata.

## Persistence

- `jobs/<job_id>.job.json`
  Planned job record.

- `jobs/<job_id>.result.json`
  Execution result record.

- `outputs/<job_id>/image_*.png`
  Generated images.

- `outputs/<job_id>/diffusers_metadata.json`
  Adapter-level metadata for the run.

## Design Boundary

The user should not need to choose:

- node graphs
- internal workflow topology
- model paths
- CFG, denoise, or backend-specific switches

Those are internal execution choices. The project is deliberately structured so
future agents can control the same generation system through the same job
interface.
