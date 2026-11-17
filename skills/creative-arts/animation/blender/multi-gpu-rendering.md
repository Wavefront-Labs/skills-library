---
id: creative-arts.animation.blender.multi-gpu-rendering
name: multi-gpu-rendering
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, multi-gpu, device-selection, cuda-visible-devices, cycles, render-farm]
level: practitioner
status: docs-checked
description: "Use several GPUs for Cycles: device selection in preferences, memory not pooled except over NVLink, one process per GPU for animation, and device selection by env var or script."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/environment-variables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# multi-gpu-rendering

Goal: get the most out of a machine with several GPUs.

## Single frame across GPUs

Preferences > System > Cycles Render Devices: tick every GPU of one backend, and set Render Properties > Device to GPU Compute. The manual says multiple GPUs can be used by configuring them in the Compute Device panel.

**Memory is not pooled**: typically each GPU can only access its own memory, so every GPU holds the scene and the smallest card sets the limit. The exception is NVIDIA GPUs connected with NVLink: tick **Distribute Memory Across Devices** in the same preferences section (only available when the GPUs are linked by a high-bandwidth protocol; NVLink is the only one currently supported). It costs a small amount of speed.

## Animation: one process per GPU

For sequences you can run one Blender per GPU, each rendering different frames, and restrict each process to its card with the vendor's visibility variable. For NVIDIA, `CUDA_VISIBLE_DEVICES` is documented in NVIDIA's CUDA environment variables page.

```bash
CUDA_VISIBLE_DEVICES=0 blender -b shot.blend -s 1 -e 50 -a -- --cycles-device OPTIX &
CUDA_VISIBLE_DEVICES=1 blender -b shot.blend -s 51 -e 100 -a -- --cycles-device OPTIX &
```
The manual's "primitive render farm" alternative: give every process the full range, disable **Overwrite** and enable **Placeholders** in the Render Properties > Output panel, so each process claims the next frame that has no file yet.

To pick devices by name instead, use a startup script:
```python
import bpy
p = bpy.context.preferences.addons["cycles"].preferences
p.compute_device_type = "OPTIX"
p.refresh_devices()
for d in p.devices:
    d.use = (d.id == wanted_id)
```
Print `d.id` and `d.name` first to find the id of each card.

## Gotchas

- System RAM: each process holds its own copy of the scene, so N processes need N times the host memory.
- Mixed GPU models in one frame: the slowest card can hold back the finish of the frame (a general scheduling effect, measure it on your own scenes).

## Verify

A vendor monitor such as `nvidia-smi` shows each GPU busy while its process renders, and each frame number appears exactly once in the output folder.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST), Cycles add-on source (properties.py on main), NVIDIA CUDA environment variables page.
Confirmed: multi-GPU selection in Preferences; memory not pooled except NVLink via Distribute Memory Across Devices; the Overwrite-off plus Placeholders farm recipe; `CUDA_VISIBLE_DEVICES` exists in NVIDIA docs; `-s`, `-e`, `-a` and `--cycles-device` options; device entries have `id`, `name`, `use`.
Removed as unconfirmed: near-linear scaling claim, poor scaling on light frames, `HIP_VISIBLE_DEVICES`, PCIe riser effects.
Method: documentation only; no commands were run.
