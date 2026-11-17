---
id: creative-arts.animation.color.rec2020-wide-gamut
name: rec2020-wide-gamut
category: creative-arts
field: animation
product: color
tags: [rec2020, display-standards, bt2020, wide-gamut, container-gamut, uhd, gamut-mapping, cie-scope, p3-limited]
level: advanced
status: draft
description: "Use Rec.2020 correctly as a UHD/HDR container gamut: P3-limited mastering inside it, gamut checks, and avoiding out-of-gamut animated colours."
sources:
  - https://www.itu.int/rec/R-REC-BT.2020
  - https://www.itu.int/rec/R-REC-BT.2100
  - https://partnerhelp.netflixstudios.com/hc/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rec.2020 wide gamut

**Goal:** deliver UHD HDR in the Rec.2020 container that specs require, while mastering to colours
real displays can show.

## Container vs mastering gamut

- **Rec.2020 primaries** (ITU-R BT.2020) are laser-pure: no consumer display reproduces the whole
  gamut. It is used as a **container**.
- Content is mastered within **P3-D65** (what reference monitors show) and stored in Rec.2020
  coordinates. Specs (Netflix and others) state this as "P3-D65 limited, Rec.2020 container".
- Matrix for Y'CbCr: BT.2020 non-constant luminance (`bt2020nc`).

## Setting it up (Resolve)

- Output colour space Rec.2020 with ST2084 (HDR) or Rec.2020 gamma 2.4 (rare SDR-UHD).
- Enable "Limit output gamut to P3-D65" (Colour Management) so nothing outside P3 is written.
- Use the CIE chromaticity scope with the P3 and 2020 triangles shown; animated FX colours should sit
  inside P3.

## Encoding tags

```bash
-color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc   # HDR10
```
(see `creative-arts.animation.color.hdr10-static-metadata`).

## Animation risks

- Saturated palette colours designed in a wide working space (ACEScg) can exceed P3, then be
  clipped differently by each TV. Gamut-limit in the grade.
- Rendering with ACEScg primaries for textures authored as sRGB is fine; problems come from
  saturated light colours and emissives pushed in comp.
- SDR derivatives must gamut map back to 709 (`creative-arts.animation.color.hdr-to-sdr-tone-mapping`).

## Gotchas

- Tagging Rec.709 content as Rec.2020 without converting makes everything look oversaturated on
  compliant players; converting without tagging makes it look dull.
- Rec.2020 SDR exists but is rare; most UHD SDR deliveries are Rec.709.

## Verify

CIE scope during playback shows no traces outside P3; ffprobe shows bt2020/smpte2084/bt2020nc tags
on the delivery.
