---
id: creative-arts.animation.blender.asset-previews
name: asset-previews
category: creative-arts
field: animation
product: blender
tags: [blender, asset-browser, asset-previews, asset-preview, preview-render, thumbnails, mark-as-asset]
level: practitioner
status: docs-checked
description: "Get good thumbnails for Blender assets: automatic previews, Generate Preview, Load Custom Preview, Render Active Object, screenshot capture, and regenerating previews from Python."
sources:
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
  - https://docs.blender.org/api/current/bpy.types.ID.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# asset-previews

Goal: a library where every thumbnail reads instantly.

## How previews are made

Marking a data-block as an asset (`Mark as Asset`: data-block selector, Outliner, or the Object menu for objects) generates a preview automatically. Objects are captured from their local -Y axis; collections from the global -Y axis (they have no local axis). Scene assets render the active camera view in Solid mode and need an active camera.

## Setting a preview (Asset Browser, Asset Details > Preview)

- **Generate Preview:** autogenerate a new preview.
- **Load Custom Preview:** file browser to pick an image.
- **Preview menu:**
  - **Render Active Object:** preview from the 3D Viewport's active object; useful for node groups, which cannot generate their own preview.
  - **Remove Preview.**
  - **Capture Screenshot Preview:** drag-select a rectangle anywhere in Blender. Only available for editable assets (Current File assets and asset system files). The previous capture area is remembered, so a simple click repeats it. A rectangle fully inside one 3D viewport does a background render of that region, which allows a transparent background but cannot include UI elements.
- Pose assets have their own preview workflow (Pose Library page).

## Batch regeneration

```python
for ob in bpy.data.objects:
    if ob.asset_data:
        ob.asset_generate_preview()
```

`ID.asset_generate_preview()` generates a preview image and might be scheduled in a background thread, so give it time before saving.

`bpy.ops.ed.lib_id_load_custom_preview(filepath=...)` is the operator behind Load Custom Preview.

## Studio consistency

Render each asset from the same camera and lighting rig, write the images, then load them as custom previews. Use the same background and framing across the library.

## Gotchas

- Asset metadata and previews are editable only in the file that contains the asset; open the source .blend for library assets.
- Clear Asset keeps the preview inside the data-block.

## Verify

With the Asset Browser thumbnails at the largest size, no asset shows a blank or default preview.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/asset_browser.rst, files/asset_libraries/introduction.rst) and the current Python API (ID.asset_generate_preview, bpy.ops.ed.lib_id_load_custom_preview).
Confirmed: preview operators and menu names, capture axes, screenshot rules, scene preview rule, Python calls. Removed unconfirmed claims: 256 to 512 px sizing advice, material preview type panel, "Generate from Viewport" and an Asset Snapshot add-on, file-size and 3.x collection preview notes.
Method: documentation only; no commands were run.
