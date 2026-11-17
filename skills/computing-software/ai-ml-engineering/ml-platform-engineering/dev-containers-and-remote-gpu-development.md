---
id: computing-software.ai-ml-engineering.ml-platform-engineering.dev-containers-and-remote-gpu-development
name: dev-containers-and-remote-gpu-development
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, devcontainer-gpu, dev-containers, remote-development, cuda, reproducible-environments]
level: practitioner
status: docs-checked
description: "Give ML engineers reproducible GPU dev environments: devcontainer.json with the nvidia-cuda feature, hostRequirements.gpu, runArgs, lifecycle commands and cached volumes."
sources:
  - https://containers.dev/implementors/json_reference/
  - https://github.com/devcontainers/features/tree/main/src/nvidia-cuda
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dev containers and remote GPU development

**Goal:** every engineer gets the same CUDA, driver-compatible, framework-pinned environment on a remote GPU machine, opened from their editor in minutes.

## devcontainer.json
```json
{
  "name": "ml-dev",
  "build": {"dockerfile": "Dockerfile"},
  "runArgs": ["--gpus", "all", "--ipc=host"],
  "hostRequirements": {"gpu": "optional"},
  "mounts": [{"source": "hf-cache", "target": "/root/.cache/huggingface", "type": "volume"}],
  "containerEnv": {"HF_HOME": "/root/.cache/huggingface"},
  "postCreateCommand": "uv sync --frozen",
  "customizations": {"vscode": {"extensions": ["ms-python.python", "ms-toolsai.jupyter"]}}
}
```
- `runArgs` is an array of Docker CLI arguments used when running the container (default `[]`).
- `hostRequirements.gpu` accepts a boolean, the string `"optional"` (use a GPU when available, not required) or an object with `cores` and `memory`. `true` works on GPU machine types but fails on CPU-only hosts, so `"optional"` works in both cases.
- `mounts` takes Docker `--mount`-style values; use a named volume to cache model weights and datasets so rebuilds do not re-download.
- `postCreateCommand` runs once after creation (after `updateContentCommand`); `postStartCommand` runs every time the container starts. If one lifecycle script fails, later ones are skipped.
- Alternative to a CUDA base image: the `ghcr.io/devcontainers/features/nvidia-cuda:2` feature installs CUDA shared libraries; options include `installCudnn`, `installCudnnDev`, `installNvtx`, `installToolkit`, `cudaVersion` and `cudnnVersion`. It works on Debian/Ubuntu-based images with `apt` and is only useful on a host with an NVIDIA GPU.
- GPU access needs the NVIDIA driver and the NVIDIA Container Toolkit installed on the host. Inside the container, run `nvidia-smi` to check the GPU is visible.
- Pin the base image by digest and install from a lockfile for reproducibility.

## Remote GPU hosts
- The editor connects over SSH to a GPU VM and opens the folder in the dev container on that host.
- Use SSH certificates or an identity-aware proxy instead of shared keys; no public SSH on GPU hosts.

## Driver compatibility
The host driver must support the container's CUDA version. Check with `nvidia-smi` inside the container on first start; a check can be put in `postStartCommand`.

## Same image for CI and training
Build the dev image from the same base and lockfile as the training image so "works in my container" means it works in the job.

## Verify
- [ ] `python -c "import torch; print(torch.cuda.is_available())"` is True in the container.
- [ ] A fresh engineer gets a working environment from the repo alone.
- [ ] Idle remote GPU workspaces stop automatically.

## Checked
2026-11-01. Confirmed on the dev container JSON reference and the nvidia-cuda feature README: `runArgs`, `hostRequirements.gpu` (boolean, `"optional"`, object), `mounts`, `containerEnv`, `customizations`, `postCreateCommand`/`postStartCommand` semantics, the feature id and options, OS support, the Container Toolkit and `nvidia-smi` guidance. Removed (not confirmed): the Docker 64 MB shared-memory default and `--shm-size` advice, `--ulimit memlock`, a pinned CUDA image tag, Coder/DevPod and `devcontainer up` claims, VS Code Remote-SSH/JetBrains names.
Method: documentation only; no commands were run.
