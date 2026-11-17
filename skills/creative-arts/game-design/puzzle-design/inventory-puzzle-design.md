---
id: creative-arts.game-design.puzzle-design.inventory-puzzle-design
name: inventory-puzzle-design
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, inventory-puzzles, adventure-game-puzzles, point-and-click, item-combination, moon-logic, lock-and-key, ron-gilbert]
level: practitioner
status: draft
description: "Design point-and-click inventory puzzles: logical item uses, motivated goals before solutions, combination limits, feedback on wrong tries, and avoiding moon logic and dead ends."
sources:
  - https://grumpygamer.com/why_adventure_games_suck
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inventory puzzle design

**Goal:** item-based puzzles where the solution feels clever in hindsight, not arbitrary,
and players are never stuck because the game misled them.

## Principles (several from Ron Gilbert's 1989 "Why Adventure Games Suck")
1. **Goal before solution:** the player should know what they're trying to do before
   finding the item that does it (or at least recognise the goal when they have the
   item). Gilbert lists "puzzles that don't advance the story" and "backwards puzzles"
   among the problems.
2. **Logical use:** the item's real-world or established in-world properties suggest
   its use. A rubber chicken with a pulley in the middle is a famous joke precisely
   because it's absurd - use absurdity knowingly.
3. **No unwinnable states without warning** (Gilbert: avoid dying or getting stuck
   without knowing).
4. **Reward experimentation:** wrong combinations get characterful responses that hint
   at what is missing ("It's too dull to cut the rope").
5. **Limit the search space:** a large inventory x many hotspots makes "try everything"
   the dominant strategy; prune inventory as items get used.
6. **Clear interactables:** hotspots readable (hover highlights, hotspot reveal key).

## Procedure
1. Chart the puzzle dependencies (see `creative-arts.game-design.puzzle-design.puzzle-dependency-charts`).
2. For each item use, write the **justification** in one sentence; if you can't, the
   puzzle may be moon logic.
3. Write wrong-use responses for likely attempts.
4. Test with players unfamiliar with the game; log every "try everything" moment.
5. Add hints or reconsider puzzles where most testers brute-force.

## Gotchas
- Pixel hunting (tiny hotspots) is not a puzzle.
- Multi-step combinations with no feedback between steps are frustrating.
- Cultural knowledge (puns, idioms) doesn't localise; avoid or adapt per language.

## Verify
- [ ] Every item use has a one-sentence justification.
- [ ] Goals are established before or at item discovery.
- [ ] Wrong-use responses written for likely attempts.
- [ ] No unwarned unwinnable states.
