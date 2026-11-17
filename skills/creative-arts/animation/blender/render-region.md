---
id: creative-arts.animation.blender.render-region
name: render-region
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, render-region, crop-to-region, border-render]
level: practitioner
status: docs-checked
description: "Render only part of the frame: set a render region with Ctrl B, Crop to Render Region on or off, the separate viewport region, and patch re-render workflows."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/navigate/regions.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/format.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# render-region

Goal: save time by rendering only the area being worked on, or patching a fix into a finished frame.

## Setting a region

- **Ctrl B** (View > View Regions > Render Region...) and drag a box. **Ctrl Alt B** (Clear Render Region) removes it.
- In Camera View the region applies to the viewport and to the final render. To disable it without clearing, untick Output Properties > Format > **Render Region**.
- Outside Camera View, the region only applies to the viewport; disable it with the checkbox in the 3D Viewport Sidebar. Both regions can exist at once.
- Per the manual, viewport render regions only apply when using Cycles, not EEVEE, but they always affect the final render.

## Crop to Render Region

- On: the saved image is cropped to the region's size.
- Off: the image keeps the full frame, with a transparent background around the region. Use this for patches, because the patch lines up with the original frame.

## Patch workflow (fix a small area on finished frames)

1. Set the region over the problem area with some margin, Crop off, and an RGBA format with Film > Transparent enabled.
2. Render the affected frames to a separate folder.
3. Comp: Alpha Over the patch on the original, or mask it in.

## Gotchas

- Leave a margin around the fix, because denoising and other effects can behave differently at the region edge. This is a precaution rather than a manual figure.
- Forgetting to clear or disable the region gives partial full renders. Check that Render Region is off before submitting to a farm.
- Python: `scene.render.use_border`, `use_crop_to_border`, and `border_min_x`, `border_max_x`, `border_min_y`, `border_max_y` (fractions of the frame).

## Verify

Render with a region and Crop off, then Difference-blend with the original in the compositor. Only the region should show differences.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and rna_scene.cc on main.
Confirmed: Ctrl B and Ctrl Alt B shortcuts and menu path; Camera View versus non-camera-view behaviour; Output Properties > Format > Render Region and Crop to Render Region definitions; the viewport-only region toggle in the Sidebar; Cycles-only viewport application; RNA properties `use_border`, `use_crop_to_border`, `border_min_x`.
Removed as unconfirmed: the 30 px margin figure and the claim that the region can be keyed via the Graph editor with a specific recipe.
Method: documentation only; no commands were run.
