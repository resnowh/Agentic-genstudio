@echo off
setlocal
set "ROOT=%~dp0.."
set "PYTHONPATH=%ROOT%\src"
python -m codex_creator.cli %*

