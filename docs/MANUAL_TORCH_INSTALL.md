# Manual PyTorch Install

Use this when package managers stall or fail to show reliable progress.

The project environment already exists at:

```text
D:\ProgramData\WorkSpace\ImageGenerator\.venv-diffusers
```

## Option A: CUDA 13.0 Wheel Download

This is the verified route for the RTX 5080 Laptop GPU in this workspace.
Manually download these files with a browser or download manager, then place
them in:

```text
D:\ProgramData\WorkSpace\ImageGenerator\downloads\torch-cu130
```

Direct links:

```text
https://download.pytorch.org/whl/cu130/torch-2.11.0%2Bcu130-cp312-cp312-win_amd64.whl
https://download.pytorch.org/whl/cu130/torchvision-0.26.0%2Bcu130-cp312-cp312-win_amd64.whl
```

Install from the local downloads:

```powershell
.\scripts\install_torch_from_downloads.bat
```

## Option B: CPU Fallback

This is slower but much smaller and good for validating the app end to end:

```powershell
.\.venv-diffusers\python.exe -m pip install torch torchvision
.\.venv-diffusers\python.exe -m pip install -r requirements\diffusers.txt
```

## Verify

```powershell
.\.venv-diffusers\python.exe -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
```

## Continue

After PyTorch is installed:

```powershell
.\.venv-diffusers\python.exe -m pip install -r requirements\diffusers.txt
```
