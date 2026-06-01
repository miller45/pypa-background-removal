# Background Removal Skill

A VS Code Copilot **skill** for removing image backgrounds locally using [rembg](https://github.com/danielgatis/rembg) with GPU acceleration (ONNX Runtime CUDA / BiRefNet). Runs fully offline — no cloud service or API key required.

- **Model:** `birefnet-general` (high accuracy, general purpose)
- **Runtime:** ONNX Runtime (CUDA when available, CPU fallback)
- **Output:** Transparent PNG

See [SKILL.md](SKILL.md) for the full skill instructions Copilot uses.

---

## Contents

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Skill metadata + instructions consumed by Copilot |
| [remove_bg.py](remove_bg.py) | Helper CLI script: single file, multiple files, or folder |

---

## Installation

### 1. Install the skill into a workspace

Skills are discovered from a `.agents/skills/<skill-name>/` folder inside your workspace. Copy (or clone) this folder there:

```powershell
# From your target workspace root
New-Item -ItemType Directory -Force -Path .\.agents\skills | Out-Null
git clone https://github.com/<your-org>/pypa-background-removal .\.agents\skills\background-removal
```

Or copy the two files (`SKILL.md`, `remove_bg.py`) manually into `.agents/skills/background-removal/`.

Restart VS Code (or reload the Copilot Chat window) so the skill is picked up.

### 2. Create and activate a Python virtual environment

```powershell
# From your workspace root
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

### 3. Install rembg

**GPU (recommended, requires NVIDIA CUDA 12):**
```powershell
pip install "rembg[gpu]"
# If the extra fails to resolve:
# pip install rembg onnxruntime-gpu
```

**CPU only:**
```powershell
pip install rembg
```

### 4. (GPU only) Install cuDNN

`onnxruntime-gpu` 1.2x needs CUDA 12 + cuDNN 9. The CUDA Toolkit does **not** ship cuDNN. Install it via pip:

```powershell
pip install nvidia-cudnn-cu12
```

To make the cuDNN/cuBLAS DLLs discoverable on every Python start, add a `sitecustomize.py` to your venv at `.venv\Lib\site-packages\sitecustomize.py`:

```python
import os, sys
from pathlib import Path

site_packages = Path(sys.prefix) / "Lib" / "site-packages"
for sub in ("cudnn", "cublas", "cuda_nvrtc"):
    bin_dir = site_packages / "nvidia" / sub / "bin"
    if bin_dir.is_dir():
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
        os.add_dll_directory(str(bin_dir))
```

### 5. Verify GPU is detected

```powershell
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Expect: ['CUDAExecutionProvider', 'CPUExecutionProvider']
```

---

## Usage

After activating `.venv`:

```powershell
# Single file -> photo_nobg.png next to the input
python .\.agents\skills\background-removal\remove_bg.py "C:\path\to\photo.jpg"

# Multiple files
python .\.agents\skills\background-removal\remove_bg.py "a.jpg" "b.png" "c.webp"

# Whole folder
python .\.agents\skills\background-removal\remove_bg.py "C:\input" --out "C:\output"

# Different model / suffix
python .\.agents\skills\background-removal\remove_bg.py "portrait.jpg" --model birefnet-portrait --suffix _cutout
```

### Options

| Flag | Description |
|---|---|
| `inputs` | One or more files or directories (positional) |
| `--out DIR` | Output directory (default: alongside each input) |
| `--model NAME` | rembg model name (default: `birefnet-general`) |
| `--suffix STR` | Filename suffix before `.png` (default: `_nobg`) |

### Available models

| Model | Best for |
|---|---|
| `birefnet-general` | General use — best overall quality |
| `birefnet-portrait` | Human portraits / headshots |
| `isnet-general-use` | Good general fallback |
| `u2net` | Fast, lightweight |
| `u2net_human_seg` | People / portraits |

Models auto-download to `~/.u2net/` on first use (requires internet once).

---

## Using the skill from Copilot Chat

Once installed, just ask Copilot naturally:

- "Remove the background from `photo.jpg`"
- "Make a transparent PNG of this product image"
- "Batch-remove backgrounds from the `./products` folder"

Copilot will read [SKILL.md](SKILL.md) and run the helper script with the right arguments.

---

## Troubleshooting

- **`CUDAExecutionProvider` not listed** — install `onnxruntime-gpu` and `nvidia-cudnn-cu12`.
- **`cudnn64_9.dll is missing` (Error 126)** — see step 4 above; the `sitecustomize.py` snippet fixes this.
- **`rembg.exe` blocked by policy** — use the bundled `remove_bg.py` script instead.
- **Out of VRAM** — switch to a lighter model (`--model u2net`) or use the CPU build.
- **Import errors** — make sure `.venv` is activated.

---

## License

rembg and the BiRefNet/U²-Net models retain their respective licenses. This skill is a thin wrapper.
