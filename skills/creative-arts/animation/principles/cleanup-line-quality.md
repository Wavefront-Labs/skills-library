---
id: creative-arts.animation.principles.cleanup-line-quality
name: cleanup-line-quality
category: creative-arts
field: animation
product: principles
tags: [animation, hand-drawn-pipeline, cleanup-animation, cleanup, line-quality, line-weight, closed-lines, ink-and-paint, 2d, toon-boom]
level: practitioner
status: draft
description: "Clean up animation drawings to final line: consistent line weight, closed shapes for paint, color-trace lines, and keeping lines from boiling between frames."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cleanup line quality

Goal: turn tie-downs into final line art that is consistent frame to frame and ready for paint.

## Standards to set (from the cleanup supervisor/model)
- **Line weight**: uniform (most TV), or tapered with thick-thin (feature). Specify brush size per
  resolution and per character size on screen.
- **Closure**: all paint areas closed, no gaps (or gaps closed with invisible lines).
- **Color trace / tone lines**: shadow and highlight boundaries drawn as colored lines (often
  red/blue/green) for the painters; separate layer.
- **Detail level by size**: simplify details on small or distant characters.

## Method
1. Work on a new layer over the tie-down.
2. Draw in long, confident strokes; avoid hairy, sketchy lines.
3. Match line placement to the previous cleaned drawing - flip constantly.
4. Close all paint zones; check with a test fill.
5. Shadow/tone lines on a separate layer (Toon Boom Harmony: Line Art vs Colour Art layers;
   other tools: separate layer named by convention).
6. Inbetweens cleaned with the same weight; inbetweener follows charts precisely.

## Boiling
"Boiling" is lines wobbling between frames on holds or slow moves. Avoid on holds by
**re-using the same drawing** (hold the exposure) instead of redrawing. On slow moves,
trace carefully from the neighbour drawings. Use it deliberately only as a style (e.g. for
a hand-made look).

## Failure modes
- Inconsistent weights between artists - fix with written specs and a sample sheet.
- Gaps causing paint leaks.
- Over-detailing distant characters.

## Verify
- [ ] Test fill: no leaks.
- [ ] Flipping: no unintended boiling.
- [ ] Line weights match the spec sheet.

Related: `creative-arts.animation.principles.tie-down-drawings`,
`creative-arts.animation.principles.inbetweening-to-charts`.
