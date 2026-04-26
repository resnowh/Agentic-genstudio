@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"
set "PYTHONPATH=%ROOT%\src"

if not exist "%ENV%\python.exe" (
  echo Missing %ENV%\python.exe
  echo Run scripts\setup_diffusers_env.bat first.
  exit /b 1
)

if "%~1"=="" (
  set "PROMPT=masterpiece, best quality, 1girl, silver hair, blue eyes, anime style, rainy neon street, detailed background, 1024x1024"
) else (
  set "PROMPT=%*"
)

"%ENV%\python.exe" -m codex_creator.cli "%PROMPT%"
