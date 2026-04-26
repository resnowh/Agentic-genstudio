@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"
set "DOWNLOADS=%ROOT%\downloads\torch-cu130"

if not exist "%ENV%\python.exe" (
  echo Missing %ENV%\python.exe
  echo Run scripts\setup_diffusers_env.bat first.
  exit /b 1
)

mkdir "%DOWNLOADS%" >nul 2>nul

"%ENV%\python.exe" -m pip download -r "%ROOT%\requirements\torch-cu130.txt" --index-url https://download.pytorch.org/whl/cu130 --dest "%DOWNLOADS%" --progress-bar on
