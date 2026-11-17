---
id: creative-arts.game-design.level-design.teaching-mechanics-through-levels
name: teaching-mechanics-through-levels
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, implicit-tutorial, teaching-through-design, safe-introduction, world-1-1, wordless-tutorial, affordances, onboarding]
level: practitioner
status: draft
description: "Teach mechanics wordlessly through level layout: introduce each mechanic in a safe space, force or invite its use, then test it under pressure (the World 1-1 approach)."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Teaching mechanics through levels

**Goal:** players learn mechanics by playing a level built to teach them, with little or
no text.

Super Mario Bros. World 1-1 is the canonical example: the first enemy approaches on
open ground, and the first question block sits where a curious player jumps into it.
Shigeru Miyamoto has discussed how the opening was designed to teach the game's basics
through layout.

## The safe-introduction pattern
1. **Isolate:** present the new mechanic or element alone, in a space where failure is
   impossible or cheap (pit-free ground under the first jump).
2. **Invite or force:** layout makes using it the natural action (the only way forward
   is up the wall; the gap is just wider than walking can cross).
3. **Confirm:** clear feedback when used correctly (sound, reward, door opens).
4. **Repeat with a small variation** soon after.
5. **Test under pressure:** later, use it with a fail state or combined with other
   mechanics (see `creative-arts.game-design.level-design.kishotenketsu-mechanic-arcs`).

## Techniques
- **Gating geometry:** the space cannot be passed without the new skill.
- **Observation first:** show an NPC or enemy using the mechanic before the player
  needs it.
- **Affordance cues:** visual language marks what to interact with (see
  `creative-arts.game-design.level-design.colour-coding-and-visual-language`).
- **Low-cost failure loops:** fall into a shallow pit that returns you to the start of
  the lesson rather than killing.

## Procedure
1. List mechanics in teaching order (from the onboarding plan).
2. For each, sketch the teaching space: isolate, invite, confirm, repeat, test.
3. Playtest with new players **without any prompts**; note where they hesitate or fail.
4. Add text prompts only where layout alone fails after iteration (and make them
   contextual and brief).

## Gotchas
- Teaching spaces that are too obvious bore experts; keep them short.
- If a player can bypass the lesson by accident, later sections relying on it fail;
  gate key lessons.
- Two new mechanics in one teaching space split attention.

## Verify
- [ ] Each mechanic has a safe introduction space.
- [ ] New players pass each lesson without text in most cases.
- [ ] Lessons cannot be bypassed where later content depends on them.
