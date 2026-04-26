@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"

if not exist "%ENV%\python.exe" (
  echo Missing %ENV%\python.exe
  exit /b 1
)

"%ENV%\python.exe" -c "import importlib.util; print('torch', importlib.util.find_spec('torch') is not None); print('diffusers', importlib.util.find_spec('diffusers') is not None)"
"%ENV%\python.exe" -c "import torch; print('torch_version', torch.__version__); print('cuda_available', torch.cuda.is_available())"

