---
id: creative-arts.comics-and-sequential-art.inking.stroke-stabilization-and-line-smoothing
name: stroke-stabilization-and-line-smoothing
category: creative-arts
field: comics-and-sequential-art
product: inking
tags: [inking, digital-inking, stroke-stabilization, line-smoothing, clip-studio-paint, photoshop-smoothing, procreate-streamline, lazy-nezumi]
level: practitioner
status: draft
description: "Tune stroke stabilisation for digital inks: CSP stabilization and post-correction, Photoshop smoothing, Procreate StreamLine, trade-offs in lag and corners, and when to turn it off."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html
  - https://openlibrary.org/search?q=Art+of+Comic+Book+Inking
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stroke stabilisation and line smoothing

**Goal:** smooth, confident digital lines without killing responsiveness or rounding
off corners you wanted sharp.

## Where the setting lives
| App | Setting |
|---|---|
| Clip Studio Paint | Tool property > Stabilization (0-100); Sub Tool Detail > Correction > Post correction, Adjust by speed |
| Photoshop | Options bar > Smoothing (0-100%) with options like Pulled String Mode and Catch-up on Stroke End |
| Procreate | Brush Studio > Stabilization > StreamLine and Stabilization amounts |
| Krita | Brush smoothing: Basic, Weighted, Stabilizer |
Windows users sometimes add a system-wide smoother (e.g. Lazy Nezumi Pro) for apps
without good built-in options.

## Choosing values
- **Low (CSP ~6-15, PS 10-20%)**: everyday figure inking; minimal lag.
- **Medium (CSP ~20-40)**: long smooth curves (hair, clothing sweeps).
- **High**: very long curves or shaky hands; noticeable lag, and corners round off.
- Separate brush presets: e.g. "G-pen 10" for figures, "G-pen 35" for long curves.

## Corners and detail
High stabilisation turns sharp corners into curves and makes small detail feel
sluggish. Ink corners as two strokes, or drop stabilisation for detail work.

## Alternatives to more smoothing
- Draw with the arm, faster strokes; rotate the canvas.
- Zoom so the stroke is a comfortable arm movement.
- Vector layers to adjust lines after (see the vector inking skill).

## Verify
- [ ] Long curves smooth without visible wobble at print size.
- [ ] Corners where intended stay sharp; small details not mushy.
