---
id: creative-arts.animation.color.lut-baking-from-ocio
name: lut-baking-from-ocio
category: creative-arts
field: animation
product: color
tags: [lut-baking, ociobakelut, ocio, show-lut, shaper, cube-lut, colour-management, review-lut, on-set-lut]
level: advanced
status: draft
description: "Bake a show LUT from the OCIO config with ociobakelut for tools that cannot read OCIO: shaper spaces for linear input, cube sizes, formats and validation."
sources:
  - https://opencolorio.readthedocs.io/en/latest/guides/using_ocio/tool_overview.html
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/overview.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baking a show LUT from OCIO

**Goal:** give LUT-only tools (some editing apps, monitors, LUT boxes, web previews) the exact show transform
defined in the OCIO config.

## The tool

`ociobakelut` (ships with OCIO). Typical bakes:

```
# ACEScct working images -> show view on Rec.709 display, 65-point cube for Resolve/ffmpeg
ociobakelut --iconfig config.ocio --inputspace ACEScct \
  --displayview "Rec.1886 Rec.709 - Display" "ACES 1.0 - SDR Video" \
  --format resolve_cube --cubesize 65 show_acescct_to_rec709.cube

# scene-linear input needs a shaper so the 3D LUT samples a sensible range
ociobakelut --iconfig config.ocio --inputspace ACEScg --shaperspace ACEScct \
  --outputspace "sRGB - Display" --format resolve_cube --cubesize 65 --shapersize 4096 show_linear.cube
```

Run `ociobakelut --help` and `ociobakelut --list` on your version: formats include `resolve_cube`, `iridas_cube`,
`flame` (3dl), `houdini`, `cinespace` (csp), `spi1d/spi3d`; flag names (`--displayview`, `--looks`) vary slightly by
release. Add `--looks "<look>"` to bake a creative look in (see `creative-arts.animation.color.ocio-looks-per-shot`).

## Rules

1. **Never bake from linear without a shaper**: a 0-1 cube sampled linearly wastes almost all samples on highlights
   and bands in the shadows.
2. Bake per output display (Rec.709, sRGB, P3) and name accordingly.
3. Bake again whenever the config changes; record the config version in the LUT `TITLE` line.

## Verify

Process a test image through the OCIO config directly (`ocioconvert` or the DCC viewer) and through the baked LUT
(e.g. ffmpeg `lut3d`, see `creative-arts.animation.color.cube-lut-format`); difference under 1-2 10-bit code values on
ramps and charts, with no banding in dark gradients.
