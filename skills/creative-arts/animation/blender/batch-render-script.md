---
id: creative-arts.animation.blender.batch-render-script
name: batch-render-script
category: creative-arts
field: animation
product: blender
tags: [blender, pipeline, automation, batch, batch-render-script, batch-render, command-line]
level: practitioner
status: docs-checked
description: "Render many shots, files or cameras in one batch: per-file background processes, looping cameras and view layers in one file, output naming, logging and resuming."
sources:
  - https://docs.blender.org/api/current/bpy.ops.render.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# batch-render-script

Goal: unattended rendering of lots of work (turntables for every asset, every camera of a set, every shot of a sequence).

## Many files: one Blender process per file

Separate processes avoid leftover state between files:
```bash
for f in shots/*.blend; do
  blender -b "$f" --python-exit-code 1 -P setup_render.py -a -- --preset final || echo "FAILED $f" >> failed.txt
done
```

## Many cameras in one file

```python
import bpy
sc = bpy.context.scene
base = "//../render/cams/"
for cam in [o for o in sc.objects if o.type == 'CAMERA']:
    sc.camera = cam
    sc.render.filepath = f"{base}{cam.name}/{cam.name}_"
    bpy.ops.render.render(animation=True)      # or write_still=True for one frame
```
Run with `blender -b set.blend -P render_cams.py` (no `-a`, the script renders).

## Variants: view layers, collections, materials

Toggle `view_layer.use` (enable or disable rendering of a View Layer) for layers, `layer_collection.exclude` per layer, or swap materials per pass in the loop, then render. Restore the original state at the end if the file is saved afterwards (or don't save).

## Robustness

- Output paths per item with `#` padding, versioned folders.
- Set `scene.render.use_overwrite = False` (default True) and `scene.render.use_placeholder = True` (default False; creates empty placeholder files while rendering) so a restarted batch skips finished frames (see frame-step-overwrite-placeholders).
- Log each item's start, end and time to a file, and check files on disk. `bpy.app.handlers.render_post`, `render_complete` and `render_cancel` handlers receive the scene for logging.
- Wrap each file in a timeout in the outer script (see subprocess-blender).

## Gotchas

- For long batches prefer one process per file so each job starts from a clean state.
- Use the render handlers above for per-frame logging.

## Verify

After the batch, a check script counts frames per item against the expected frame range and lists anything missing.

## Checked

2026-10-27 against the Blender 5.2 Python API (RenderSettings.use_overwrite and use_placeholder defaults, ViewLayer.use, LayerCollection.exclude, bpy.app.handlers render_post/render_complete/render_cancel, bpy.ops.render.render arguments) and the 5.2 manual command line arguments page. Removed unconfirmed claims (memory growth, blocking, log line text). Method: documentation only; no commands were run.
