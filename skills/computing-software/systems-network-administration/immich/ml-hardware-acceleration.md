---
id: computing-software.systems-network-administration.immich.ml-hardware-acceleration
name: ml-hardware-acceleration
category: computing-software
field: systems-network-administration
product: immich
tags: [cuda, openvino, rocm, armnn, rknn, hwaccel-ml]
level: advanced
status: docs-checked
description: "Run Immich machine learning on a GPU or NPU: backends, prerequisites, image tag suffix, hwaccel.ml.yml extends and confirming use."
sources:
  - https://docs.immich.app/features/ml-hardware-acceleration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: accelerate Smart Search and facial recognition models on hardware.

Backends: ARM NN (Mali), CUDA (NVIDIA, compute capability 5.2 or higher), ROCm (AMD), OpenVINO (Intel GPUs) and RKNN (Rockchip RK3566, RK3568, RK3576, RK3588). Only Linux and Windows via WSL2 are supported, and the instructions are Docker Compose specific. CUDA is the most reliable.

Prerequisites: CUDA needs the official NVIDIA driver (version 545 or higher) and NVIDIA Container Toolkit on Linux except WSL2. ROCm needs the AMDGPU driver and at least 35GiB free disk for the image. ARM NN needs `/dev/mali0` and `libmali.so`.

Setup:

1. Download `hwaccel.ml.yml` from the latest release next to `docker-compose.yml`.
2. In `immich-machine-learning`, add `-armnn`, `-cuda`, `-rocm`, `-openvino` or `-rknn` to the end of the image tag, for example `${IMMICH_VERSION:-release}-cuda`.
3. Uncomment `extends` and change `cpu` to the backend (`openvino-wsl` on WSL2).
4. Redeploy `immich-machine-learning`.

Single compose file platforms such as Unraid inline the `deploy.resources.reservations.devices` block (driver `nvidia`, `count: 1`, capabilities `gpu`).

Confirm usage with `nvtop`, `intel_gpu_top` or `radeontop`, or look in the machine learning container logs for `Available ORT providers` when a Smart Search or Face Detection job starts.

No jobs need rerunning after enabling. Raising job concurrency raises utilisation and VRAM use; larger models benefit more. If a model errors, try another model.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/ml-hardware-acceleration in full. The backend service names (`armnn`, `cuda`, `rocm`, `openvino`, `openvino-wsl`, `rknn`) were also read from the `hwaccel.ml.yml` release asset.
Reworded: the ROCm disk figure, which the page gives as at least 35GiB.
Method: documentation only; no commands were run.
