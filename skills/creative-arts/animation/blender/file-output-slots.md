---
id: creative-arts.animation.blender.file-output-slots
name: file-output-slots
category: creative-arts
field: animation
product: blender
tags: [blender, file-output, file-output-slots, file-slots, per-slot-format, compositor]
level: practitioner
status: docs-checked
description: "Configure File Output node inputs in Blender: add items, names as sub-paths, Override Node Format for per-item formats, and how the 5.x node layout differs from 4.x slots."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/file_output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# file-output-slots

Goal: write several images per frame from the compositor (passes, mattes, a review image) with the right names and formats.

## Blender 5.2 layout (Items)

Add > Output > **File Output** (scene compositor only). In the Sidebar > Node > Properties tab:

- **Images/Layers** panel: lists all input sockets. The name of each input is used to build the final file name; each can be renamed. Add inputs by dragging an output onto the blank socket area or from this panel.
- With **Media Type** *Image*, an input name containing a slash is read as folders, for example `passes/diffuse`; missing folders are created.
- **Override Node Format** on the selected item lets it use its own **Item Format** instead of the node's *Node Format* (for example a JPEG review image next to EXR passes). The per-item format applies to Media Type Image; with *Multi-Layer EXR* all inputs are layers of one file.
- **Output Paths** panel shows the final path and extension for each input.

## Older 4.x files

The 4.5 manual describes a single **Base Path** for the node. In 5.x the node has separate Directory and File Name fields and inputs are items. The 5.2 manual does not describe converting older files, so check names and formats after opening an older file in 5.x.

## Typical setup

```
Image (graded)   -> item "beauty/sh010_beauty_"     EXR (node format)
Matte            -> item "matte/sh010_hero_matte_"  PNG (override node format)
Image (graded)   -> item "review/sh010_"            JPEG (override node format)
```

## Gotchas

- `####` in the File Name or item name controls where the frame number goes and its padding.
- Non-colour data saved as a display-referred format may get the view transform; check *Save as Render* in the item and node format, or use EXR for data (see `creative-arts.animation.blender.compositor-file-output`).
- The node writes when frames are rendered or the compositor is run, not while you tweak nodes.

## Verify

Render two frames and check that each item's folder holds files with the expected names and formats, using the Output Paths panel as a guide.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch, compositing/types/output/file_output) and the 5.2 source (rna_nodetree.cc NodeCompositorFileOutputItem: override_node_format, save_as_render, format). Fixed: 5.2 uses Images/Layers items, Override Node Format and Output Paths; the 4.x layout is described only from the 4.5 manual (Base Path). Removed unconfirmed claims that names without hashes get four digits appended, and the release-notes link (not a 5.2 manual page).
Method: documentation only; no commands were run.
