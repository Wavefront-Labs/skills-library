---
id: creative-arts.animation.production-design.costume-change-tracking
name: costume-change-tracking
category: creative-arts
field: animation
product: production-design
tags: [production-design, costume-design, costume-continuity, continuity, wardrobe-plot]
level: practitioner
status: draft
description: "Track costume changes across a production: a wardrobe plot by scene, change and damage states, asset variants and checks so characters never switch outfits by accident."
sources:
  - https://animationguild.org/
  - https://en.wikipedia.org/wiki/Costume_design
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Costume change tracking

Goal: every shot uses the correct outfit and state for that point in the story.

## 1. Wardrobe plot
A grid with scenes (in story order) as columns and characters as rows; each cell names the costume and
state. Mark story days: a costume can only change between days or at a motivated change.

## 2. States
- Name variants explicitly: `mia_jacket_A_clean`, `mia_jacket_A_torn`, `mia_jacket_A_wet`.
- Progressive damage (dirt, tears, soot) is cumulative; once torn it stays torn until a change.
- Accessories (hat on/off, bag) tracked like costumes.

## 3. Pipeline link
- Each state is an asset variant or a rig switch in CG, or a model sheet in 2D.
- Shot breakdowns reference the variant ID; layout/animation load the right one automatically where possible.

## 4. Checks
- At story reel and at lighting, run the wardrobe plot against the cut: every shot's variant matches its scene.
- Watch flashbacks and out-of-order production; most errors happen when a shot is made before the
  scenes around it.

## Verify
- [ ] Wardrobe plot covers every scene and character.
- [ ] Damage states cumulative and named.
- [ ] Shot variants checked against the plot.

Related: `creative-arts.animation.production-design.costume-design`,
`creative-arts.animation.editorial.continuity-supervision`,
`creative-arts.animation.pipeline.character-consistency`.
