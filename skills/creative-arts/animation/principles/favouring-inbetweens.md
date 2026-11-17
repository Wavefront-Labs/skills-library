---
id: creative-arts.animation.principles.favouring-inbetweens
name: favouring-inbetweens
category: creative-arts
field: animation
product: principles
tags: [animation, slow-in-slow-out, favouring-inbetweens, thirds, halves, quarters, timing-chart, spacing, inbetweening, 2d]
level: practitioner
status: draft
description: "Read and write timing charts that favour inbetweens (halves, thirds, quarters) to build ease-ins and ease-outs, and translate them to CG key placement."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Inbetweening
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Favouring inbetweens

Goal: produce slow-in/slow-out by placing inbetweens off-centre - closer to one key - using
the chart notation every 2D studio uses.

## Notation
A chart is a short line between two keys with ticks for each inbetween:
- A tick at the **half** (50 %) is a plain inbetween.
- A tick at a **third** or **quarter** nearer one key "favours" that key.
- Successive halves toward a key (1/2, 1/4, 1/8) produce a classic ease into it.

Example: keys 1 and 9 on twos, chart with breakdown 5 at 1/2, then 7 at 1/2 of 5-9, then 8 at
1/2 of 7-9 -> the drawings bunch near 9: an ease-in to 9.

## Method
1. Decide where the move is slow (near which key) and where it is fast.
2. Place the breakdown first (it may itself favour a key).
3. Halve repeatedly toward the slow end; leave wide gaps at the fast end.
4. Write the chart on the key drawing next to the drawing number (2D), or annotate the
   blocking notes (CG).

## Thirds vs halves
- Halving gives a strong, accelerating ease (each gap is half the last).
- Thirds give a gentler ease. Williams uses thirds for subtle, softer moves; halves for crisp
  eases into accents.

## CG translation
- Place breakdown keys at the charted positions (use a tween slider at 33 % / 25 %), then
  let spline tangents create the in-betweens; check with motion trails that the spacing matches
  the chart.
- Or keep keys on the extremes and shape the curve so the per-frame spacing follows the chart.

## Failure modes
- Every chart halving into both keys: everything eases, nothing has snap.
- Charting without considering the arc: favoured spacing on a straight line.
- Inbetweeners inbetweening "by eye" instead of measuring the chart - drift.

## Verify
- [ ] Each interval has a chart with intentional favouring.
- [ ] Onion skin shows bunching at the slow end, gaps at the fast end.
- [ ] Fast moves have at least one wide gap (no universal ease).

Related: `creative-arts.animation.principles.applying-timing-and-spacing`,
`creative-arts.animation.principles.inbetweening-to-charts`.
