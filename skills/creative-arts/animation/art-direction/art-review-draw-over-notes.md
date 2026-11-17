---
id: creative-arts.animation.art-direction.art-review-draw-over-notes
name: art-review-draw-over-notes
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, art-review, paintover-notes, draw-over, feedback]
level: practitioner
status: draft
description: "Give art notes as draw-overs on the artist's own frame: separate layer, one colour per note type, numbered callouts and a before/after toggle, kept small and specific."
sources:
  - https://animationguild.org/
  - https://www.khanacademy.org/computing/pixar
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Art review draw-over notes

Goal: a note the artist understands in five seconds and can execute without guessing.

## 1. Mechanics
- Always draw on a copy or overlay layer, never the artist's working file. Export a flattened image named
  with the shot/asset and version (`seq03_sh020_v004_note01.png`).
- Colour code: e.g. red = must fix, yellow = suggestion, cyan = composition and lines.
- Number each callout and write the matching numbered sentence beside it.
- Provide a before/after pair or an A/B flip in the review tool.

## 2. What to draw
- Draw the change roughly: a value block, a pushed silhouette, an arrow for light direction.
- For colour notes, paint a swatch of the target colour next to the area, sampled from the palette.
- For composition, redraw the big shapes and the eye path; ignore detail.

## 3. What to avoid
- Repainting the whole frame replaces the artist's judgement and hides which change matters.
- Ten notes in one image: split into separate draw-overs by priority.

## 4. Record
- Attach the draw-over to the version in the tracker; the next version references the note numbers it fixes.

## Verify
- [ ] Each callout numbered and paired with a sentence.
- [ ] Must-fix vs suggestion distinguishable at a glance.
- [ ] Draw-over attached to the exact version reviewed.

Related: `creative-arts.animation.art-direction.actionable-visual-feedback`,
`creative-arts.animation.pipeline.dailies-review`.
