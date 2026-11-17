---
id: computing-software.ai-ml-engineering.vllm.quickstart-install
name: quickstart-install
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [quickstart, install, uv, download-kernels]
level: intro
status: docs-checked
description: "Install vLLM on NVIDIA CUDA with uv and set up the environment the quickstart recommends."
sources:
  - https://docs.vllm.ai/en/latest/getting_started/quickstart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a working vLLM install for offline batched inference or online serving.

Prerequisites from the quickstart: OS Linux, Python 3.11 to 3.14. macOS Apple Silicon is served by the separate vLLM-Metal project.

NVIDIA CUDA install with uv (recommended for fast environment management):

```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto
vllm download-kernels
```

`--torch-backend=auto` (or `UV_TORCH_BACKEND=auto`) lets uv pick the PyTorch index from the installed CUDA driver; pin one explicitly with `--torch-backend=cu126`. `vllm download-kernels` installs precompiled kernels that vLLM would otherwise download and compile at startup, which can add several minutes on Hopper and newer GPUs.

Run without a permanent environment: `uv run --with vllm vllm --help`. conda also works: create a Python 3.12 env, `pip install --upgrade uv`, then the same `uv pip install vllm --torch-backend=auto`.

Other hardware:
- AMD ROCm: `uv pip install vllm --extra-index-url https://wheels.vllm.ai/rocm/`. Currently Python 3.12, ROCm 7.0 and glibc 2.35 or newer. Nightly image: `vllm/vllm-openai-rocm:nightly`.
- Google TPU: `uv pip install vllm-tpu`.
- Intel GPU: XPU backend; official Docker images arrive from v0.26.0, nightly image `vllm/vllm-openai-xpu:nightly`.

The older `rocm/vllm-dev` image location is being deprecated in favour of vLLM's own release pipeline.

## Checked

2026-11-03. Confirmed against the Quickstart page (docs.vllm.ai/en/latest/): supported Python versions, uv install, download-kernels, ROCm, XPU and TPU notes.

Method: documentation only; no commands were run.
