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

If `hf download` is unreliable on your network, use the direct resumable
downloader instead:

```powershell
.\scripts\download_animagine_xl_4_direct.bat
```

The script downloads the public Hugging Face repository with:

```powershell
hf download cagliostrolab/animagine-xl-4.0 --local-dir models/diffusers/animagine-xl-4.0 --max-workers 1 --include "README.md" --include "model_index.json" --include "scheduler/*" --include "text_encoder/*" --include "text_encoder_2/*" --include "tokenizer/*" --include "tokenizer_2/*" --include "unet/*" --include "vae/*"
```

This downloads the diffusers folder layout only. It intentionally skips the
top-level single-file checkpoints because the app loads the model with
diffusers `from_pretrained(...)`.

If anonymous downloads stall, log the local Hugging Face CLI in and retry:

```powershell
.\scripts\login_huggingface.bat
.\scripts\download_animagine_xl_4.bat
```

The Hugging Face plugin used by Codex is separate from the local `hf.exe`
login state, so the local downloader may still be anonymous until this login is
completed.

The model is stored locally under:

```text
models/diffusers/animagine-xl-4.0
```

Large model files are ignored by Git.

Verify the local model files:

```powershell
.\scripts\verify_animagine_model.bat
```

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
