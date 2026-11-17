---
id: creative-arts.animation.blender.aces-workflow
name: aces-workflow
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, aces-ocio, aces, acescg, working-space]
level: practitioner
status: docs-checked
description: "Work in ACES with Blender: ACEScg working space, the bundled ACES 1.3 and 2.0 views, ACES2065-1 and ACEScg EXR colour spaces, and full ACES configs through OCIO."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/opencolorio.html
  - https://docs.blender.org/manual/en/latest/render/color_management/color_spaces.html
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# aces-workflow

Goal: make Blender renders fit an ACES pipeline.

## Options by depth

1. **Bundled config**: Blender's standard OpenColorIO configuration includes essential ACES support: the ACEScg working space, the ACES 2.0 view transform (the Views list also has ACES 1.3), and OpenEXR images saved in the ACES2065-1 and ACEScg colour spaces. The manual says this covers most needs for an ACES pipeline.
2. **Working space**: Render Properties > Color Management > **Working Space** (File). Linear Rec.709 is the default; Linear Rec.2020 and ACEScg are available for a wider gamut and ACES compatibility. The working space affects the colours of all data-blocks in the file. Choose it at the start of a project and use it for all blend files; conversion between working spaces is only an approximation and linking/appending converts colours automatically.
3. **Official ACES configs**: for more complete support, install the official ACES OpenColorIO configurations manually and point the `OCIO` environment variable at one (see custom-ocio-config).

## Handoff

- Use OpenEXR for intermediate files: the manual says EXR is always stored in scene-linear colour spaces at high precision, suiting later compositing and conversion.
- Pick the EXR colour space (Working Space, ACEScg or ACES2065-1) explicitly and record it in the pipeline notes.

## Gotchas

- Mixing renders from different working spaces without conversion shifts colours. Decide on one working space per show.
- AgX and the ACES views are separate view transforms in the Views list; for an ACES show, choose an ACES view.
- Wide-gamut display work pairs with the ACEScg or Linear Rec.2020 working space and a Display P3 or Rec.2020 display (see display-device-hdr).

## Verify

Render a colour chart scene, open the saved EXR in the downstream tool with the agreed colour space, and compare patch values with the reference.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/opencolorio (ACES section, BLENDER_OCIO, roles), color_spaces (Working Space options, ACEScg and ACES2065-1 definitions, OpenEXR always scene linear) and displays_views (ACES 1.3 / ACES 2.0 views). Removed unconfirmed claims about EXR metadata, half float, Nuke settings, colour-picker behaviour and the contents of full ACES studio configs.
Method: documentation only; no commands were run.
