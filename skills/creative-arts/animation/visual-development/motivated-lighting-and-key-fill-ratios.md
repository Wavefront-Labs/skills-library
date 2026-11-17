---
id: creative-arts.animation.visual-development.motivated-lighting-and-key-fill-ratios
name: motivated-lighting-and-key-fill-ratios
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-properties, motivated-lighting, key-fill-ratio, lighting-design, three-point-lighting]
level: practitioner
status: draft
description: "Design motivated lighting: every light traced to a source in the world, with key-to-fill ratios chosen for mood, translated from paint to CG lighting."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Three-point_lighting
  - https://en.wikipedia.org/wiki/Key_light
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motivated lighting and key-fill ratios

Goal: lighting that feels natural because every light has a believable source, and a
contrast level chosen for the emotion.

## Motivation
- Each light in a key painting or CG scene answers "what emits this?": sun, window, lamp,
  screen, fire, bounce from a wall.
- Cheats are allowed (a little extra fill, a rim to separate a character) if they feel
  plausible within the world.

## Key-to-fill ratio (contrast)
| Ratio (key:fill) | Look | Typical use |
|---|---|---|
| 2:1 | low contrast, soft | comedy, daytime, upbeat TV |
| 4:1 | moderate | drama, naturalistic |
| 8:1 and up | high contrast, chiaroscuro | noir, horror, intense drama |
Ratios are in light intensity; one stop (2x) per doubling.

## Method
1. List the sources in the set from the layout/key (with colour and size).
2. Choose the key source for each shot and the mood ratio.
3. Place fill from a motivated secondary (sky, bounce wall, second lamp).
4. Add accents (rim, kicker, practical glow) only where motivated or for clear separation.
5. Document per sequence for lighting artists: source list, ratio, colour temperatures.
6. Check continuity across shots: the key may cheat position between angles but keeps
   colour and side.

## Failure modes
- Unmotivated multi-colour rim lights everywhere.
- Same ratio for every mood.
- Key flipping sides between shots in one scene.

## Verify
- [ ] Every light linked to a source.
- [ ] Ratio matches the intended mood.
- [ ] Key side and colour consistent across the sequence.

Related: `creative-arts.animation.visual-development.lighting-keys-per-sequence`,
`creative-arts.animation.blender.lighting`.
