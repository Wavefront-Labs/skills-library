---
id: creative-arts.animation.art-direction.sequence-lighting-continuity
name: sequence-lighting-continuity
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, visual-continuity, lighting-continuity, lighting, sequence-lighting]
level: advanced
status: draft
description: "Keep lighting continuous within a sequence: master-shot lighting, shared rigs, key direction relative to set not camera, and cheats that stay invisible across cuts."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Continuity_editing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lighting continuity in a sequence

Goal: the light comes from the same world-space sources in every shot, even when each shot is cheated for
beauty.

## 1. Light the set, then the shot
- Build a **sequence (master) rig**: key, fill, bounce, practicals, sky placed in world space on the set.
- Light the master/establishing shot first and get it approved; every other shot inherits the rig.
- Shot-level lights are added only as named cheats on a separate layer (`shot_rim_cheat`).

## 2. Direction is relative to the set
- When the camera reverses (shot/reverse-shot), a key from screen-left becomes screen-right; that is
  correct. A key that stays screen-left on both sides of a reverse breaks the geography.
- Draw an overhead of the set with the sun/practicals and camera positions; check each shot against it.

## 3. Acceptable cheats
- Adding rim or kicker to separate a character, lifting fill on a close-up, flagging a hot background.
- Keep intensity and colour of the main key within a small range (about plus or minus half a stop);
  change direction only for a motivated reason.

## 4. Progressions
- Time passing within a scene (sunset, storm rolling in) is planned per shot as a curve, so adjacent
  shots step smoothly.

## Verify
- [ ] Sequence rig exists and shots reference it.
- [ ] Overhead with source positions checked for reverses.
- [ ] Cheats are named and limited; key changes under about half a stop between cuts.

Related: `creative-arts.animation.art-direction.shot-to-shot-color-continuity`,
`creative-arts.animation.storyboarding.the-180-degree-rule`,
`creative-arts.animation.editorial.continuity-supervision`.
