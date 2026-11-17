---
id: computing-software.ai-ml-engineering.ollama.gpu-vulkan-and-metal
name: gpu-vulkan-and-metal
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [vulkan, metal, ggml-vk-visible-devices, setcap, ollama-vulkan]
level: advanced
status: docs-checked
description: "Understand Metal on Apple devices and the Vulkan backend: setcap for VRAM data, GGML_VK_VISIBLE_DEVICES and OLLAMA_VULKAN=0."
sources:
  - https://docs.ollama.com/gpu.md
  - https://docs.ollama.com/docker.md
  - https://docs.ollama.com/windows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use or disable the Vulkan backend.

Apple devices get GPU acceleration through the Metal API.

Vulkan provides additional GPU support on Windows and Linux and is enabled by default when the backend is installed (the Docker image bundles it too, and it is used when the container can access the GPU devices). On Windows most vendor drivers bundle Vulkan; most Linux distributions need extra components. Documented controls:

- `OLLAMA_VULKAN=0` disables the Vulkan backend.
- `GGML_VK_VISIBLE_DEVICES` takes one or more numeric IDs to select Vulkan devices; `GGML_VK_VISIBLE_DEVICES=-1` disables all Vulkan GPUs. On mixed iGPU/dGPU systems with an unstable iGPU, keep Vulkan on and set it to the discrete GPU index, for example `1` when `Vulkan1` is the discrete GPU.
- Ollama's scheduler uses available-VRAM data from the GPU libraries. Vulkan exposes that data only with extra capabilities or when running as root; otherwise Ollama uses approximate model sizes for best-effort scheduling. Grant the capability with:

```
sudo setcap cap_perfmon+ep /usr/local/bin/ollama
```

- For AMD GPUs on some Linux distributions you may need to add the `ollama` user to the `render` group.

Windows: the Windows page says Vulkan is enabled by default and is the recommended fallback for some RDNA2 / Radeon RX 6000 systems that do not expose ROCm v7; the ROCm stack for standalone installs is a separate `ollama-windows-amd64-rocm.zip`.

In Docker, the `ollama/ollama` image with `--device /dev/kfd --device /dev/dri` uses Vulkan; the `rocm` tag is the AMD ROCm image. Full recipes are in the Docker skill.

## Checked

2026-11-08. Metal, Vulkan default, `OLLAMA_VULKAN`, `GGML_VK_VISIBLE_DEVICES`, setcap and VRAM data, and the render group against the GPU page (docs.ollama.com/gpu); Docker bundling and device flags against the Docker page; the RDNA2 note and ROCm zip against the Windows page. Changed "Metal on Apple silicon" to "Apple devices" per the page, rewrote the "extra privilege" claim to the page's actual statement about VRAM data, and reworded the Windows line.

Method: documentation only; no commands were run.
