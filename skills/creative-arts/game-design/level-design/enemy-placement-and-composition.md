---
id: creative-arts.game-design.level-design.enemy-placement-and-composition
name: enemy-placement-and-composition
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, enemy-placement, encounter-design, encounter-composition, combat-spaces, enemy-mix, sightlines, approach-options]
level: practitioner
status: draft
description: "Build combat encounters by placing and mixing enemies in a space: roles, sightlines, approach options, introduction order and difficulty budget per encounter."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enemy placement and composition

**Goal:** encounters where enemy mix, positions and the space together create a
tactical problem with more than one good answer.

## Procedure
1. **Encounter brief:** purpose (teach, test, combine, climax), intended difficulty,
   player loadout expected at this point, intended approaches (stealth, ranged, melee).
2. **Choose the mix** by role (see
   `creative-arts.game-design.systems-and-mechanics.enemy-design-archetypes`):
   - Teach: one new enemy type alone, or with familiar fodder.
   - Combine: new type + known types whose combination creates a new problem.
   - Climax: several roles at once, with the space supporting the player.
3. **Place for readability first:** the player should see most threats before they
   engage (vista or entry point overlooking the space).
4. **Positions:**
   - Ranged enemies on high ground or behind cover, with a flank route available.
   - Melee/rushers between the player and ranged enemies, or arriving from a side.
   - Support/healers protected but reachable.
5. **Approach options:** at least two routes (direct, flank, vertical); place cover
   accordingly (see `creative-arts.game-design.level-design.cover-placement-design`).
6. **Difficulty budget:** assign each enemy a cost (e.g. fodder 1, ranged 2, tank 4) and
   cap an encounter's total; scale budget across the level following the intensity
   graph.
7. **Waves vs all-at-once:** waves control intensity but can feel arbitrary if enemies
   spawn behind the player without warning.

## Gotchas
- Enemies placed out of sight that attack immediately feel cheap; give a reveal.
- Identical enemies in a row (corridor of fodder) is filler.
- AI behaviour may not use the space as designed; playtest with real AI, not
  assumptions.

## Verify
- [ ] Encounter brief written (purpose, difficulty, approaches).
- [ ] Enemy mix justified by roles; budget within the cap.
- [ ] Player can observe the space before committing.
- [ ] Playtesters use at least two different approaches across sessions.
