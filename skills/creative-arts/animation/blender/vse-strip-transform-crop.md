---
id: creative-arts.animation.blender.vse-strip-transform-crop
name: vse-strip-transform-crop
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-strip-transform, strip-crop, image-fit]
level: practitioner
status: verified
description: "Position and crop strips in the VSE: transform position, scale, rotation and origin, preview transform tools, crop values, mirror, and the fit method used when adding media."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html#image-menu
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/toolbar.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/controls/pivot_point.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# vse-strip-transform-crop

Goal: picture-in-picture, reframing and mixed-resolution media in an edit.

## Fit on import

Add > Movie/Image has **Fit Method**: Scale to Fit (whole picture inside the frame, transparent borders possible), Scale to Fill (fills the frame, may crop), Stretch to Fill (distorts to fill). Afterwards the same three exist as Strip > Image Transform > Scale to Fit, Scale to Fill and Stretch to Fill. The operator enum in 4.5.14 also has a fourth entry, Use Original Size (`ORIGINAL`).

## Transform (Sidebar > Strip > Transform)

- **Position X/Y**, **Scale X/Y**, **Rotation**, **Mirror** (X or Y) and **Filter** (Auto, Nearest, Bilinear, Cubic Mitchell, Cubic B-Spline, Box; Auto picks by scale factor). In 4.5.14 these are `strip.transform.offset_x/offset_y`, `scale_x/scale_y`, `rotation`, `origin` (default 0.5, 0.5) and `filter`, and `strip.use_flip_x/use_flip_y`.
- In the Preview, the toolbar tools Move (G), Rotate (R) and Scale (S) change the selected strips directly. Rotation and scale happen around the **Pivot Point** (header, shortcut Period): Bounding Box Center, Median Point, 2D Cursor or Individual Origins.
- The Image menu has Clear > Position, Scale, Rotation and Strip > Clear > All Transforms to reset values.
- Properties can be animated (hover and press I) for moves, zooms and picture-in-picture.

## Crop (Sidebar > Strip > Crop)

**Top**, **Left**, **Bottom**, **Right**: the number of pixels cropped from the source image (integer properties `strip.crop.max_y`, `min_x`, `min_y`, `max_x`).

## Recipes

- Picture-in-picture: reduce Scale, position in a corner, crop slightly, add a Color strip behind it as a border.
- Reframe 16:9 to 9:16 for social: set the scene resolution to portrait, use Scale to Fill and animate Position X to follow the subject.

## Gotchas

- Scaling up low-resolution media looks soft. Choose the Filter that suits the content.
- The Sidebar Strip tab is only available in Sequencer and Sequencer & Preview modes.

## Verify

Play the edit: the strip sits where intended at every frame and the render matches the preview.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Fit Method options and the Strip > Image Transform equivalents, Transform panel fields and Filter list, preview toolbar Move, Rotate and Scale shortcuts, Pivot Point options and shortcut, Clear menus, Crop fields in pixels, Strip tab availability. Removed the Use Original Size fit option, the Origin field, Alt G/S/R resets and the modifiers-before-transform claim, which the 5.2 manual does not give.
- Run check, 2026-11-01, Blender 4.5.14 LTS headless: the Transform property set and the Filter items AUTO, NEAREST, BILINEAR, CUBIC_MITCHELL, CUBIC_BSPLINE, BOX on a strip; `use_flip_x/y`; the four integer crop fields; `fit_method` items FIT, FILL, STRETCH, ORIGINAL on the Add Movie and Add Image operators; a two-strip sequence with a scaled, offset, cropped Color strip rendered five PNG frames in background mode. Unrun: the preview toolbar tools and shortcuts, Pivot Point, Clear menus, animation by hovering and pressing I, the recipes, visual result of transform and crop.
- Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
