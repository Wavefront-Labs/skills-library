---
id: creative-arts.animation.blender.hip-setup
name: hip-setup
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, hip, hip-setup, hip-rt, amd, radeon]
level: practitioner
status: docs-checked
description: "Enable Cycles HIP rendering on AMD Radeon: supported GPU generations, minimum drivers, the HIP RT hardware ray tracing option, and command-line device choice."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hip-setup

Goal: Cycles on AMD GPUs with HIP, plus hardware ray tracing with HIP RT where supported.

## Requirements

- HIP is supported on Windows and Linux and needs an AMD card with the RDNA1 architecture or newer; discrete GPUs and APUs are both supported. The manual lists Radeon RX 5000, 6000 (and Pro W6000), 7000 (and Pro W7000) and 9000 series. Check the manual's GPU Rendering page for the list in your Blender version.
- Minimum drivers in the current manual: Windows, Radeon Software 24.9.1 or Radeon PRO Software 24.Q4; Linux, Radeon Software 24.30 or ROCm HIP Runtime 6.3. Re-read the page for your version, these numbers move.
- The manual advises installing official drivers from the GPU maker (or the Linux package manager), because computer-maker drivers can be outdated or incomplete.

## Setup

1. Preferences > System > Cycles Render Devices: select *HIP* and enable the available GPU(s).
2. In each scene, set Render Properties > Device to *GPU Compute*.

**HIP RT** (preferences, HIP devices only): speeds up rendering by enabling AMD hardware ray tracing on RDNA2 and above (the GPU page says Radeon RX 6000 and newer, with recent drivers). Compare speed and correctness against HIP without it. Shadow Caustics are not supported when using HIP without hardware ray tracing.

GPU-accelerated denoising: discrete Radeon RX 6000 and newer on Linux, discrete RX 7000 and newer on Windows.

## Command line

```
blender -b file.blend -f 20 -- --cycles-device HIP
```
Cycles options go after a double dash. Valid devices: CPU, CUDA, OPTIX, HIP, ONEAPI, METAL; append +CPU to a GPU device to render on CPU and GPU together.

## Limits and failures

- Path Guiding is not supported on any GPU. OSL is supported only for OptiX.
- If the GPU runs out of memory, CUDA, OptiX, HIP and Metal devices try to fall back to system memory, which costs speed but is usually still faster than CPU. Smaller textures cut GPU memory use.
- A card that is also driving the display can make Blender unresponsive while rendering; the only complete fix the manual gives is a separate GPU for display.
- HIP missing from the preferences: check the card generation and driver version against the manual.

## Verify

Render with Device set to GPU Compute and the HIP GPU enabled; confirm the GPU shows compute load in the operating system's GPU monitor.

## Checked

2026-11-09. Confirmed against the Blender manual GPU Rendering page (raw RST, read in full), the Preferences System page (HIP and HIP RT entries, grep read) and the command-line arguments page (`--cycles-device` entry, grep read). Removed: the Python headless snippet, Linux `render`/`video` group advice, first-render kernel compile claim, integrated-graphics advice, `rocm-smi` and the "3.6+" version gate (none on the checked pages).
Method: documentation only; no commands were run.
