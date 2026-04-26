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

"%ENV%\python.exe" -m codex_creator.web_cli --host 127.0.0.1 --port 8765

