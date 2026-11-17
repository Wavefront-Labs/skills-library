---
id: creative-arts.visual-art.digital-illustration.line-stabilisation-and-smoothing
name: line-stabilisation-and-smoothing
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-inking, digital-line-art, stabilizer, line-smoothing, stabilization, krita-brush-smoothing, clip-studio-paint, krita, procreate-streamline]
level: intro
status: draft
description: "Get clean digital ink lines with stabilisation: Krita's smoothing modes, Clip Studio's stabilization and post-correction, Procreate StreamLine, the lag trade-off, and canvas rotation."
sources: ["https://docs.krita.org/en/reference_manual/tools/freehand_brush.html", "https://procreate.com/handbook"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line stabilisation and smoothing

**Goal:** confident, smooth inked lines on a tablet, compensating for hand wobble
and the slippery pen-on-glass feel.

## Krita
- Freehand Brush tool options: **Brush Smoothing** modes:
  - *None*; *Basic*; *Weighted* (distance and stroke ending options);
  - *Stabilizer*: delay distance and "finish line"; the line trails behind the pen
    like a string. Higher distance = smoother, more lag.
- Turn on "Delay" with a small distance for inking curves; off for sketching.

## Clip Studio Paint
- Sub tool detail: **Stabilization** level (0-100; around 10-25 for inking is common)
  and **Post correction** (smooths after the stroke; adjust by speed).
- Vector layers allow fixing lines afterward (see vector layers skill).

## Procreate
- Brush Studio > Stabilization: **StreamLine** amount and Motion filtering; also a
  global pressure-and-smoothing setting in Prefs. (See Procreate brush skills.)

## Technique matters more
1. Draw from the shoulder/elbow for long lines; ghost the stroke above the surface first.
2. **Rotate the canvas** so the stroke falls in your natural arc direction.
3. Zoom out to ink long lines (less magnified wobble), zoom in for detail.
4. One stroke per line; undo and redo rather than feathering many short strokes.
5. Use a slightly rougher screen protector or tablet nib for friction.

## Trade-offs
High stabilisation lags and rounds off sharp corners and quick tapers; lower it
for hatching and fast flicks, raise it for long smooth curves.

## Gotchas
- Very high stabiliser on everything: lines feel dead and corners round.
- Forgetting smoothing is per-tool/per-brush: switching brushes changes behaviour.

## Verify
- [ ] Long curves smooth without visible lag errors.
- [ ] Sharp corners and tapers still possible (stabiliser adjusted per task).
