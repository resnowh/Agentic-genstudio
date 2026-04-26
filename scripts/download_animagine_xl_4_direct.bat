@echo off
setlocal
set "ROOT=%~dp0.."
set "MODEL_DIR=%ROOT%\models\diffusers\animagine-xl-4.0"
set "BASE=https://huggingface.co/cagliostrolab/animagine-xl-4.0/resolve/main"
set "HTTP_PROXY="
set "HTTPS_PROXY="
set "ALL_PROXY="
set "GIT_HTTP_PROXY="
set "GIT_HTTPS_PROXY="

mkdir "%MODEL_DIR%" >nul 2>nul
mkdir "%MODEL_DIR%\scheduler" >nul 2>nul
mkdir "%MODEL_DIR%\text_encoder" >nul 2>nul
mkdir "%MODEL_DIR%\text_encoder_2" >nul 2>nul
mkdir "%MODEL_DIR%\tokenizer" >nul 2>nul
mkdir "%MODEL_DIR%\tokenizer_2" >nul 2>nul
mkdir "%MODEL_DIR%\unet" >nul 2>nul
mkdir "%MODEL_DIR%\vae" >nul 2>nul

echo Downloading Animagine XL 4.0 diffusers files to:
echo %MODEL_DIR%
echo.
echo This window shows real curl progress and supports resume.
echo.

call :fetch "README.md" "README.md"
call :fetch "model_index.json" "model_index.json"
call :fetch "scheduler/scheduler_config.json" "scheduler\scheduler_config.json"
call :fetch "text_encoder/config.json" "text_encoder\config.json"
call :fetch "text_encoder/model.safetensors" "text_encoder\model.safetensors"
call :fetch "text_encoder_2/config.json" "text_encoder_2\config.json"
call :fetch "text_encoder_2/model.safetensors" "text_encoder_2\model.safetensors"
call :fetch "tokenizer/merges.txt" "tokenizer\merges.txt"
call :fetch "tokenizer/special_tokens_map.json" "tokenizer\special_tokens_map.json"
call :fetch "tokenizer/tokenizer_config.json" "tokenizer\tokenizer_config.json"
call :fetch "tokenizer/vocab.json" "tokenizer\vocab.json"
call :fetch "tokenizer_2/merges.txt" "tokenizer_2\merges.txt"
call :fetch "tokenizer_2/special_tokens_map.json" "tokenizer_2\special_tokens_map.json"
call :fetch "tokenizer_2/tokenizer_config.json" "tokenizer_2\tokenizer_config.json"
call :fetch "tokenizer_2/vocab.json" "tokenizer_2\vocab.json"
call :fetch "unet/config.json" "unet\config.json"
call :fetch "unet/diffusion_pytorch_model.safetensors" "unet\diffusion_pytorch_model.safetensors"
call :fetch "vae/config.json" "vae\config.json"
call :fetch "vae/diffusion_pytorch_model.safetensors" "vae\diffusion_pytorch_model.safetensors"

echo.
call "%ROOT%\scripts\verify_animagine_model.bat"
if errorlevel 1 exit /b 1
echo Run scripts\run_animagine_text_to_image.bat next.
exit /b 0

:fetch
set "REMOTE=%~1"
set "LOCAL=%~2"
echo.
echo [%REMOTE%]
curl.exe -L --fail --retry 5 --retry-delay 5 -C - -o "%MODEL_DIR%\%LOCAL%" "%BASE%/%REMOTE%"
if errorlevel 1 (
  echo Download failed for %REMOTE%
  exit /b 1
)
exit /b 0
