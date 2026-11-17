---
id: creative-arts.animation.blender.cuda-setup
name: cuda-setup
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, cuda, cuda-setup, cuda-driver, nvidia]
level: practitioner
status: docs-checked
description: "Enable Cycles CUDA rendering on NVIDIA: compute-capability and driver needs, preferences device setup, headless enabling via Python and CLI, and common failures."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# cuda-setup

Goal: Cycles rendering on an NVIDIA GPU with the CUDA backend, interactively and on a headless render node.

## Requirements

- Windows or Linux, and an NVIDIA GPU with compute capability 5.0 or higher (the manual links NVIDIA's list of cards and their compute capabilities).
- Official drivers from the GPU vendor's site (or the Linux package manager). The manual warns that drivers supplied by the computer maker can be outdated or incomplete.
- Blender ships precompiled CUDA kernels, so normally no CUDA toolkit install is needed.

## Interactive setup

Edit > Preferences > System > Cycles Render Devices > **CUDA**, tick the GPU(s). Then Render Properties > Device: **GPU Compute**. For RTX cards, OptiX is the usual choice (see optix-setup); CUDA is the fallback when OptiX is unavailable or you are isolating an OptiX-specific problem.

## Headless (render nodes)

Preferences are per user and not in the .blend, so set them in a startup script:
```python
import bpy
p = bpy.context.preferences.addons["cycles"].preferences
p.compute_device_type = "CUDA"
p.refresh_devices()
for d in p.devices:
    d.use = d.type == "CUDA"
    print(d.name, d.type, d.use)
bpy.context.scene.cycles.device = "GPU"
```
`blender -b shot.blend -P enable_cuda.py -a`. Or set the device for one run: `blender -b shot.blend -a -- --cycles-device CUDA` (valid values: CPU, CUDA, OPTIX, HIP, ONEAPI, METAL; append +CPU to add the CPU). Older scripts call `get_devices()`, which is deprecated in favour of `refresh_devices()`.

## Failures

- CUDA is missing from Preferences: the card or driver is not supported by this Blender version. Install the vendor's official driver and check the compute capability.
- Windows ends a long GPU kernel when the same GPU also drives the display (the manual's "lost connection with the display driver" case). Use a separate GPU for display, or increase the Windows timeout (Microsoft's timeout detection and recovery page), which makes the interface less responsive.
- "CUDA Error: Kernel compilation failed" on a very new card: try the latest official or daily Blender build, or a newer CUDA toolkit if you build Blender yourself.
- Renders on CPU anyway: the scene's Device is still CPU. Check `scene.cycles.device`.

## Verify

Render Properties > Device shows GPU Compute, and the CUDA device is ticked under Preferences > System. A vendor tool such as `nvidia-smi` can show the GPU busy during a render.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) plus the Cycles add-on source (properties.py on main).
Confirmed: CUDA needs compute capability 5.0 or higher on Windows and Linux; precompiled kernels need no toolkit; Preferences > System > Cycles Render Devices entries and the GPU Compute device; `--cycles-device` values and +CPU; `refresh_devices()` exists and `get_devices()` is marked deprecated in source; display-timeout and kernel-compilation advice from the GPU Rendering FAQ.
Removed as unconfirmed: the exact CUDA timeout message text and the TdrDelay registry value.
Method: documentation only; no commands were run.
