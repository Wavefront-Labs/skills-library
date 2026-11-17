---
id: computing-software.systems-network-administration.immich.ml-multi-gpu
name: ml-multi-gpu
category: computing-software
field: systems-network-administration
product: immich
tags: [multi-gpu, device-ids, machine-learning-workers, concurrency, vram]
level: advanced
status: docs-checked
description: "Spread Immich machine learning across NVIDIA or Intel GPUs with MACHINE_LEARNING_DEVICE_IDS and MACHINE_LEARNING_WORKERS, or pin a device."
sources:
  - https://docs.immich.app/features/ml-hardware-acceleration
  - https://docs.immich.app/install/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use more than one GPU, or choose which GPU Immich uses.

Set two variables in `.env` for the machine learning container, for devices 0 and 1:

```
MACHINE_LEARNING_DEVICE_IDS=0,1
MACHINE_LEARNING_WORKERS=2
```

The service spawns two worker processes. One allocates models on device 0 and the other on device 1. Incoming requests go to whichever worker handles them. Set `MACHINE_LEARNING_WORKERS` to the number of listed devices.

Multi-GPU applies to NVIDIA or Intel GPUs per the docs. The default for `MACHINE_LEARNING_DEVICE_IDS` is `0`.

Pinning a single device works the same way:

```
MACHINE_LEARNING_DEVICE_IDS=1
```

This guarantees device 1 is always used instead of device 0.

Constraints and tips:

- Every GPU must be able to load all models. A single model cannot be split across GPUs.
- Raise job concurrencies in Administration, Settings, Job Settings so work is spread across devices and utilisation rises. Higher concurrency also increases VRAM use.

These variables belong to the hardware acceleration setup, so configure the image tag suffix and `extends` first. Each worker process duplicates models in memory, so extra workers need spare memory. For RKNN devices the docs describe `MACHINE_LEARNING_RKNN_THREADS` instead.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/ml-hardware-acceleration in full (Multi-GPU, Tips) and the Machine Learning table with its footnotes in install/environment-variables.
Removed: the claim that RKNN must keep one worker, and the claim that the variables have no effect without the acceleration setup; neither is stated.
Method: documentation only; no commands were run.
