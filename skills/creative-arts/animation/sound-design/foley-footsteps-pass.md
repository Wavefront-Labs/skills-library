---
id: creative-arts.animation.sound-design.foley-footsteps-pass
name: foley-footsteps-pass
category: creative-arts
field: animation
product: sound-design
tags: [foley-footsteps, foley, footsteps, feet-pass, foley-pit, surfaces, shoes, contact-frames, sync]
level: practitioner
status: draft
description: "Record or build the footsteps pass for an animated scene: surfaces and shoes per character, sync to contact frames, gait and weight, and variation so steps never repeat."
sources:
  - https://www.routledge.com/The-Foley-Grail-The-Art-of-Performing-Sound-for-Film-Games-and-Animation/Ament/p/book/9780367420819
  - https://www.reaper.fm/userguide.php
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Footsteps pass

**Goal:** every on-screen footfall has a step that matches the character's weight, shoe and surface, on the
contact frame.

## Plan from the animation

1. Make a **footsteps cue list** per scene: character, shoe type (sneaker, heel, boot, bare, robot foot), surface
   (concrete, wood, gravel, metal grating, carpet), gait (walk, run, sneak, stumble).
2. Mark contact frames from the animation (heel strike for a walk); in animation these are exact, so mark them
   from the shot files or by stepping through the cut.

## Recording (foley stage or home pit)

- Surfaces in pits or on boards: concrete slab, plywood on a frame, gravel tray, carpet offcut, metal sheet.
- Mic 1-1.5 m away, cardioid or shotgun, slightly off-axis to the feet; record at 48 kHz/24-bit with plenty of headroom
  (heels peak hard).
- Perform to picture with the character: the foley artist walks in place watching the screen. Do one character per
  pass, one track per character.

## Building from library (budget pipelines)

- Use a library of single steps (not loops) per shoe/surface, 6-10 variants each.
- Place each step on the contact frame, alternate variants, randomise pitch +/- 50-100 cents and level +/- 2 dB.
- Reaper: a script or *Item > Item processing* random pitch per item; or the stylized-series tooling in
  `creative-arts.animation.sound-design.sfx-design`.

## Craft

- Weight: heavier characters get more low end and a second "settle" layer.
- Cartoon walks may want stylised steps (wood blocks, xylophone "tiptoe") per show style
  (see `creative-arts.animation.sound-design.cartoon-sfx-vocabulary`).
- Off-screen and far characters: lower level and less high end, not removed.

## Verify

Mute everything but feet: each step lands on the contact frame within a frame, no two consecutive steps are the
same sample, and each character is identifiable by footsteps alone. Cut and fit in
`creative-arts.animation.sound-design.foley-design`.
