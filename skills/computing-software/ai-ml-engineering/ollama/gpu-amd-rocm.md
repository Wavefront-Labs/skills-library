---
id: computing-software.ai-ml-engineering.ollama.gpu-amd-rocm
name: gpu-amd-rocm
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [amd, rocm, hsa-override-gfx-version, rocr-visible-devices]
level: advanced
status: docs-checked
description: "Use AMD Radeon GPUs with ROCm v7, select devices with ROCR_VISIBLE_DEVICES and override an unsupported gfx target."
sources:
  - https://docs.ollama.com/gpu.md
  - https://docs.ollama.com/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run on AMD GPUs and handle unsupported cards.

Ollama supports AMD GPUs through ROCm v7 on Linux and Windows; the GPU page lists the supported Radeon and Instinct cards per platform. A driver older than ROCm 7 (ROCm 6.x or earlier) makes GPU discovery time out after 30 seconds and Ollama falls back to CPU, per the troubleshooting page, which says to upgrade with AMD's `amdgpu-install` utility.

Select devices with `ROCR_VISIBLE_DEVICES`, a comma-separated list of GPU IDs.

For a card not on the list, a close supported target can be forced with `HSA_OVERRIDE_GFX_VERSION=x.y.z`, for example `HSA_OVERRIDE_GFX_VERSION="10.3.0"`. For mixed GPUs set it per device with a suffix: `HSA_OVERRIDE_GFX_VERSION_0=10.3.0` and `HSA_OVERRIDE_GFX_VERSION_1=11.0.0`.

Container and permission notes:

- Linux AMD needs access to `/dev/kfd`; the user running Ollama must be in the groups that own it (`video`, `render`), or pass `--group-add` to Docker.
- On SELinux systems allow container device access with `setsebool container_use_devices=1`.
- `AMD_LOG_LEVEL=3` enables info logging in the HIP/ROCm libraries for more detailed error codes.

On Windows, Radeon defaults to one loaded model, and Vulkan is the fallback for RDNA2.

## Checked

2026-11-03. ROCm v7, `ROCR_VISIBLE_DEVICES`, `HSA_OVERRIDE_GFX_VERSION` forms and `setsebool` against the GPU page (docs.ollama.com/gpu); `/dev/kfd` groups, `AMD_LOG_LEVEL=3` and the 30s discovery timeout log line against the troubleshooting page (docs.ollama.com/troubleshooting); Windows Radeon default against the FAQ (docs.ollama.com/faq). Nothing removed.

Method: documentation only; no commands were run.
