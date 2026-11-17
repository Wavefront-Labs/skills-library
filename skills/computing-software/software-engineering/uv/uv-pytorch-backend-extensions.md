---
id: computing-software.software-engineering.uv.uv-pytorch-backend-extensions
name: uv-pytorch-backend-extensions
category: computing-software
field: software-engineering
product: uv
tags: [uv, pytorch, torch-backend, uv-pip, cuda, gpu-extensions, astral-gpu-indexes, flash-attn]
level: practitioner
status: docs-checked
description: "Use uv pip with --torch-backend for automatic PyTorch accelerator selection, and install GPU extensions like flash-attn from Astral GPU indexes."
sources: [https://docs.astral.sh/uv/guides/integration/pytorch/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv PyTorch backend selection and GPU extensions

Goal: install PyTorch through the pip interface with the right accelerator, and add prebuilt GPU extension wheels.

## Method

### uv pip with an index

PyTorch's own pip command works with `pip3` swapped for `uv pip`:

```shell
$ uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Automatic backend selection

`--torch-backend=auto` or `UV_TORCH_BACKEND=auto`:

```shell
$ uv pip install torch --torch-backend=auto
$ UV_TORCH_BACKEND=auto uv pip install torch
```

uv queries the installed CUDA driver, AMD GPU versions and Intel GPU presence, then uses the most compatible PyTorch index for all relevant packages (`torch`, `torchvision`, etc.). With no GPU found it falls back to the CPU-only index. Existing index configuration for packages outside the PyTorch ecosystem is still respected.

Pick a specific backend with a value such as `cu130`:

```shell
$ uv pip install torch torchvision --torch-backend=cu130
$ UV_TORCH_BACKEND=cu130 uv pip install torch torchvision
```

`--torch-backend` is currently available only in the `uv pip` interface, not the project interface (`uv lock`, `uv sync`, `uv run`).

### GPU extensions (flash-attn and similar)

Packages with GPU extensions are compiled for a specific CUDA and PyTorch pair, and building from source needs the CUDA development toolkit. The Astral GPU indexes at `https://wheels.astral.sh/` publish prebuilt wheels for `flash-attn`, `deepspeed`, `deep-gemm`, `torch-scatter` and `vllm`.

```console
$ uv add flash-attn --index astral-cu128=https://wheels.astral.sh/simple/cu128/
```

This adds the dependency, configures the index and pins `flash-attn` to it. Equivalent configuration, with `explicit = true` so only pinned packages use the index:

```toml
[tool.uv.sources]
flash-attn = { index = "astral-cu128" }

[[tool.uv.index]]
name = "astral-cu128"
url = "https://wheels.astral.sh/simple/cu128/"
explicit = true
```

Each index targets one CUDA version and its wheels target specific PyTorch versions; a local version such as `+cu.12.8.torch.2.11` means CUDA 12.8 and PyTorch 2.11. Choose the index and wheel matching your Python version, platform, CUDA version and installed PyTorch.

## Verify

After the `uv add`, `pyproject.toml` contains the `[tool.uv.sources]` and `[[tool.uv.index]]` entries shown above.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/pytorch). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
