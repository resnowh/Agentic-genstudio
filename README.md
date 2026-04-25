# Codex Creator Agent

Local AI creation orchestrator controlled by natural language.

The goal is to keep the user-facing surface simple:

```text
Create an anime character from this reference image, keep the same face,
change the pose to sitting by a window, and output 4 images.
```

Codex Creator Agent converts that request into a structured job, selects a
backend, records all assets and parameters, and leaves backend-specific
workflow details hidden.

## Current Status

This repository is the first local scaffold:

- Natural-language intent planning.
- Unified job schema.
- Asset manifest layout.
- Backend adapter interfaces.
- Dry-run execution that validates routing without installing heavy AI stacks.
- Diffusers adapter scaffold for real text-to-image, image-to-image, and inpaint execution once a local Python environment and model are configured.

No global Python packages are required for this version.

## Quick Start

From this directory:

```powershell
.\scripts\run_agent.bat "Generate an anime girl with silver hair, blue eyes, rainy street, output 4 images"
```

Run the local web app:

```powershell
.\scripts\run_web.bat
```

Then open:

```text
http://127.0.0.1:8765
```

Or:

```powershell
$env:PYTHONPATH="D:\ProgramData\WorkSpace\ImageGenerator\src"
python -m codex_creator.cli "Use reference.png to keep the character face and change the pose to sitting"
```

The command writes job records under `jobs/` and generated placeholders under
`outputs/`. Real image generation backends are wired in later through adapters.

## Real Generation Backend

The first real backend target is `diffusers`. See:

[docs/DIFFUSERS_BACKEND.md](docs/DIFFUSERS_BACKEND.md)

## Project Layout

```text
config/       Local settings.
docs/         Architecture and implementation plan.
inputs/       User-provided source images.
jobs/         Job JSON records.
manifests/    Models, characters, styles, and backend capabilities.
outputs/      Generated outputs and metadata.
src/          Codex Creator Agent source.
web/          Browser UI and client-side assets.
```
