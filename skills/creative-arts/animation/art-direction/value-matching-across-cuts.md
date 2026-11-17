---
id: creative-arts.animation.art-direction.value-matching-across-cuts
name: value-matching-across-cuts
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, visual-continuity, value-matching, value, exposure, editing]
level: practitioner
status: draft
description: "Match values across cuts so eyes don't jump or flash: focal brightness, black and white points, and the luminance of the area the audience is looking at on either side of the cut."
sources:
  - https://books.google.com/books?vid=ISBN9781138014152
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Continuity_editing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Value matching across cuts

Goal: across a cut, the audience's eye lands on the new subject at a similar brightness, unless a jolt is
intended.

## 1. Match the area of attention
- Find where the eye is at the end of shot A (usually the subject's face) and where it should be at the
  start of shot B. Keep those areas at similar luminance and close in screen position.
  Large differences make the cut feel like a flash.
- Block calls this tonal continuity; contrast across the cut is a choice for shock or a beat change.

## 2. Check black and white points
- Waveform both shots: black level and the brightest significant highlight should be similar in the same
  scene. A wide shot with a hot sky followed by a dim close-up feels like an exposure change.

## 3. Average key
- The overall average luminance of adjacent shots in a scene should be close; a quick check is to
  blur both frames heavily and compare the grey.

## 4. Fix order
- Lighting first (fill level, sky intensity), then compositing (background lift, vignette), then grade trims.
- For 2D, repaint or adjust BG levels to match the reference frame.

## 5. Intentional contrast
- Cut from dark to bright for a reveal, shock or time jump; plan it in the color script.

## Verify
- [ ] Focal areas across each cut are within about one value step.
- [ ] Black/white points consistent in the scene on the waveform.
- [ ] Any tonal jump is intentional and noted.

Related: `creative-arts.animation.storyboarding.tonal-contrast`,
`creative-arts.animation.art-direction.shot-to-shot-color-continuity`.
