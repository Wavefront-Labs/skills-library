---
id: computing-software.software-engineering.uv.uv-pytorch-indexes
name: uv-pytorch-indexes
category: computing-software
field: software-engineering
product: uv
tags: [uv, pytorch, cuda, cpu, explicit-index, tool-uv-sources, markers, extras, conflicts]
level: practitioner
status: docs-checked
description: "Configure uv projects to install CPU, CUDA, ROCm or Intel GPU PyTorch builds using explicit indexes, platform markers and conflicting extras."
sources: [https://docs.astral.sh/uv/guides/integration/pytorch/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv with PyTorch: indexes, markers and extras

Goal: pick the right PyTorch accelerator build per platform in a uv project (some features need uv 0.5.3 or later).

## Method

PyTorch encodes accelerators in the local version (for example `2.11.0+cpu`, `2.11.0+cu130`) and publishes each build to its own index such as `https://download.pytorch.org/whl/cpu` or `.../whl/cu130`. By default (`uv add torch torchvision`) PyPI is used: CPU wheels on Windows and macOS, CUDA-enabled wheels on Linux.

To force a variant everywhere, add an index and point the packages at it. Use `explicit = true` so the index serves only the packages that name it (not generic ones like `jinja2`):

```toml
[tool.uv.sources]
torch = [{ index = "pytorch-cpu" }]
torchvision = [{ index = "pytorch-cpu" }]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

Index URLs listed: cpu, cu118, cu126, cu128, cu130, rocm7.2, xpu (Intel GPUs), all under `https://download.pytorch.org/whl/`.

### Markers

No CUDA builds exist for macOS, so gate on `sys_platform`:

```toml
[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", marker = "sys_platform != 'linux'" },
  { index = "pytorch-cu130", marker = "sys_platform == 'linux'" },
]
```

Repeat for `torchvision` and define both indexes. ROCm (Linux only) also needs `pytorch-triton-rocm` and `triton-rocm` in dependencies, both with `; sys_platform == 'linux'` and sourced from the ROCm index. Intel GPU needs `triton-xpu` sourced from the xpu index.

### Extras

Choose by extra, for `uv sync --extra cpu` versus `uv sync --extra cu130`:

```toml
[project.optional-dependencies]
cpu = ["torch>=2.11.0", "torchvision>=0.26.0"]
cu130 = ["torch>=2.11.0", "torchvision>=0.26.0"]

[tool.uv]
conflicts = [[{ extra = "cpu" }, { extra = "cu130" }]]

[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", extra = "cpu" },
  { index = "pytorch-cu130", extra = "cu130" },
]
```

## Gotchas

- With the extras setup, enabling `cu130` fails to install on macOS because GPU builds are not available there.
- The `conflicts` table is what lets two extras request different `torch` builds.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/pytorch). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
