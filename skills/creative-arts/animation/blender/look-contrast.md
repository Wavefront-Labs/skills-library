---
id: creative-arts.animation.blender.look-contrast
name: look-contrast
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, look-contrast, looks, contrast-preset, agx]
level: practitioner
status: docs-checked
description: "Use Color Management Looks: AgX Punchy and contrast looks, Filmic contrast looks, and when to grade in Looks vs the compositor."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://projects.blender.org/blender/blender/src/branch/main/release/datafiles/colormanagement/config.ocio
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# look-contrast

Goal: set the overall contrast character of the image from the view transform.

## Render Properties > Color Management > Look

The manual describes Look as an artistic effect from measured film response data, applied before the colour space conversion. Looks come from the OCIO config; Blender's bundled config (release/datafiles/colormanagement/config.ocio in the source) defines:
- Contrast looks without prefix: Very High, High, Medium High, Medium, Medium Low, Low and Very Low Contrast (used with Filmic).
- AgX looks: `AgX - Punchy`, `AgX - Greyscale`, and Very High, High, Medium High, Base, Medium Low, Low and Very Low Contrast with the `AgX - ` prefix.
- The same ladder with a `False Color - ` prefix for the False Color view.
- `ACES 1.3 - Reference Gamut Compression` and `ACES 2.0 - Reference Gamut Compression`.

Which looks the UI lists depends on the selected view transform and config.

## Looks vs grading

- Look: a global adjustment applied with the view transform, chosen early for the whole show.
- Per-shot grade: compositor (for example Color Balance, RGB Curves) or external grading.
- Fix exposure with lights or Exposure first (see exposure-gamma), not with a contrast look.

## Python

`scene.view_settings.look`, for example `"AgX - Punchy"`; the available identifiers match the config's look names.

## Verify

Render a grey-scale chart and compare middle grey while changing the look; mostly shadows and highlights should move.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (Look: applied before colour space conversion) and the colour management config.ocio in the Blender source (blender/blender main, release/datafiles/colormanagement) for look names; Python API ColorManagedViewSettings.look. Removed unconfirmed per-scene, VSE and recommendation claims; corrected Filmic and AgX look lists.
Method: documentation only; no commands were run.
