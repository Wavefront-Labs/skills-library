---
id: creative-arts.game-design.level-design.shortcuts-and-backtracking
name: shortcuts-and-backtracking
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, shortcuts, backtracking, level-flow, one-way-doors, unlockable-shortcuts, loop-design, interconnected-world]
level: practitioner
status: draft
description: "Design unlockable shortcuts and planned backtracking: one-way doors and ladders that loop back to checkpoints, re-using space with new purpose, and reducing retrace tedium."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shortcuts and backtracking

**Goal:** levels that loop back on themselves so progress feels like mastering a place,
and returning through old space is quick and changed rather than tedious.

## Unlockable shortcuts
Pattern popularised by interconnected action-RPGs: the player pushes forward through a
long, dangerous route, then opens a one-way door, kicks down a ladder or lowers a lift
that connects back to a checkpoint/safe point.
- **One-way first:** the shortcut is visible but locked from the start side (player sees
  the locked door early and later realises where they are - a moment of spatial
  understanding).
- **Placement:** after a significant challenge and before the next one, so the
  checkpoint-to-new-area route becomes short.
- **Signal:** a distinct visual language for "opens from the other side".

## Planned backtracking
- **Change the space on return:** new enemies, flooded/destroyed areas, lighting or
  time-of-day changes, new traversal ability opening new routes.
- **Shorten the return:** shortcuts, faster traversal unlocked, fewer enemies on the
  way back.
- **Reward the return:** previously unreachable items now accessible (see
  `creative-arts.game-design.level-design.metroidvania-ability-gating`).

## Procedure
1. On the node graph, mark the checkpoint and each long route; add a shortcut edge back
   once the route exceeds the target replay time.
2. For each retraced segment, list what is new on the return trip; if nothing, add a
   shortcut or change.
3. Playtest: time return trips; watch for "where was that again?" confusion; add
   landmarks.

## Gotchas
- Too many shortcuts make the level a flat network with no sense of depth.
- Shortcut doors that look like ordinary locked doors (which need keys) confuse players.
- Backtracking without a map in large spaces frustrates; provide a map or strong landmarks.

## Verify
- [ ] Every long route has a shortcut to the nearest checkpoint or a reason not to.
- [ ] Retraced segments have something new or are short.
- [ ] One-way doors are visually distinct and seen before they open.
