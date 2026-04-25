@echo off
setlocal
set "ROOT=%~dp0.."
set "PYTHONPATH=%ROOT%\src"
python -m codex_creator.web_cli --host 127.0.0.1 --port 8765

