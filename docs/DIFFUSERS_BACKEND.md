# Diffusers Backend

`diffusers` is the first real local image-generation backend in Agentic
GenStudio.

## Current Support

- `text_to_image`
- `image_to_image`
- `inpaint`
- `batch_variation`

Practical status today:

- `text_to_image` is verified with the local production anime model
- `image_to_image` and `inpaint` are implemented at the adapter level but still
  need a stronger end-to-end user flow in the web app

## Production Model

Current production anime model:

```text
cagliostrolab/animagine-xl-4.0
```

Configured locally as:

```text
models/diffusers/animagine-xl-4.0
```

Model manifest:

`manifests/models.json`

## Smoke-Test Model

The project also keeps a tiny validation model:

```text
hf-internal-testing/tiny-stable-diffusion-pipe
```

This exists to verify the full execution path with a minimal download. It is
not suitable for production output quality.

Run:

```powershell
.\scripts\run_real_smoke_test.bat
```

## Prompt Path

`diffusers` does not always receive the raw user prompt directly.

The effective inference prompt is:

1. original user prompt
2. adapted by the local prompt adapter when needed
3. stored as `parameters.positive_prompt`
4. merged with model quality suffix tags
5. deduplicated before inference

The negative prompt is:

1. default or adapted `parameters.negative_prompt`
2. merged with model manifest negative tags
3. deduplicated before inference

This keeps the original prompt auditable while still feeding the model a
cleaner prompt.

## Runtime

Use the isolated local environment:

```powershell
.\scripts\setup_diffusers_env.bat
```

Verified GPU stack for the current machine family:

```text
Python 3.12.13
torch 2.11.0+cu130
torchvision 0.26.0+cu130
CUDA runtime 13.0
```

Verification:

```powershell
.\scripts\verify_diffusers_env.bat
```

## Run Paths

CLI:

```powershell
.\scripts\run_agent_diffusers.bat "Generate an anime girl with silver hair, blue eyes, rainy street, output 4 images"
```

Web:

```powershell
.\scripts\run_web_diffusers.bat
```

## Output Contract

Expected result shape:

```text
backend: diffusers
status: completed | blocked | error
outputs: outputs/<job_id>/image_001.png ...
metadata_path: outputs/<job_id>/diffusers_metadata.json
```

## Known Limits

- the current prompt adapter is rule-based, not semantic translation
- long prompt strings can still trigger tokenizer length warnings
- image-to-image and inpaint are not yet fully polished in the browser workflow
