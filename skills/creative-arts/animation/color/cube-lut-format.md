---
id: creative-arts.animation.color.cube-lut-format
name: cube-lut-format
category: creative-arts
field: animation
product: color
tags: [cube-lut, lut-format, 3d-lut, 1d-lut, iridas-cube, resolve-cube, lut-interchange, ffmpeg-lut3d, ocio]
level: practitioner
status: draft
description: "Read, write and debug .cube LUT files: 1D vs 3D headers, domain lines, red-fastest ordering, sizes, and the Resolve vs Iridas variants that break interchange."
sources:
  - https://opencolorio.readthedocs.io/en/latest/guides/using_ocio/tool_overview.html
  - https://ffmpeg.org/ffmpeg-filters.html#lut3d-1
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .cube LUT formats

**Goal:** move LUTs between Resolve, Nuke, OCIO, ffmpeg and cameras without silent misreads.

## Structure

```
TITLE "show_look_v003"
LUT_3D_SIZE 33
DOMAIN_MIN 0.0 0.0 0.0
DOMAIN_MAX 1.0 1.0 1.0
0.000000 0.000000 0.000000
0.031250 0.000000 0.000000
...
```

- Lines after the header are output RGB triplets. **Red changes fastest**, then green, then blue
  (index = r + g*N + b*N*N). Getting this wrong swaps channels in strange ways.
- A 3D LUT of size N has N^3 lines (33^3 = 35,937; 65^3 = 274,625).
- `LUT_1D_SIZE` defines a 1D LUT (per-channel curves, N lines).
- Comments start with `#`.

## Variants

| Variant | Difference |
|---|---|
| Adobe/Iridas cube | `DOMAIN_MIN/MAX` for input range; either 1D or 3D |
| Resolve cube | can contain a 1D shaper **and** a 3D LUT in one file (`LUT_1D_SIZE` + `LUT_3D_SIZE`, with `LUT_1D_INPUT_RANGE`/`LUT_3D_INPUT_RANGE`) |

Many tools read only one of these; OCIO identifies them as `iridas_cube` and `resolve_cube` formats. A Resolve
shaper+3D cube loaded in a tool that only reads Iridas cubes ignores the shaper and gives a wrong image.

## Input range

A LUT expects input within its domain (usually 0-1). Feeding linear scene values (up to 10+) into a 0-1 3D LUT
clips; use a log shaper or build the LUT in log (ACEScct) space
(see `creative-arts.animation.color.lut-baking-from-ocio`).

## Applying with ffmpeg

`ffmpeg -i in.mov -vf "lut3d=file=show_look.cube:interp=tetrahedral" -c:v prores_ks -profile:v 3 out.mov`
(tetrahedral interpolation is the most accurate; ffmpeg works in the input's pixel format, so convert to a 10-bit+
RGB format first if precision matters).

## Verify

Apply the LUT to a synthetic ramp/colour-patch image in two tools (e.g. Resolve and ffmpeg): pixel values match
within 1-2 code values in 10-bit.
