@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"
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

echo This logs the local Hugging Face CLI in for downloads.
echo Generate a token at https://huggingface.co/settings/tokens
echo A read-only token is enough for public model downloads.
echo.

"%ENV%\Scripts\hf.exe" auth login
