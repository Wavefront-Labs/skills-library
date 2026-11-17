---
id: creative-arts.animation.blender.qa-validation-script
name: qa-validation-script
category: creative-arts
field: animation
product: blender
tags: [blender, pipeline, automation, qa-validation-script, scene-validation, python]
level: practitioner
status: docs-checked
description: "Write pre-render and pre-publish validation scripts for Blender: missing files, naming, simplify left on, sample counts, unapplied scales, and failing CI or farm jobs properly."
sources:
  - https://docs.blender.org/api/current/bpy.types.BlendData.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# qa-validation-script

Goal: catch common mistakes automatically before they cost a night of rendering or a broken publish.

## Script skeleton

```python
import bpy, os, sys
errors, warns = [], []
sc = bpy.context.scene

# missing files
for img in bpy.data.images:
    if img.filepath and not img.packed_file:      # skips generated and packed images
        if not os.path.exists(bpy.path.abspath(img.filepath)): errors.append(f"missing image {img.filepath}")
for lib in bpy.data.libraries:
    if not os.path.exists(bpy.path.abspath(lib.filepath)): errors.append(f"missing library {lib.filepath}")
# render settings
if sc.render.use_simplify: errors.append("Simplify is on")
if sc.render.resolution_percentage != 100: errors.append("resolution % not 100")
if sc.render.use_border: errors.append("render region is on")
# assets
for ob in sc.objects:
    if ob.type == 'MESH' and any(abs(s - 1) > 1e-4 for s in ob.scale): warns.append(f"unapplied scale {ob.name}")
    if ob.name.endswith((".001", ".002")): warns.append(f"duplicate-style name {ob.name}")

for w in warns: print("WARN", w)
for e in errors: print("ERROR", e)
if errors: sys.exit(1)
```
## Running

```bash
blender -b shot.blend --python-exit-code 1 -P validate.py
```
`-P` runs the script file. `--python-exit-code <code>` (0-255; zero disables) sets the exit code used when a Python exception is raised in a script run from the command line, and the script's own `sys.exit(1)` returns non-zero too (practice), so CI, farm pre-tasks and publish tools can stop on it.

## What to check (pick per department)

Render: simplify, region, resolution, sample counts for the active render engine, output path relative and versioned, camera set, frame range. Assets: naming, applied transforms, no n-gons in game assets, UVs present, materials assigned. Animation: no keys outside range, rig in default pose at frame 0. Files: missing textures and libraries, absolute paths.

## Gotchas

- Keep checks fast; run heavy checks (evaluated mesh topology) only for publish (practice).
- Warnings that nobody reads become noise. Fail on what matters, warn sparingly.

## Verify

Break each rule in a test file on purpose and run the script: each problem is reported and the exit code is 1. A clean file exits 0.

## Checked

Blender 5.2 manual (command-line arguments) and Python API 5.2, read 2026-10-27.
- `-P` / `--python <filepath>` and `--python-exit-code <code>` semantics (range 0-255, only for scripts run from the command line, zero disables): manual command-line arguments page.
- `RenderSettings.use_simplify`, `resolution_percentage`, `use_border`, `engine`; `Image.filepath`, `Image.packed_file`; `Library.filepath`; `BlendData.images` and `libraries`; `bpy.path.abspath`: API 5.2.
- Removed as unconfirmed: the `Image.source` value set and the `scene.cycles.samples` check (Cycles properties are not listed in the API docs).

Method: documentation only; no commands were run.
