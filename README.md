# Agentic GenStudio

Local AI image-generation studio controlled by natural language.

The project goal is to keep the user-facing surface simple:

```text
Use this character reference, keep the same face, change the pose to sitting
by a window, and output 4 images.
```

The app converts that request into a structured local job, selects a backend,
applies prompt adaptation, runs generation, and records the result.

## What Exists Today

- Local CLI and local web app.
- Real local text-to-image with `diffusers` and `Animagine XL 4.0`.
- Rule-based Chinese prompt adaptation to model-friendly English tags.
- Automatic negative prompt defaults.
- Generation progress, gallery preview, and recent-job history.
- Local job/result persistence under `jobs/` and `outputs/`.
- Isolated `.venv-diffusers` runtime. No system Python pollution.

## Current Scope

Working now:

- `text_to_image`
- basic `image_to_image` backend wiring
- basic `inpaint` backend wiring
- custom resolution
- 1-12 output images
- history preview and deletion

Not production-ready yet:

- robust Chinese semantic prompt understanding
- web upload flow for source images and masks
- identity preservation
- pose control
- LoRA training
- image-to-3D

## Quick Start

Run the web app:

```powershell
.\scripts\run_web.bat
```

Then open:

```text
http://127.0.0.1:8765
```

Run the CLI:

```powershell
.\scripts\run_agent.bat "Generate an anime girl with silver hair, blue eyes, rainy street, output 4 images"
```

Or:

```powershell
$env:PYTHONPATH="D:\ProgramData\WorkSpace\ImageGenerator\src"
python -m codex_creator.cli "Use reference.png to keep the character face and change the pose to sitting"
```

## Local Runtime

Create the isolated runtime:

```powershell
.\scripts\setup_diffusers_env.bat
```

Install the verified RTX 5080 Laptop GPU stack:

```powershell
.\scripts\install_torch_from_downloads.bat
.\.venv-diffusers\python.exe -m pip install -r requirements\diffusers.txt
.\scripts\verify_diffusers_env.bat
```

## Models

Production anime model:

```text
cagliostrolab/animagine-xl-4.0
```

Configured in:

`manifests/models.json`

Download and verify:

```powershell
.\scripts\download_animagine_xl_4.bat
.\scripts\verify_animagine_model.bat
```

Fallback smoke-test model:

```text
hf-internal-testing/tiny-stable-diffusion-pipe
```

## Prompt Handling

- The original user prompt is preserved in the job record.
- Chinese input is processed locally by a rule-based prompt adapter.
- The adapter writes:
  - `parameters.prompt_language`
  - `parameters.positive_prompt`
  - `parameters.negative_prompt`
  - `parameters.prompt_adapter`
- `diffusers` uses the adapted positive prompt for inference.

This is local-only behavior. The prompt is not sent to OpenAI or another cloud
translation service.

## Output Layout

```text
jobs/      Job and result JSON records.
outputs/   Generated images and metadata.
inputs/    User-provided source images.
models/    Local models and cache.
web/       Browser UI assets.
src/       Application source.
docs/      Project documentation.
```

## Documentation Map

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/WEB_APP.md](docs/WEB_APP.md)
- [docs/DIFFUSERS_BACKEND.md](docs/DIFFUSERS_BACKEND.md)
- [docs/PRODUCTION_ANIME_MODEL.md](docs/PRODUCTION_ANIME_MODEL.md)
- [docs/PROMPT_ADAPTER.md](docs/PROMPT_ADAPTER.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/MANUAL_TORCH_INSTALL.md](docs/MANUAL_TORCH_INSTALL.md)
