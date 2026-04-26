@echo off
setlocal
set "ROOT=%~dp0.."
set "PYTHONPATH=%ROOT%\src"
set "ENV=%ROOT%\.venv-diffusers"
if exist "%ENV%\python.exe" (
  "%ENV%\python.exe" -m codex_creator.web_cli --host 127.0.0.1 --port 8765
) else (
  python -m codex_creator.web_cli --host 127.0.0.1 --port 8765
)
