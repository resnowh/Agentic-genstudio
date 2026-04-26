# Diffusers Backend

The diffusers backend is the first real image-generation backend for Codex
Creator Agent.

## What It Supports

- `text_to_image`
- `image_to_image`
- `inpaint`

## Local Environment

Use a local environment, not the system Python. PyTorch support is usually best
on Python 3.11 or 3.12.

Recommended setup for this workspace:

```powershell
.\scripts\setup_diffusers_env.bat
```

This creates `.venv-diffusers` without touching the system Python.

For large downloads with visible progress, use the two-step flow:

```powershell
.\scripts\download_torch_wheels.bat
.\scripts\install_torch_from_downloads.bat
```

If package-manager downloads are unreliable, see:

[MANUAL_TORCH_INSTALL.md](MANUAL_TORCH_INSTALL.md)

The verified GPU stack for the RTX 5080 Laptop GPU is:

```text
Python 3.12.13
torch 2.11.0+cu130
torchvision 0.26.0+cu130
CUDA runtime 13.0
```

Run the agent with that interpreter:

```powershell
.\scripts\run_agent_diffusers.bat "生成一个二次元银发蓝眼女孩，雨夜街道，输出4张"
```

Run the web app with that interpreter:

```powershell
.\scripts\run_web_diffusers.bat
```

## Enabling

Set `config/settings.json`:

```json
"diffusers": {
  "enabled": true,
  "service_url": "local"
}
```

Then enable or add a model in `manifests/models.json`.

For Hugging Face models, `path` may be a model id such as:

```json
"path": "stabilityai/stable-diffusion-xl-base-1.0"
```

For local models, `path` may be an absolute local directory compatible with
diffusers.
