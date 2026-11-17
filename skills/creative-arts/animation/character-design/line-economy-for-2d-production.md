---
id: creative-arts.animation.character-design.line-economy-for-2d-production
name: line-economy-for-2d-production
category: creative-arts
field: animation
product: character-design
tags: [character-design, design-for-animation, line-economy, 2d-production, simplification, cleanup]
level: practitioner
status: draft
description: "Design for 2D production with line economy: minimise lines, colours and detail that must be redrawn every frame, and budget detail by shot type."
sources:
  - https://books.google.com/books?vid=ISBN9780823023493
  - https://books.google.com/books?vid=ISBN9781560100843
  - https://animationguild.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line economy for 2D production

Goal: a character that can be drawn thousands of times on a TV schedule without drift.
Every line in a design is drawn by an animator, an assistant and an inbetweener in every
frame; detail has a cost per frame.

## Rules
- **Count lines**: fewer than a target number per character (TV designs often aim for
  tens of lines, not hundreds). Remove folds, stitching, patterns that do not carry story.
- **Colour zones**: each zone needs a closed shape for ink-and-paint; fewer zones =
  faster paint and fewer gaps. Avoid tiny islands of colour.
- **Patterns**: no plaids, stripes or prints on moving cloth unless handled as textures
  in compositing.
- **Shadows**: decide the shadow rule (none, one tone, hard-edged tone lines) and design
  forms where shadow shapes are simple.
- **Symmetry and rotation**: features that look the same from many angles are cheap;
  asymmetric details flipping sides on turns are expensive.
- **Detail by shot size**: define a reduced version for wide shots.

## Method
1. Count lines and colour zones on the approved design.
2. Remove or merge detail until counts hit the production budget; keep the identity features.
3. Draw a timed test: how long to redraw the character on model? Compare to schedule.
4. Draw the wide-shot simplification.
5. Hand to the cleanup lead for a cleanup-cost review.

## Failure modes
- Pitch-art design carried into production unchanged.
- Gaps between lines that do not close, breaking paint fill.
- Detail that disappears in some shots and reappears in others.

## Verify
- [ ] Line and colour-zone counts within budget.
- [ ] Timed redraw meets schedule.
- [ ] Wide-shot version approved.

Related: `creative-arts.animation.principles.cleanup-line-quality`,
`creative-arts.animation.character-design.iconic-and-simple-characters`.
