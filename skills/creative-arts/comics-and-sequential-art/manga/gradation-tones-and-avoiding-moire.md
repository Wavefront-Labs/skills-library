---
id: creative-arts.comics-and-sequential-art.manga.gradation-tones-and-avoiding-moire
name: gradation-tones-and-avoiding-moire
category: creative-arts
field: comics-and-sequential-art
product: manga
tags: [manga, screentone, manga-tones, gradation-tone, tone-moire, tone-layering, screen-angle, double-toning]
level: advanced
status: draft
description: "Use gradation tones and layered tones without moire: same-LPI stacking, angle offsets, gradient direction choices, and checking/rescuing moire in scans or digital output."
sources:
  - https://en.wikipedia.org/wiki/Screentone
  - https://en.wikipedia.org/wiki/Moir%C3%A9_pattern
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gradation tones and avoiding moire

**Goal:** smooth tonal gradients and layered shadows without interference patterns.

## Gradation tones
- Pre-made gradation sheets (traditional) or gradient tones (digital): dots grow from
  0% to high density across the area.
- Uses: skies, backgrounds, mood shading, light falloff.
- Direction follows light: darker away from the source.
- Digital (CSP): fill a gradient on a layer, then set Layer property > Tone; or use
  gradient tone materials. Set LPI to the book default.

## Layering tones (double toning)
- Add a second tone over a first for darker shadow areas.
- **Moire** appears when two dot grids overlap at slightly different angles or LPIs.
- Avoid:
  1. Use the **same LPI** for stacked tones.
  2. Either the same angle with offset (aligned dots, darkening density), or an angle
     difference of around 45 degrees, which reduces visible moire compared with small
     differences.
  3. Prefer a single darker tone instead of stacking when possible.

## Scans and reductions
- Scanning printed tones or reducing toned art can create moire against the
  scanner/screen grid. Scan line art at high resolution (1200 dpi) and resize with
  care; descreen only for printed sources being restored.
- Digital: output tones at the final print size and resolution; resizing after
  toning causes moire.

## Verify
- [ ] Stacked tones share LPI; no visible moire at print size.
- [ ] Tones applied/rasterised at final output size.
