---
id: creative-arts.game-design.puzzle-design.puzzle-sequencing-and-teaching-ramp
name: puzzle-sequencing-and-teaching-ramp
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-sequencing, teaching-ramp, difficulty-curve, mechanic-introduction]
level: practitioner
status: draft
description: "Sequence puzzles into a teaching ramp: one new rule per puzzle, develop, combine, twist; track it in a rule-by-puzzle matrix and test the order with fresh players."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Puzzle sequencing and the teaching ramp

**Goal:** each puzzle teaches or tests exactly one new idea, so players feel clever and
never lost (Portal, The Witness, Baba Is You, Snakebird).

## The pattern per mechanic
1. **Introduce:** the new rule in isolation, trivially, with no failure possible.
2. **Develop:** a puzzle where the rule must be used deliberately.
3. **Combine:** the rule with one previously learned rule.
4. **Twist:** an unexpected consequence of the rule (the "aha"), often a perceptual shift.
5. **Test / master:** a harder puzzle using several rules; optional or end of chapter.

This mirrors the kishotenketsu structure used by Nintendo levels.

## Rule x puzzle matrix
| Puzzle | portal | momentum | cube | laser | new |
|---|---|---|---|---|---|
| 01 | I | | | | portal |
| 02 | D | | | | |
| 03 | D | | I | | cube |
| 04 | C | | C | | |
| 05 | T | I | | | momentum |
I = introduce, D = develop, C = combine, T = twist. Rules: at most one I per puzzle;
no T before D; each rule gets at least one C before it appears in a mastery puzzle.

## Procedure
1. List every rule, interaction and "trick" the game expects players to know.
2. Build the matrix and the order; spot puzzles with two new things and split them.
3. Mark optional branches (side puzzles) so mastery content does not block progress.
4. Test with fresh players in order; record solve times. A spike in time or a quit marks
   a missing step; insert a bridge puzzle.
5. Re-check the matrix after every reorder; moved puzzles often drag hidden prerequisites.

## Gotchas
- Designers sequence by their own difficulty perception; only fresh-player times count.
- Red herrings in teaching puzzles teach the wrong thing.
- Players who sequence-break (open hubs) need each puzzle self-contained or gated.

## Verify
- [ ] Matrix shows at most one new element per puzzle.
- [ ] Solve-time curve from fresh players has no unexplained spikes.
- [ ] Every rule combined at least once before mastery puzzles.
