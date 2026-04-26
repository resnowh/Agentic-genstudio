@echo off
setlocal
set "ROOT=%~dp0.."
set "ENV=%ROOT%\.venv-diffusers"

where conda >nul 2>nul
if errorlevel 1 (
  echo conda was not found. Install Miniconda or Anaconda first.
  exit /b 1
)

if not exist "%ENV%\python.exe" (
  conda create -y -p "%ENV%" python=3.12 pip
)

"%ENV%\python.exe" -m pip install --upgrade pip
conda install -y -p "%ENV%" pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
"%ENV%\python.exe" -m pip install -r "%ROOT%\requirements\diffusers.txt"
"%ENV%\python.exe" -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
