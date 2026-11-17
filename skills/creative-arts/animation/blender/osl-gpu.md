---
id: creative-arts.animation.blender.osl-gpu
name: osl-gpu
category: creative-arts
field: animation
product: blender
tags: [blender, osl-gpu, osl-optix, osl, optix, cycles, gpu-rendering]
level: advanced
status: docs-checked
description: "Render OSL shaders on the GPU with Cycles OptiX: requirements, enabling, and the documented limitations (noise types, texture lookups, trace) and when to fall back to CPU."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
  - https://developer.blender.org/docs/release_notes/3.5/cycles/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-gpu

Goal: use OSL scripts without giving up GPU render speed.

## Requirements

- OSL on the GPU needs the **OptiX** backend: the manual states OSL is not supported with GPU rendering unless using OptiX. The Blender 3.5 Cycles release notes introduced OSL on OptiX.
- Select OptiX in the *Cycles Render Devices* preference, enable the available devices, set the scene Device to *GPU Compute* (the manual's GPU Rendering steps), and enable *Open Shading Language* in the Render Properties.

## Limitations (5.2 manual)

- Texture lookups require OSL to be able to determine a constant image file path for each texture call.
- Some noise functions are not available, for example *Cell*, *Simplex* and *Gabor*.
- The `trace` function is not functional, so the Ambient Occlusion and Bevel nodes do not work with OSL on OptiX.

Test each script on the target device; when output differs from CPU, render that shot on CPU.

## Gotchas

- Mixed farm devices (some OptiX, some CPU) must all handle the script's features or frames mismatch.
- The Script node is only evaluated when Open Shading Language is enabled, on any device.
- Rendering on OptiX is a different code path from CPU, so compare a frame from each before committing a farm job.

## Verify

Render the same frame on CPU and on OptiX with OSL on and compare them (for example with a difference blend in the compositor); the render log shows which device was used.

## Checked

2026-10-27 against the Blender 5.2 manual (Cycles > Open Shading Language, Limitations) and the Blender 3.5 Cycles release notes. Confirmed OptiX-only GPU support and the three listed limitations. Removed unconfirmed claims (CUDA/HIP/Metal/oneAPI behaviour, RTX requirement, JIT compile times and cache behaviour, performance remarks, driver cache invalidation). Method: documentation only; no commands were run.
