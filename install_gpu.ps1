$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

& $python -m pip install --upgrade pip
& $python -m pip install --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
& $python -m pip install --force-reinstall pyg_lib torch_scatter torch_sparse -f https://data.pyg.org/whl/torch-2.11.0+cu128.html
& $python -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")

& $python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
