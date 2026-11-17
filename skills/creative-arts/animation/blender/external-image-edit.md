---
id: creative-arts.animation.blender.external-image-edit
name: external-image-edit
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, external-image-edit, quick-edit, project-paint, photoshop, krita]
level: practitioner
status: docs-checked
description: "Round-trip texture painting through an external paint app with Blender Quick Edit and Apply (projection) or Image > Edit Externally, plus the Image Editor preference."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/tool_settings/options.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/file_paths.html
  - https://docs.blender.org/manual/en/latest/editors/image/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# external-image-edit

Goal: do the heavy 2D work in an external paint app and bring it back without manual UV wrangling.

## Prerequisite
Preferences > File Paths > Applications > **Image Editor**: the path to the external program used for image editing. Both Quick Edit and Edit Externally use it.

## Quick Edit (projection round trip)
1. Texture Paint mode, frame the model. Texture Paint tool settings > Options panel > **External**: **Screen Grab Size** is the size of the captured image used for reprojecting.
2. **Quick Edit** edits a snapshot of the viewport in the external editor.
3. Paint in the external app and save the file it opened.
4. Back in Blender, with the view unchanged, press **Apply**: it projects the edited image back onto the object. **Apply Camera Image** projects an edited render from the active camera instead. The Options panel's Occlude and Backface Culling settings affect what the projection reaches (Occlude affects only exposed pixels; Backface Culling paints only front sides).

Keep the view unchanged between Quick Edit and Apply, since the projection depends on the captured viewpoint (practice).

## Edit Externally (the texture file itself)
Image Editor > Image > **Edit Externally** opens the image in the same external program. After saving in that program use Image > **Reload** (Alt R), which reloads the image from the file on drive. The image needs a file on disk, so save generated images first (practice).

## Gotchas
- Packed or generated images have no external file to round-trip; save them to disk or unpack first (practice).
- Apply targets the active paint slot; check the slot first (practice).
- Colour management: avoid applying a display LUT or view transform in the external app (practice).

## Verify
After Apply the external strokes sit on the features they were painted over; the image shows `*` until saved.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): texture_paint/tool_settings/options.rst (Screen Grab Size, Quick Edit, Apply, Apply Camera Image, Occlude, Backface Culling), editors/preferences/file_paths.rst (Image Editor path), editors/image/editing.rst (Edit Externally, Reload Alt R). Removed: the 512 default grab size, the "Image editor not set" error text, Krita/Photoshop/GIMP names as required apps, and the Image Editor view-bookmark advice. Method: documentation only; no commands were run.
