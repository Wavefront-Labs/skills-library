---
id: creative-arts.animation.blender.oneapi-setup
name: oneapi-setup
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, oneapi, oneapi-setup, intel-arc]
level: practitioner
status: docs-checked
description: "Enable Cycles oneAPI rendering on Intel Arc GPUs: supported hardware, minimum drivers on Windows and Linux, the Embree on GPU option, and headless device setup."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# oneapi-setup

Goal: Cycles on Intel Arc discrete GPUs.

## Requirements

- Windows or Linux and an Intel Arc graphics card with the Xe HPG architecture. The manual lists Arc A-Series and Arc B-Series.
- Minimum drivers from the manual: on Windows, Intel Graphics Driver XX.X.101.5518 (or newer); on Linux, the `intel-level-zero-gpu` package 1.3.27642, typically provided through `intel-compute-runtime` XX.XX.34666.3. Check the manual for the current numbers before pinning a driver.
- Hardware acceleration for ray tracing and denoising is supported, and GPU denoising works on all supported GPUs.

## Setup

Preferences > System > Cycles Render Devices > **oneAPI**, tick the Arc GPU. Render Properties > Device: GPU Compute.

**Embree on GPU** (same preferences section, oneAPI only, on by default in the source): enables hardware ray tracing on Intel GPUs for better overall performance. If you suspect it for artefacts, untick it and compare.

## Headless

`compute_device_type = "ONEAPI"` in a startup script, then `p.refresh_devices()` (same pattern as cuda-setup), or `blender -b f.blend -a -- --cycles-device ONEAPI`.

## Failures

- oneAPI is missing from Preferences: the driver or compute runtime is older than the minimum above, or the card is not an Arc GPU.
- When GPU memory fills, Blender uses system memory for CUDA, OptiX, HIP and Metal devices according to the manual; oneAPI is not in that list, so reduce scene memory (see gpu-out-of-memory).
- Path guiding is not supported on any GPU, and OSL on GPU is OptiX only.

## Verify

Render Properties > Device shows GPU Compute and the Arc device is ticked under Preferences > System.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) plus the Cycles add-on source (properties.py on main).
Confirmed: oneAPI needs Intel Arc with Xe HPG on Windows or Linux; A- and B-Series listed; minimum driver strings for both platforms; Embree on GPU is oneAPI only and default on; GPU denoising on all supported GPUs; `ONEAPI` is a valid `--cycles-device` value.
Removed as unconfirmed: Arc Pro and Data Center GPU models, the integrated-graphics statement, render-group and /dev/dri advice, Resizable BAR advice, intel_gpu_top, and the first-render kernel timing.
Method: documentation only; no commands were run.
