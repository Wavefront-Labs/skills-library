---
id: creative-arts.photography-fine-art.adobe-lightroom.upright-and-guided-perspective-correction
name: upright-and-guided-perspective-correction
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, upright-correction, lightroom-transform, guided-upright, perspective-correction, keystone, lightroom-classic]
level: practitioner
status: draft
description: "Correct perspective in Lightroom Classic with Upright modes (Auto, Level, Vertical, Full, Guided) and Transform sliders, keeping natural proportions."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/guided-upright-perspective-correction.html", "https://helpx.adobe.com/in/lightroom-classic/desktop/help/upright-automatic-perspective-correction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upright and Guided perspective correction

Apply **lens profile corrections first**: Upright analyses distortion-corrected lines.

## Upright modes (Transform panel, `Shift+T`)
- **Auto**: balanced level, aspect and perspective; good default.
- **Level**: horizon only.
- **Vertical**: level plus converging verticals.
- **Full**: level, vertical and horizontal perspective; can look extreme.
- **Guided**: draw 2-4 guide lines along lines that should be vertical or horizontal (two verticals fix keystoning; add two horizontals for full correction). Best control for architecture.

## Manual sliders
Vertical, Horizontal, Rotate, **Aspect** (restore building proportions: perfectly corrected buildings look too tall and wide-topped; Aspect +10 to +30 or leave ~10% convergence), Scale, X/Y Offset.
- **Constrain Crop** trims the empty white areas; or leave it off and fill edges with Generative/content-aware Remove for maximum frame.

## Craft
- For tall buildings shot from below, leaving slight convergence looks more natural than fully parallel verticals.
- Use the grid overlay (View > Loupe Overlay > Grid; Ctrl/Cmd+Alt/Option+O) to judge.
- Sync Upright: syncing the mode re-analyses each image; sync the "Upright transform" settings (computed values) to apply identical correction to a bracket for merging.

## Gotchas
- Heavy correction stretches pixels near edges; check sharpness at 100% in corners.
- Upright resets if you change the lens profile; reapply after profile changes.

## Verify
- [ ] Verticals parallel (or deliberately converging slightly), horizon level, proportions look natural.
