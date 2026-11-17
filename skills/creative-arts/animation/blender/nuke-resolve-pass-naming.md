---
id: creative-arts.animation.blender.nuke-resolve-pass-naming
name: nuke-resolve-pass-naming
category: creative-arts
field: animation
product: blender
tags: [blender, nuke-handoff, comp-handoff, nuke-naming, resolve-handoff, pass-naming, exr]
level: practitioner
status: docs-checked
description: "Package Blender passes for Nuke and Resolve: view layer and AOV naming, Multi-Layer EXR, Cryptomatte, frame numbering and a handoff sheet (studio practice)."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/files/media/image_formats.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# nuke-resolve-pass-naming

Goal: compositors in Nuke or Resolve can open Blender renders without asking questions. Most of this is studio convention (practice); the Blender facts are stated with their source in Checked.

## Output

- Output Properties > Output > Media Type **Multi-Layer EXR** saves all inputs in one multi-layer OpenEXR file; Media Type Image with OpenEXR writes one file per input. OpenEXR can store multiple layers and passes, and the manual recommends it for compositing or colour grading.
- Pass-based masks: **Cryptomatte** is an image standard for object and material masks that works with compositing software other than Blender. Light Groups (Cycles) give limited Combined passes lit by chosen lights, to be recombined in compositing.

## Naming conventions (practice)

- View layers: short names without spaces (`bg`, `char`, `fx`). Avoid dots in names; compositing packages commonly use dots to separate layer from channel, so check your target package's rules.
- AOVs and light groups: lowercase, consistent across shots (`rim_mask`, `lg_key`).
- Files: `<show>_<shot>_<layer>_v###.####.exr`, with frame numbers matching the edit (often starting at 1001). Set the number padding with `#` characters in the output File Path (the manual: `image_##_test.png` becomes `image_01_test.png`).

## In the compositing package

Check how the package lists the layers and channels of a multi-layer EXR by opening one test frame before the full handoff, and write the recombine formula for the light passes in the sheet. Do not rely on memory of channel naming; look at the file.

## Handoff sheet (put in the shot folder)

- Blender version, render engine, samples.
- Colour space of the EXRs and the view transform used for review. Blender's current manual marks Filmic as deprecated in favour of AgX.
- Pass list with meaning and the recombine formula; state whether the beauty is denoised.
- Alpha convention (premultiplied or straight) as set in your pipeline; state it explicitly.
- Frame range and handles, resolution, overscan if any.
- Camera export (FBX or Alembic) for 3D comp work.

## Verify

Open one frame in the compositing package: layer names match the sheet, and each pass shows the expected image.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): output.rst (Media Type Multi-Layer EXR, `#` frame padding), image_formats.rst (OpenEXR layers and passes, rule of thumb), passes.rst (Cryptomatte, Light Groups), color management displays_views.rst (Filmic deprecated, AgX). Removed unconfirmable specifics: EXR channel name strings, Nuke Shuffle and Resolve page behaviour, premultiplied-alpha statements, and the "denoised combined differs from summed passes" claim. The rest is marked practice. Method: documentation only; no commands were run.
