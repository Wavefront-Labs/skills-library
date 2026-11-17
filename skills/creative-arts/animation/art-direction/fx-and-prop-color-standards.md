---
id: creative-arts.animation.art-direction.fx-and-prop-color-standards
name: fx-and-prop-color-standards
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, color-styling, fx-color-standards, effects, props, palette]
level: practitioner
status: draft
description: "Set colour standards for effects and props: consistent hues for magic, fire, water, energy and hero props, how FX glow relates to scene light, and reserved story colours."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740797712
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Effects and prop color standards

Goal: a fireball, a spell or the hero's sword looks like the same thing every time it appears.

## 1. FX colour sheet
For each recurring effect, specify:
- **Core / mid / edge** colours (e.g. fire: near-white yellow core, orange mid, deep red edge, dark smoke).
- **Value**: FX that emit light are the brightest thing in their area; set the core value relative to
  the scene's white point.
- **Glow**: colour and falloff; whether it lights characters and set (cast colour on nearby surfaces).
- **Night/day variants**: emissive FX look brighter and more saturated at night; keep the hue.
- **Line treatment** for 2D FX (coloured lines, no lines, line colour).

## 2. Story-reserved colours
- Assign colours with meaning (villain's magic = acid green) and keep them out of BGs and costumes.
- Write the list in the palette spec so painters don't use those hues casually.

## 3. Props
- Hero props have fixed colour models with lit/shadow per lighting state, like characters.
- Background props follow environment palettes and stay lower in saturation than hero props.

## 4. Interaction rules
- FX light on characters: state whether it is painted (2D tone/shadow change) or lit (CG light linked).
- Water and transparent FX: specify how much BG shows through and the tint.

## Verify
- [ ] Each recurring effect has a core/mid/edge spec and glow rule.
- [ ] Reserved story colours listed and absent elsewhere.
- [ ] Hero props have colour models per lighting state.

Related: `creative-arts.animation.art-direction.master-palette-specification`,
`creative-arts.animation.production-design.hero-vs-background-props`.
