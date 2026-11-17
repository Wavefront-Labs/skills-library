---
id: computing-software.ai-ml-engineering.ollama.gpu-nvidia-selection
name: gpu-nvidia-selection
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [nvidia, cuda, cuda-visible-devices, compute-capability]
level: practitioner
status: docs-checked
description: "Check NVIDIA support (compute capability 5.0+, driver 550+) and pin Ollama to GPUs with CUDA_VISIBLE_DEVICES."
sources:
  - https://docs.ollama.com/gpu.md
  - https://docs.ollama.com/troubleshooting.md
  - https://docs.ollama.com/windows.md
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run on the right NVIDIA GPU.

Requirements from the GPU page: compute capability 5.0 or higher and a recent driver, version 550 or newer (570 or newer for compute capability 5.0 to 6.2 cards). The Windows page asks for NVIDIA driver 551.61 or newer.

Select GPUs with `CUDA_VISIBLE_DEVICES` as a comma-separated list. Numeric IDs can change between boots, so the page recommends UUIDs, listed with:

```
nvidia-smi -L
```

```
CUDA_VISIBLE_DEVICES=GPU-xxxxxxxx-xxxx ollama serve
```

To ignore GPUs and force CPU, use an invalid ID such as `-1`.

Known Linux issue: after a suspend and resume cycle, Ollama can fail to discover the GPU and fall back to CPU. Reload the driver module:

```
sudo rmmod nvidia_uvm && sudo modprobe nvidia_uvm
```

In containers, the container runtime must be set up first (see the Docker skill); verify with `docker run --gpus all ubuntu nvidia-smi`.

Multi-GPU placement follows the FAQ: a model goes on one GPU if it fits entirely, otherwise it is spread across all available GPUs. Confirm what loaded with `ollama ps` (the Processor column) and the server log.

## Checked

2026-11-08. Compute capability and driver minimums, `CUDA_VISIBLE_DEVICES` with UUIDs and `-1`, and the suspend/resume fix against the GPU page (docs.ollama.com/gpu); the container check against the troubleshooting page; 551.61 against the Windows page; multi-GPU placement and `ollama ps` against the FAQ. Added "entirely" to the single-GPU rule per the FAQ. Nothing removed.

Method: documentation only; no commands were run.
