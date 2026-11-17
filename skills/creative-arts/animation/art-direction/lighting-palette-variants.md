---
id: creative-arts.animation.art-direction.lighting-palette-variants
name: lighting-palette-variants
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, color-styling, palette-variants, color-models, night-palette, lighting-states]
level: advanced
status: draft
description: "Create lighting palette variants of colour models (day, dusk, night, interior, special) so characters and props stay recognisable while belonging to each lighting state."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740797712
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lighting palette variants

Goal: each character and prop has a tested colour model for every lighting state in the show, so painters and
ink-and-paint never invent colours shot by shot.

## 1. Define the states
- Typical set: day exterior, overcast, dusk/golden, night exterior, interior warm (tungsten),
  interior cool (fluorescent/screen), plus specials (fire, underwater, flashback).
- Each state gets a written light colour, shadow colour, ambient and contrast level, from the color script.

## 2. Derive variants from the base model
- Start from the neutral (daylight, normal) model. For each state, shift the base colours, don't repaint
  from scratch:
  - Apply the state's light colour (multiply/overlay at a fixed opacity) and its value shift.
  - Re-check hue identity: key recognisable colours (hero's red jacket) must still read as that hue.
  - Night: lower value and saturation, shift toward blue-violet, but keep a value gap between skin,
    hair and clothing so the character still reads.
- Record every variant swatch with values; name them `char_mia_night_lit`, `char_mia_night_shadow`.

## 3. Test in context
- Drop each variant onto a BG of that state; check separation and that the character feels lit by the BG.
- Present all states as a grid on one sheet for approval.

## Failure modes
- Night models that are just darker: muddy, flat; add the hue shift and keep the value gaps.
- Variants made per shot: inconsistent across episodes.

## Verify
- [ ] State list with light/shadow/ambient colours written.
- [ ] Each character has a swatch set per state.
- [ ] Hero identity colours still read in every state.

Related: `creative-arts.animation.art-direction.master-palette-specification`,
`creative-arts.animation.art-direction.character-background-separation`,
`creative-arts.animation.art-direction.color-script`.
