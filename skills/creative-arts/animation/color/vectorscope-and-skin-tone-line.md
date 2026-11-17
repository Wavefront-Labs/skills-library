---
id: creative-arts.animation.color.vectorscope-and-skin-tone-line
name: vectorscope-and-skin-tone-line
category: creative-arts
field: animation
product: color
tags: [vectorscope, skin-tone-line, saturation, hue, video-scopes, gamut, resolve, ffmpeg, colour-grading]
level: practitioner
status: draft
description: "Read a vectorscope to judge hue and saturation, check neutrals and the skin-tone line, and keep saturated cartoon colours inside broadcast gamut."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://ffmpeg.org/ffmpeg-filters.html#vectorscope
  - https://www.itu.int/rec/R-REC-BT.709
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vectorscope and the skin-tone line

**Goal:** measure chroma: the angle from centre is hue, distance from centre is saturation.

## Reading it

- Targets mark the 75% (or 100%) colour bar positions for R, Mg, B, Cy, G, Yl. Anything beyond the 100% targets
  is likely out of legal gamut for broadcast.
- The centre dot is zero chroma: neutrals must cluster there (see
  `creative-arts.animation.color.neutral-balance-white-point`).
- The **skin-tone line** (I-line, between yellow and red at about 123 degrees on Rec.709 scopes) is where human skin
  of all ethnicities falls in natural light; skin off the line looks sick (toward green) or sunburnt (toward
  magenta).

## Animation use

- Stylized characters often have non-human skin (blue aliens, yellow cartoon skin): there the reference is the
  colour model, not the I-line. For human characters, keep the skin palette near the line under neutral light, so
  grade shifts do not push it off.
- Palette QC: plot each character's model-sheet colours on the vectorscope; brand-saturated reds and magentas
  often exceed legal limits and need a gamut-limited version for broadcast.
- Shot matching: the shape of the vectorscope "blob" for a sequence should be similar shot to shot.

## Tools

- **Resolve:** Video Scopes > Vectorscope, enable *Show Skin Tone Indicator*; zoom 2x for low-saturation images.
- **ffmpeg:** `ffmpeg -i shot.mov -vf "vectorscope=m=color3:g=green,scale=512:512" -frames:v 1 vs.png`
- **Gamut check:** Resolve's broadcast-safe limiter (Project Settings > Color Management > Broadcast Safe) or a
  QC tool flags out-of-gamut pixels; prefer fixing saturation in the grade rather than relying on a clipper.

## Verify

Neutrals on the centre dot, human skin within a few degrees of the skin-tone line, and no traces beyond the 100%
targets in the broadcast master.
