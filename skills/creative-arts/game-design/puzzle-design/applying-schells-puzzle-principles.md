---
id: creative-arts.game-design.puzzle-design.applying-schells-puzzle-principles
name: applying-schells-puzzle-principles
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, schell-puzzle-principles, puzzle-critique, art-of-game-design]
level: practitioner
status: draft
description: "Critique and fix a puzzle against Schell's ten puzzle principles: clear goal, easy start, progress, solvability, ramp, parallelism, pyramid, hints, answer, perceptual shifts."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://grumpygamer.com/why_adventure_games_suck
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Applying Schell's ten puzzle principles

**Goal:** a repeatable review pass for any puzzle, using the principles from chapter 14 of
Schell's *The Art of Game Design*.

## The ten principles as review questions
| # | Principle | Ask | Typical fix |
|---|---|---|---|
| 1 | Make the goal easily understood | Can a tester state the goal in one sentence after 10 s? | show the target state (picture on the box, locked door with a visible slot) |
| 2 | Make it easy to get started | Is the first action obvious? | one clearly interactive element; a free first move |
| 3 | Give a sense of progress | Does the player see they are closer? | partial feedback: lights, clicks, segments filling |
| 4 | Give a sense of solvability | Does the player believe it is solvable without trickery? | show all needed pieces in view; consistent rules |
| 5 | Increase difficulty gradually | Is this puzzle one step beyond the last? | add an intro version earlier |
| 6 | Parallelism lets the player rest | Is there something else to do when stuck? | two or three open puzzles at once |
| 7 | Pyramid structure extends interest | Do small puzzles feed a bigger one? | sub-puzzle answers combine into a meta answer |
| 8 | Hints extend interest | Is there a hint path before frustration? | tiered hints |
| 9 | Give the answer! | Can a player who gives up see the answer and still get the aha? | reveal/solution option |
| 10 | Perceptual shifts are a double-edged sword | Does it rely on a single insight? | add multiple routes to the insight, or accept that some players will be shut out |

## Procedure
1. Play-test the puzzle with 3-5 fresh players, silent observation.
2. Score each principle 0-2 for the puzzle with evidence from the sessions.
3. Fix the lowest scores first; principles 1, 2 and 4 failures usually explain most quits.
4. Re-test with new players (people who solved it cannot test it again).

## Notes
- Principle 10 is where "moon logic" lives (Gilbert's *Why Adventure Games Suck*): one
  unexpected insight with no clues. Give at least two clues pointing at the shift.
- Principles 6 and 7 are structural; review the whole puzzle chain, not one puzzle.

## Verify
- [ ] Every puzzle scored on all ten principles with session evidence.
- [ ] No puzzle scores 0 on principles 1, 2 or 4.
- [ ] Fixed puzzles re-tested with fresh players.
