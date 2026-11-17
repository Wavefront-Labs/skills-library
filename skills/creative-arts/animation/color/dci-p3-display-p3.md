---
id: creative-arts.animation.color.dci-p3-display-p3
name: dci-p3-display-p3
category: creative-arts
field: animation
product: color
tags: [dci-p3, display-standards, display-p3, p3-d65, cinema, xyz, wide-gamut, apple-displays, theatrical-grade]
level: advanced
status: draft
description: "Work with P3 gamuts: DCI-P3 for cinema (2.6 gamma, DCI white, 48 nits) vs Display P3 on Apple devices vs P3-D65 for HDR mastering, and converting between them."
sources:
  - https://www.dcimovies.com/
  - https://www.color.org/chardata/rgb/DisplayP3.xalter
  - https://partnerhelp.netflixstudios.com/hc/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DCI-P3, P3-D65 and Display P3

**Goal:** not confuse three "P3"s that share primaries but differ in white point and tone curve,
so cinema, HDR and Apple-device versions all look right.

## The three

| Name | White | Transfer | Peak | Use |
|---|---|---|---|---|
| DCI-P3 (SMPTE RP 431-2) | DCI white (~6300K, greenish) | gamma 2.6 | 48 cd/m2 (14 fL) | theatrical projection |
| P3-D65 | D65 | gamma 2.6 (cinema) or PQ (HDR) | 48 nits / up to 1000+ | modern theatrical, HDR mastering gamut |
| Display P3 (Apple) | D65 | sRGB curve | device | iPhone/Mac screens, web wide-gamut |

All have the same red, green, blue primaries: wider than Rec.709, especially in reds and greens,
which matters for saturated animated palettes.

## Workflows

- **Theatrical grade**: grade on a P3 projector or monitor in P3-D65 or DCI mode at 48 nits, in a
  dark room. The DCP tool converts to X'Y'Z' (`creative-arts.animation.encode-delivery.dcp-festival-master`).
- **Rec.709 master to cinema**: conversion keeps colours inside 709 (looks correct but does not use
  P3's extra range); fine for festivals.
- **HDR mastering**: P3-D65 gamut limited inside a Rec.2020 container (`creative-arts.animation.color.hdr-pq-hlg`).
- **Apple devices**: Display P3 images/video show wider colour on device; untagged images are
  assumed sRGB, so tag P3 assets (ICC profile in PNG/JPEG, colour tags in video).

## Converting

OCIO configs (ACES) have P3-D65 and P3-DCI displays; Resolve has P3-D65, P3-DCI, P3-D60 output
spaces. When moving from DCI white to D65, use chromatic adaptation (Bradford/CAT02) unless the look
intentionally keeps the DCI white tint.

## Gotchas

- Viewing a DCI-P3 grade on a D65 display looks green-yellow tinted.
- Gamma 2.6 at 48 nits in a dark cinema looks right; the same file on a 100-nit TV looks dark and
  contrasty: make a separate video version.
- Saturated P3 colours clip to 709 in SDR video versions; plan gamut mapping in the trim.

## Verify

Test patterns (P3 primaries and greys) through the chain on the target display; white measures the
intended white point and saturated primaries are not clipped or shifted.
