---
id: creative-arts.game-design.puzzle-design.puzzle-hunts-and-metapuzzles
name: puzzle-hunts-and-metapuzzles
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-hunt, meta-puzzle, metapuzzles, hunt-structure]
level: practitioner
status: draft
description: "Design puzzle hunts and metapuzzles: answer extraction, metas built from feeder answers, round structure, unlock schedules, test-solving and answer checking."
sources:
  - https://puzzles.mit.edu/
  - https://www.puzzledpint.com/
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Puzzle hunts and metapuzzles

**Goal:** a set of puzzles whose answers feed metapuzzles, structured into rounds that
teams can solve in parallel (MIT Mystery Hunt, Puzzled Pint, Galactic Puzzle Hunt).

## Answer extraction
Hunt puzzles end in a word or phrase. Common extraction methods:
- Index into answers (3rd letter of each).
- Ordering by a given clue (alphabetical, by number on the page).
- Letters highlighted by the solving process (circled squares in a crossword).
- Flavour text hints the mechanism; keep flavour precise.

## Metapuzzles
A meta uses the round's feeder answers as input:
1. Choose the meta answer first; then a mechanism; then the feeder answers that make it work.
2. Feeder answers must look natural as answers of their own puzzles.
3. Allow solving the meta with a few answers missing (around 60-80% of feeders),
   so teams can backsolve the rest.
4. Give the meta a clear "aha" mechanism that clicks when spotted.

## Structure
| Element | Notes |
|---|---|
| Rounds | 6-12 feeders + meta per round, themed |
| Unlocks | solving N puzzles unlocks more; time-based unlocks keep slow teams moving |
| Parallelism | multiple open puzzles at all times (Schell principle 6) |
| Finale | a final meta of metas or a physical runaround |

## Production
1. **Test-solve every puzzle** with people who have not seen it, at least twice.
2. Record solve times; adjust unlock pacing to expected team speeds.
3. **Answer checker:** normalise answers (case, spaces, punctuation) and add intermediate
   "keep going" responses for common partial answers.
4. Errata process during the hunt; announce corrections to all teams.
5. Publish solutions after the hunt, with author notes.

## Gotchas
- Ambiguous extraction steps (which order?) are the top complaint; test specifically for them.
- Puzzles requiring niche knowledge need it to be searchable.
- A broken meta wastes a round; test-solve metas with the feeders hidden.

## Verify
- [ ] Every puzzle test-solved twice by fresh solvers.
- [ ] Metas solvable with a fraction of feeders.
- [ ] Answer checker normalises and gives partial-answer feedback.
