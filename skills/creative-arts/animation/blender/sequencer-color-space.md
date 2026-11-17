---
id: creative-arts.animation.blender.sequencer-color-space
name: sequencer-color-space
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, sequencer-color-space, sequencer-colorspace, vse]
level: practitioner
status: docs-checked
description: "Set the Sequencer color space so VSE blending, fades and effects behave: sRGB vs linear options, strip colour space per strip, and avoiding double transforms."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/color_spaces.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html#source
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/movie.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sequencer-color-space

Goal: correct colour in the Video Sequence Editor.

## Two settings

1. **Color Management > Sequencer** (scene setting): the colour space the Sequencer operates in. By default it is sRGB, but it can also be set to work in Linear space like the Compositing nodes, or another colour space. Different colour spaces give different results for colour correction, crossfades and other operations.
2. **Strip > Source > Color Space** (per strip): the colour space of the source file. The list depends on the active OCIO config. Blender tries to guess the right space automatically; if it is wrong, change it here. Data such as normal maps should use Non-Color.

## Rules

- When importing movies, **Set View Transform** (Add > Movie option) automatically picks a View Transform based on the media's colour space. In most cases Standard should be used; the wrong transform can give inaccurate colours or reduce rendering performance.
- For intermediate image files the manual recommends OpenEXR, which is always stored in a scene linear colour space.
- Blender's working space (File setting in Color Management) is Linear Rec.709 by default, with Linear Rec.2020 and ACEScg also available.

## Gotchas

- If an edit looks flat after adding already tone-mapped footage, check the scene's View Transform: set it to Standard for finished footage.
- Check Scene strips next to movie strips; their look depends on the render and colour settings in use.

## Verify

Import a rendered PNG frame as an image strip next to the same frame opened in the Image Editor. With the edit view transform set to Standard, sampled pixel values should match.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Sequencer colour space setting and its sRGB default, per-strip Color Space and OCIO-dependent list, Set View Transform behaviour and Standard recommendation, OpenEXR advice, working-space options. Removed the recommended-for-editorial and dip-and-blur crossfade claims and the AgX second-pass explanation, which are not stated in the manual.
- Method: documentation only; no commands were run.
