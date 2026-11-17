---
id: creative-arts.animation.blender.line-art-baking-performance
name: line-art-baking-performance
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-baking, bake-line-art, line-art-performance, line-art-cache]
level: practitioner
status: docs-checked
description: "Bake Line Art to editable strokes and speed it up: bake all/selected, clear bakes, cached calculation, chaining thresholds, image boundary trim, crease filters."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html#bake
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-baking-performance

Goal: a responsive viewport while animating, and baked strokes for final frames.

## Baking (Line Art modifier, Bake panel)

- **Bake Line Art**: bakes the active Grease Pencil object over the scene start/end frame range; baked Line Art modifiers are deactivated automatically.
- **Bake All**: bakes every Grease Pencil object that has at least one Line Art modifier.
- **Clear Baked Line Art** (active object) and **Clear All**. Warning from the manual: clearing also removes anything drawn by hand in the frame range where Line Art runs.
- **Continue without Clearing**: re-activates one Line Art modifier without clearing baked strokes, for working on portions of the frames separately.

## Performance levers

- Each Line Art modifier runs the whole occlusion calculation itself (no global cache), so several Line Art modifiers make evaluation much slower.
- **Use Cache**: reuses the scene data of the first Line Art modifier in the stack. Only available on a second or later Line Art modifier in the same stack, and some settings become unavailable.
- **Force Backface Culling** removes back faces to speed up calculation (it changes which occlusion levels edges get).
- **Overscan** adds a margin outside the camera view so strokes do not end abruptly at the image edge; **Image Boundary Trimming** trims strokes exactly at the image boundary (including the overscan region).
- **Chaining**: *Image Threshold* (chain short segments whose 2D distance is within the threshold), *Smooth Tolerance*, *Geometry Space* (chain by geometry distance instead of image space), *Loose Edges as Contour*, *Preserve Details* (off gives a smoother result).
- *Instanced Objects* has a performance impact with many instances; leave it off unless needed.
- Object/collection *Usage* (Include, Occlusion Only, Exclude, Intersection Only...) controls what is loaded; the manual notes Line Art still loads the whole visible scene for correct occlusion unless Usage says otherwise.

## Verify

Compare playback speed with and without Use Cache, and check that baked frames contain strokes after the modifier deactivates.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier page and Object Properties Line Art page). Confirmed Bake panel buttons and behaviour, Use Cache conditions, Overscan, Image Boundary Trimming, chaining options and Usage values. Removed unconfirmed claims about face mark filtering speed, viewport toggling, baked strokes not updating, file size and downstream modifier baking.
Method: documentation only; no commands were run.
