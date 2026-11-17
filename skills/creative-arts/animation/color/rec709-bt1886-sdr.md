---
id: creative-arts.animation.color.rec709-bt1886-sdr
name: rec709-bt1886-sdr
category: creative-arts
field: animation
product: color
tags: [rec709, display-standards, bt1886, gamma-2-4, sdr, broadcast-video, d65, 100-nits, legal-range, grading-standard]
level: practitioner
status: draft
description: "Master SDR video to Rec.709 with BT.1886 gamma 2.4: primaries, white point, 100-nit reference, legal levels, and how it differs from sRGB viewing."
sources:
  - https://www.itu.int/rec/R-REC-BT.709
  - https://www.itu.int/rec/R-REC-BT.1886
  - https://tech.ebu.ch/publications/tech3320
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rec.709 with BT.1886

**Goal:** an SDR master that matches what broadcasters, streamers and TVs expect. Rec.709 (ITU-R
BT.709) defines HD primaries, D65 white and the Y'CbCr matrix; BT.1886 defines the reference
display EOTF (effectively gamma 2.4 on an ideal display).

## The reference

| Parameter | Value |
|---|---|
| Primaries | BT.709 (same as sRGB) |
| White point | D65 (x 0.3127, y 0.3290) |
| EOTF | BT.1886, gamma 2.4 |
| Peak white | 100 cd/m2 (nits) |
| Surround | dim, ~5 nits around the display (BT.2035 / EBU Tech 3320 guidance) |
| Levels | limited range for delivery: 64-940 10-bit |

## Setting it up

- Monitor: a reference or calibrated display in Rec.709 / gamma 2.4 / 100 nits mode (see `creative-arts.animation.color.look-development-for-color-pipelines`
  for monitor calibration).
- Resolve: colour-managed output Rec.709 Gamma 2.4; or Rec.709-A on Mac GUI viewers to compensate
  macOS ColorSync display of the viewer.
- OCIO/Blender: choose a Rec.1886 / Rec.709 display in the config for the final output, not sRGB.

## Rec.709 vs sRGB

Same primaries and white; different tone curve and viewing assumption. sRGB (approximately 2.2,
brighter office surround) makes the same file look lighter and less contrasty than gamma 2.4 in a
dim room. Decide per project:
- Broadcast/streaming TV first: grade 2.4, deliver tagged BT.709.
- Web/phone first: many studios grade 2.2 or sRGB; tag accordingly (`iec61966-2-1` transfer for sRGB).

## Legal levels

Keep luma within 64-940 (10-bit) and chroma within limits; broadcasters reject super-whites and
illegal chroma. Saturated animated reds and blues hit chroma limits first. Use Resolve's
broadcast safe or a soft clip node, and check the waveform/vectorscope.

## Verify

A 75% bars and greyscale ramp through the output reads correct on the waveform (0/100 IRE at
64/940), and the same frame on the reference display matches the grading viewer.
