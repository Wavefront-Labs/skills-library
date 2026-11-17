---
id: creative-arts.animation.blender.optix-setup
name: optix-setup
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, optix, optix-setup, optix-denoiser-gpu, nvidia]
level: practitioner
status: docs-checked
description: "Set up Cycles OptiX on NVIDIA: device choice vs CUDA, driver minimum, hardware ray tracing, the OptiX denoiser choice, OSL support, and memory behaviour to watch."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# optix-setup

Goal: use NVIDIA RTX hardware ray tracing for Cycles renders on NVIDIA GPUs.

## Setup

Preferences > System > Cycles Render Devices > **OptiX**, tick the GPU(s). Render Properties > Device: GPU Compute.

Requirements from the manual: Windows or Linux, an NVIDIA card with compute capability 5.0 or higher, and a driver version of at least 575. OptiX uses the hardware ray-tracing acceleration of RTX cards.

## What OptiX adds

- Hardware ray-tracing acceleration on RTX cards.
- **OptiX denoiser** (Render Properties > Sampling > Denoising > Denoiser: OptiX). The manual says Automatic prefers OpenImageDenoise over OptiX, and that OptiX is mainly useful for GPU acceleration on some older NVIDIA GPUs where OpenImageDenoise cannot run on the GPU. GPU acceleration for OpenImageDenoise needs compute capability 7.0 or higher (all RTX cards).
- **OSL on GPU**: per the manual, Open Shading Language is only supported on GPU with OptiX, with limitations listed on the OSL page. CUDA does not support OSL.

## Watch out for

- Path guiding is not supported on any GPU (CPU only).
- If the GPU runs out of memory, Blender falls back to system memory for CUDA, OptiX, HIP and Metal devices, with a speed cost. See gpu-out-of-memory.
- When mixing machines or backends in one shot, render the whole shot on one backend, because noise patterns and tiny numeric differences between backends can show at cuts. This is a pipeline precaution, not a manual statement.

## Headless

`blender -b shot.blend -a -- --cycles-device OPTIX`, or set `compute_device_type = "OPTIX"` in a startup script (same pattern as cuda-setup, using `refresh_devices()`). Append `+CPU` (`OPTIX+CPU`) to include the CPU.

## Verify

Render Properties > Device shows GPU Compute, the OptiX device is ticked in Preferences, and the Denoiser dropdown offers OptiX.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: OptiX needs Windows or Linux, compute capability 5.0+, driver 575 or newer; OpenImageDenoise GPU acceleration needs compute capability 7.0+; OSL on GPU is OptiX only; path guiding not on GPU; Denoiser choices (Automatic, OpenImageDenoise, OptiX) and the Automatic preference; `--cycles-device OPTIX` and +CPU.
Removed as unconfirmed: the 30 to 80 percent speed-up figure, the claim that OptiX uses more VRAM than CUDA, the first-render kernel compile time, the "Cycles 3.5+" gate for OSL, and "OptiX denoiser is ideal for the viewport".
Method: documentation only; no commands were run.
