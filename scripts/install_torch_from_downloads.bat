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

"%ENV%\python.exe" -m pip install --no-index --find-links "%DOWNLOADS%" -r "%ROOT%\requirements\torch-cu130.txt"
"%ENV%\python.exe" -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
