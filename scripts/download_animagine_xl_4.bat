@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"
set "MODEL_DIR=%ROOT%\models\diffusers\animagine-xl-4.0"
set "HF_HUB_DISABLE_SYMLINKS_WARNING=1"
set "HF_HUB_ENABLE_HF_TRANSFER=0"
set "HTTP_PROXY="
set "HTTPS_PROXY="
set "ALL_PROXY="
set "GIT_HTTP_PROXY="
set "GIT_HTTPS_PROXY="

if not exist "%ENV%\Scripts\hf.exe" (
  echo Missing %ENV%\Scripts\hf.exe
  echo Run .\.venv-diffusers\python.exe -m pip install -r requirements\diffusers.txt first.
  exit /b 1
)

mkdir "%MODEL_DIR%" >nul 2>nul

echo Downloading cagliostrolab/animagine-xl-4.0 to:
echo %MODEL_DIR%
echo.
echo Keep this window open. Hugging Face will show per-file progress.
echo If this stalls while anonymous, run scripts\login_huggingface.bat and retry.

"%ENV%\Scripts\hf.exe" download cagliostrolab/animagine-xl-4.0 ^
  --local-dir "%MODEL_DIR%" ^
  --max-workers 1 ^
  --include "README.md" ^
  --include "model_index.json" ^
  --include "scheduler/*" ^
  --include "text_encoder/*" ^
  --include "text_encoder_2/*" ^
  --include "tokenizer/*" ^
  --include "tokenizer_2/*" ^
  --include "unet/*" ^
  --include "vae/*"

if errorlevel 1 (
  echo.
  echo Download failed. You can re-run this script; completed files will be reused.
  exit /b 1
)

echo.
echo Download complete.
call "%ROOT%\scripts\verify_animagine_model.bat"
echo Run scripts\run_animagine_text_to_image.bat next.
