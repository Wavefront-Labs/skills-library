---
id: computing-software.ai-ml-engineering.ml-platform-engineering.cuda-container-images-driver-compatibility
name: cuda-container-images-driver-compatibility
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, self-service, cuda-container-images, cuda-compatibility, nvidia-container-toolkit, reproducible-images]
level: practitioner
status: gated
description: "Build reproducible GPU images: host driver vs container CUDA compatibility, nvidia/cuda base/runtime/devel tags, PyTorch CUDA wheels, compute capability and pinning."
sources:
  - https://docs.nvidia.com/deploy/cuda-compatibility/
  - https://hub.docker.com/r/nvidia/cuda
  - https://pytorch.org/get-started/locally/
  - https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible GPU container images

## The compatibility rule
- The **kernel driver** lives on the host (installed with the node image or GPU Operator). The **CUDA runtime/toolkit and libraries** (cuDNN, NCCL, cuBLAS) live in the container.
- A container's CUDA version needs a host driver at least as new as that CUDA release requires. Minor-version compatibility allows a newer CUDA 12.x minor on an older 12.x driver for most features (PTX JIT excluded); forward compatibility to a newer major needs the `cuda-compat` package on supported datacenter GPUs. (gated: unconfirmed, source is paywalled or blocked)
- `nvidia-smi` on the host shows the driver version and the highest CUDA version it supports; that number is a ceiling, not what containers use.
- The NVIDIA Container Toolkit (or GPU Operator on Kubernetes) mounts the driver libraries into containers.

## Base images
`nvidia/cuda:<cuda>-<flavor>-<os>`:
- `base` - CUDA runtime only (minimal).
- `runtime` - adds CUDA math libraries (and `cudnn-runtime` variants with cuDNN). Use for serving/training images with prebuilt wheels.
- `devel` - compilers and headers (nvcc). Use only in a build stage for compiling extensions (flash-attention, custom ops), then copy artefacts into a runtime image.
NGC framework images (`nvcr.io/nvidia/pytorch:<yy.mm>-py3`) bundle tested framework + CUDA + NCCL combinations.

## PyTorch specifics
PyTorch wheels bundle their own CUDA libraries; pick the index matching your target:
```dockerfile
FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04 AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv && rm -rf /var/lib/apt/lists/*
COPY requirements.lock /tmp/
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir \
      --index-url https://download.pytorch.org/whl/cu128 torch==<pinned> && \
    /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.lock
```
With pip wheels, a slim `python` base plus the driver is often enough; the CUDA base mainly matters for non-PyTorch CUDA libraries and compiling.

## Compute capability
Newer GPUs need builds that include their architecture (Blackwell needs CUDA 12.8+ builds). "no kernel image is available for execution on the device" means the wheel/extension was not compiled for that GPU's `sm_XX`; set `TORCH_CUDA_ARCH_LIST` when compiling extensions.

## Reproducibility
- Pin base images by digest, Python packages with a lock file (uv/pip-tools), and record CUDA/cuDNN/NCCL versions as image labels.
- Rebuild regularly for security patches; test on each GPU type in the fleet.

## Verify
```bash
docker run --rm --gpus all IMAGE python -c "import torch;print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```
- [ ] Prints True and the expected device on every GPU node type; a small matmul runs.
- [ ] Host driver versions in the fleet meet the image's CUDA requirement (check before rollout).

## Checked

2026-11-02

- Confirmed: NVIDIA CUDA compatibility page, the nvidia/cuda Docker Hub page, PyTorch get-started page and the Container Toolkit index were fetched (short pages).
- Removed or gated: The fetched pages do not state the specific image tags, TORCH_CUDA_ARCH_LIST usage, error text or driver version thresholds used here; gated, confirm in the NVIDIA compatibility documentation.

Method: documentation only; no commands were run.
