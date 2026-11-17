---
id: creative-arts.animation.blender.metal-setup
name: metal-setup
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, metal-gpu, metal-setup, apple-silicon, macos]
level: practitioner
status: docs-checked
description: "Render Cycles on macOS with Metal: Apple Silicon requirement, the MetalRT and kernel optimization preferences, memory behaviour, and headless device setup."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# metal-setup

Goal: GPU Cycles on Macs.

## Requirements

- An Apple Silicon Mac. The manual lists Metal GPU rendering for Apple Silicon only, and macOS 13.0 or newer to support all features. Ray tracing and denoising are GPU accelerated there.
- Preferences > System > Cycles Render Devices > **Metal**, tick the GPU. Render Properties > Device: GPU Compute.

## MetalRT

On Apple Silicon the preferences show a **MetalRT** setting with three values:

- Off: uses the BVH2 layout for intersection queries.
- On: use MetalRT for intersection queries.
- Auto (the default): automatically picks the fastest intersection method.

The manual says MetalRT uses less memory for scenes that use curves extensively and can give better performance in specific cases. Compare a representative frame with Off and Auto. The setting is only active when the device supports hardware ray tracing. A **Kernel Optimization** setting (Off, Intersection only, Full) also appears on Apple Silicon.

## Unified memory

Apple Silicon GPUs share system RAM with the CPU. Heavy scenes compete with the OS and Blender for the same pool. When GPU memory is full Blender tries to use system memory for Metal devices, which costs speed (watch Memory Pressure in Activity Monitor).

## Gotchas

- OSL on GPU is only supported with OptiX, so shaders that use Script nodes must stay on CPU on a Mac.
- Path guiding is not supported on any GPU.
- Background `blender -b` renders: set the device in a startup script (`compute_device_type = "METAL"`, then `refresh_devices()`), or pass `-- --cycles-device METAL`.

## Verify

Render Properties > Device shows GPU Compute and the Apple GPU is ticked in Preferences. Activity Monitor > Window > GPU History shows the load.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) plus the Cycles add-on source (properties.py on main).
Confirmed: Metal is for Apple Silicon with macOS 13.0 or newer for all features; MetalRT is Off/On/Auto with Auto default and the manual's description; the MetalRT and Kernel Optimization options are drawn only on arm64; OSL and path guiding limits; `METAL` is a valid `--cycles-device` value.
Removed as unconfirmed: AMD GPUs in Intel Macs, M3-only hardware ray tracing and the M1/M2 software path, first-render kernel compile time, Low Power Mode advice.
Method: documentation only; no commands were run.
