# Production Anime Model

The first production anime model target is:

```text
cagliostrolab/animagine-xl-4.0
```

It is configured in `manifests/models.json` as `animagine-xl-4.0`.

## Download

Run this in a normal terminal so download progress is visible:

```powershell
.\scripts\download_animagine_xl_4.bat
```

The model is stored locally under:

```text
models/diffusers/animagine-xl-4.0
```

Large model files are ignored by Git.

## Generate

After the download completes:

```powershell
.\scripts\run_animagine_text_to_image.bat
```

Or pass your own prompt:

```powershell
.\scripts\run_animagine_text_to_image.bat "masterpiece, best quality, 1girl, silver hair, blue eyes, night city"
```

Outputs are written under:

```text
outputs/<job_id>/image_001.png
```

## Fallback Behavior

`animagine-xl-4.0` has `require_local: true`. Until the local model directory
exists, the router skips it and continues using the tiny smoke-test model. This
keeps the app usable while a large model download is still pending.
