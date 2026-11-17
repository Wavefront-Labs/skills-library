---
id: creative-arts.animation.blender.bpy-render-api
name: bpy-render-api
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-render-api, render-api, bpy-render, render-settings, cycles-python, write-still]
level: practitioner
status: verified
description: "Configure and run renders from Python: engine, resolution, samples, GPU device preferences, output format, render.render for stills and animation, and saving Render Result."
sources:
  - https://docs.blender.org/api/current/bpy.types.RenderSettings.html
  - https://docs.blender.org/api/current/bpy.ops.render.html
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-render-api

Goal: script a render that produces the same image every time, independent of whatever the .blend was saved with.

## Settings

```python
import bpy
sc = bpy.context.scene
r = sc.render
r.engine = 'CYCLES'                 # or 'BLENDER_WORKBENCH'; EEVEE is 'BLENDER_EEVEE' in 5.2 but 'BLENDER_EEVEE_NEXT' in 4.2-4.5 (setting 'BLENDER_EEVEE' fails in 4.5.14)
r.resolution_x, r.resolution_y, r.resolution_percentage = 1920, 1080, 100
r.fps = 24
sc.frame_start, sc.frame_end = 1, 120
r.filepath = "//render/shot010_####"     # #### becomes the zero-padded frame
r.image_settings.file_format = 'OPEN_EXR'
r.image_settings.color_depth = '16'              # default '8' for PNG; switching to OPEN_EXR gave '32' in 4.5.14
r.use_file_extension = True
sc.cycles.samples = 256
sc.cycles.use_denoising = True
sc.camera = bpy.data.objects["CAM_main"]
```

Find a property's identifier with Python Tooltips or the API docs page for `RenderSettings`/`CyclesRenderSettings`; enum values are the uppercase identifiers, not the UI labels.

## GPU device (preferences, not the scene)

```python
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = 'OPTIX'      # 'CUDA', 'HIP', 'METAL', 'ONEAPI'
prefs.refresh_devices()                  # refresh the device list (get_devices() is deprecated)
for d in prefs.devices:
    d.use = d.type != 'CPU'
sc.cycles.device = 'GPU'
```

The device list is not refreshed automatically on startup (unstable drivers can crash), so refresh it in the script and enable the devices you want.

## Render

```python
bpy.ops.render.render(write_still=True)             # still -> r.filepath
bpy.ops.render.render(animation=True)               # frame range -> r.filepath with frame numbers
bpy.data.images["Render Result"].save_render("//render/still.png")   # saves using a scene's render settings
```

`bpy.ops.render.render` takes `animation`, `write_still`, `use_viewport`, `layer` and `scene`. Blender 4.5.14 lists exactly these; the 5.2 API page also lists `frame_start` and `frame_end`, not run here, so set `sc.frame_start` / `sc.frame_end` instead. Single frame of an animation: set `sc.frame_set(f)` then `render(write_still=True)` with a frame-specific filepath.

## Gotchas

- Relative `//` paths resolve against the .blend location; an unsaved file has no `//` (4.5.14: `bpy.path.abspath("//render")` stayed relative, `render`). Use absolute paths in automation.
- `save_render(filepath, scene=None, quality=0)` takes its image parameters from the scene's render settings.
- EEVEE and Workbench engines are flagged as needing a GPU context (`RE_USE_GPU_CONTEXT` in the engine source); check that your headless host provides one.

## Verify

Print `r.engine, r.resolution_x, sc.cycles.samples, sc.cycles.device` before rendering; check the output file exists and has the expected resolution.

## Checked

2026-10-27 against the Blender 5.2 Python API (RenderSettings.engine, use_overwrite, ImageFormatSettings.color_depth default '8', bpy.ops.render.render arguments, Image.save_render signature) and 5.2 sources (Cycles add-on properties: samples, device, use_denoising, compute_device_type values, refresh_devices with get_devices deprecated; EEVEE and Workbench engine ids and GPU-context flag). Corrected the EEVEE identifier and the device refresh call; removed unconfirmed claims (silent CPU fallback, EGL, blocking remark). Run check, 2026-11-01, Blender 4.5.14 LTS headless: the Settings block ran (engine, resolution, percentage 50 of 200x100 rendered 100x50, fps, frame range, EXR depth); animation=True with one frame wrote seq_0003.png for a `####` path; `refresh_devices()` ran and listed the CPU and a HIP GPU (`get_devices()` also still exists in 4.5.14); `Image.save_render(filepath, scene, quality)` signature. Errors found: the 'BLENDER_EEVEE' id and the frame_start/frame_end operator arguments do not hold in 4.5.14. Unrun: 5.2-only behaviour, GPU context remark, headless-host advice, OPTIX/CUDA/METAL/ONEAPI device types.

Method: documentation checked against the 5.2 API pages; the code was run headless in Blender 4.5.14.
