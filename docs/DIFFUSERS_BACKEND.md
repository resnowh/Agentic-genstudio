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

Example setup once a compatible Python is available:

```powershell
python -m venv .venv-diffusers
.\.venv-diffusers\Scripts\python.exe -m pip install -r requirements\diffusers.txt
```

Run the agent with that interpreter:

```powershell
$env:PYTHONPATH="D:\ProgramData\WorkSpace\ImageGenerator\src"
.\.venv-diffusers\Scripts\python.exe -m codex_creator.cli "生成一个二次元银发蓝眼女孩，雨夜街道，输出4张"
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
