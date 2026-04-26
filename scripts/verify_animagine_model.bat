@echo off
setlocal
set "ROOT=%~dp0.."
set "MODEL_DIR=%ROOT%\models\diffusers\animagine-xl-4.0"

set "MISSING="

if not exist "%MODEL_DIR%\model_index.json" set "MISSING=1"
if not exist "%MODEL_DIR%\unet\*.safetensors" set "MISSING=1"
if not exist "%MODEL_DIR%\vae\*.safetensors" set "MISSING=1"
if not exist "%MODEL_DIR%\text_encoder\*.safetensors" set "MISSING=1"
if not exist "%MODEL_DIR%\text_encoder_2\*.safetensors" set "MISSING=1"

if defined MISSING (
  echo Animagine XL 4.0 is incomplete.
  echo Expected model files under:
  echo %MODEL_DIR%
  exit /b 1
)

echo Animagine XL 4.0 model files look complete:
echo %MODEL_DIR%
