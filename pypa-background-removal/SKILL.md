---
name: background-removal
description: "Remove backgrounds from images locally using rembg with GPU acceleration (ONNX Runtime CUDA / BiRefNet). Model: birefnet-general (high accuracy). Runs fully offline on the local machine. Use for: product photos, portraits, e-commerce, transparent PNGs, photo editing. Triggers: remove background, background removal, remove bg, transparent background, cut out image, background remover, rembg, product photo editing, cutout, transparent png, bg removal, photo cutout"
allowed-tools: run_in_terminal
---

# Background Removal (Local GPU)

Remove backgrounds from images locally using [rembg](https://github.com/danielgatis/rembg) with GPU acceleration via ONNX Runtime CUDA. No cloud service or API key required.

**Model:** `birefnet-general` — high-accuracy general-purpose background removal.

---

## Setup

> Always activate the `.venv` virtual environment first.

```powershell
# 1. Activate venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1

# 2. Install rembg with GPU support (onnxruntime-gpu for CUDA acceleration)
pip install "rembg[gpu]"
# If onnxruntime-gpu conflicts, install separately:
# pip install rembg onnxruntime-gpu
```

> **CPU-only fallback:** Replace `rembg[gpu]` with `rembg` — it will use `onnxruntime` (CPU).

---

## Quick Start

Use the bundled helper script [remove_bg.py](remove_bg.py) — it handles single files, multiple files, and directories. **Prefer this over inline Python one-liners.**

```powershell
# Activate venv first
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1

# Single file (output: input_nobg.png next to the input)
python .\.agents\skills\background-removal\remove_bg.py "C:\path\to\photo.jpg"
```

> **Note:** The `rembg.exe` CLI may be blocked by system policy. Use the script above instead.

---

## How To

### Single image
```powershell
& .\.venv\Scripts\Activate.ps1
python .\.agents\skills\background-removal\remove_bg.py "C:\path\to\photo.jpg"
```

### Multiple images
```powershell
python .\.agents\skills\background-removal\remove_bg.py "a.jpg" "b.png" "c.webp"
```

### Batch process a folder
```powershell
python .\.agents\skills\background-removal\remove_bg.py "C:\input_folder" --out "C:\output_folder"
```

### Pick a different model or output suffix
```powershell
python .\.agents\skills\background-removal\remove_bg.py "portrait.jpg" --model birefnet-portrait --suffix _cutout
```

### Script options
```text
inputs           One or more files or directories
--out DIR        Output directory (default: alongside each input)
--model NAME     rembg model (default: birefnet-general)
--suffix STR     Filename suffix before .png (default: _nobg)
```

### Check GPU is being used
```powershell
& .\.venv\Scripts\Activate.ps1
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
# Should include 'CUDAExecutionProvider' when GPU/CUDA toolkit is available
```

---

## Available Models

| Model | Best for |
|---|---|
| `birefnet-general` | General use — best overall quality |
| `birefnet-portrait` | Human portraits / headshots |
| `isnet-general-use` | Good general fallback |
| `u2net` | Fast, lightweight |
| `u2net_human_seg` | People / portraits |

---

## Use Cases

- **E-commerce**: Clean product photos
- **Portraits**: Professional headshots
- **Marketing**: Assets for design
- **Social Media**: Profile pictures
- **Design**: Elements for compositions

---

## Output

Produces a PNG with a transparent (alpha) background. The output filename should end in `.png`.

---

## Troubleshooting

- **CUDAExecutionProvider not listed:** Install the CUDA-enabled runtime: `pip install onnxruntime-gpu`
- **`cudnn64_9.dll is missing` (Error 126) on Windows:** onnxruntime-gpu 1.2x needs CUDA 12 + cuDNN 9. The CUDA Toolkit does **not** include cuDNN. Install it via pip and make sure its DLLs are on `PATH`:
  ```powershell
  & .\.venv\Scripts\Activate.ps1
  pip install nvidia-cudnn-cu12   # also pulls nvidia-cublas-cu12, nvidia-cuda-nvrtc-cu12
  ```
  This repo's `.venv` has a `sitecustomize.py` that auto-prepends those bin dirs to `PATH` and calls `os.add_dll_directory` on every Python start, so the CUDA EP loads transparently. If you recreate the venv, restore that file (it adds `<venv>\Lib\site-packages\nvidia\{cudnn,cublas,cuda_nvrtc}\bin`).
- **Model not found on first run:** rembg auto-downloads models to `~/.u2net/` on first use — requires internet for initial download.
- **Out of VRAM:** Use `u2net` (lighter model) or fall back to CPU with `rembg` (no GPU package).
- **Import errors:** Make sure `.venv` is activated before running any command.

