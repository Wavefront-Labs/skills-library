---
id: creative-arts.animation.blender.stamp-metadata
name: stamp-metadata
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, stamp, stamp-metadata, burn-into-image, metadata-note]
level: practitioner
status: docs-checked
description: "Add render metadata in Blender: Metadata panel fields, Note, Metadata Input, Burn into Image options, and the Python properties for farm scripts."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/metadata.html
  - https://projects.blender.org/blender/blender/src/branch/main/source/blender/makesrna/intern/rna_scene.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# stamp-metadata

Goal: every frame says what it is: shot, version, frame, camera, who rendered it.

## Output Properties > Metadata
Only some image formats support metadata (see the manual's image formats page). Options:
- **Metadata Input**: *Scene* (metadata from the current scene) or *Sequencer Strips* (from the strips in the Sequencer).
- **Include**: Date, Time (current scene time and render frame as HH:MM:SS.FF), Render Time, Frame, Frame Range, Memory (peak usage), Hostname, Camera (active camera name), Lens (the active camera's lens value), Scene, Marker (name of the last marker), Filename (of the blend file), Strip Name (foreground sequence strip).
- **Note**: a custom note. The manual suggests it for render farms, scripting in an identifier such as a render node or job number.
- **Burn into Image**: adds the metadata as text on the render: **Font Size**, **Text Color** (with alpha), **Background** (colour and alpha), **Include Labels** (prefix each value with its label, such as "Camera").

## Python
Properties on `bpy.context.scene.render` (names from the RNA source): `use_stamp` (Burn into Image), `use_stamp_note` with `stamp_note_text`, `use_stamp_camera`, `use_stamp_lens`, `use_stamp_frame`, `use_stamp_frame_range`, `use_stamp_scene`, `use_stamp_marker`, `use_stamp_filename`, `use_stamp_sequencer_strip`, `use_stamp_render_time`, `use_stamp_memory`, `use_stamp_hostname`, `use_stamp_labels`, `metadata_input`, `stamp_font_size`.

```python
r = bpy.context.scene.render
r.use_stamp = True
r.use_stamp_note = True
r.stamp_note_text = "SH010 anim v012"
r.use_stamp_camera = r.use_stamp_lens = r.use_stamp_frame = True
```
Setting these in a pre-render script keeps the note matching the job.

## Gotchas
- Burn-in is drawn on the render, so set Font Size to suit the output resolution.
- Metadata is only written if the chosen image format supports it.

## Verify
Render a frame and confirm the burned-in text is readable; for file metadata, inspect the saved file with a tool that reads that format's metadata.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Metadata panel page, branch blender-v5.2-release; Python property names from rna_scene.cc on the Blender main branch. Confirmed: panel option names and meanings (including Strip Name, Metadata Input, Include Labels), Note hint, and the property names listed. Removed unconfirmed claims: EXR and PNG as metadata formats, Image Editor sidebar Metadata location, oiiotool, dailies font size, and behaviour remarks about Marker and strips.
Method: documentation only; no commands were run.
