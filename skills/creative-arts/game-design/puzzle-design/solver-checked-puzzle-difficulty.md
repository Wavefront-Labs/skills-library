---
id: creative-arts.game-design.puzzle-design.solver-checked-puzzle-difficulty
name: solver-checked-puzzle-difficulty
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-solver, automated-solving, state-space-search, unique-solution]
level: practitioner
status: draft
description: "Use a solver to check puzzles: BFS state search for solvability and shortest solution, uniqueness checks, difficulty metrics and catching unintended shortcuts."
sources:
  - https://www.puzzlescript.net/Documentation/documentation.html
  - https://en.wikipedia.org/wiki/Breadth-first_search
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solver-checked puzzle difficulty

**Goal:** prove every puzzle is solvable, find unintended shorter solutions, check
uniqueness where required (logic puzzles), and get objective difficulty signals.

## What a solver tells you
| Check | Method |
|---|---|
| Solvable | search reaches a goal state |
| Shortest solution length | breadth-first search (BFS) depth |
| Unintended solutions | compare found solutions to the intended one |
| Uniqueness (Sudoku, nonograms) | search for a second solution; must not exist |
| State-space size | states explored; rough complexity |
| Dead ends | number of reachable states from which no solution exists (Sokoban deadlocks) |

## Building a simple BFS solver (grid push puzzle)
```
from collections import deque
def solve(start, moves, is_goal, step):
    seen = {start}; q = deque([(start, [])])
    while q:
        s, path = q.popleft()
        if is_goal(s): return path
        for m in moves:
            n = step(s, m)
            if n is not None and n not in seen:
                seen.add(n); q.append((n, path + [m]))
    return None   # unsolvable
```
State must be hashable and canonical (player position plus sorted box positions).
Prune deadlocks (box in a non-goal corner) to keep search tractable.

## Logic puzzles
- Uniqueness: run the solver to find all solutions up to two; more than one is a broken puzzle.
- Grade by the techniques required: a solver that applies human techniques in order of
  difficulty (singles, pairs, X-wing in Sudoku) grades by the hardest needed.

## Interpreting difficulty
- Solution length and state count correlate weakly with human difficulty. Human
  difficulty comes from the insight required, misleading options and the number of
  plausible wrong paths. Use solver data with fresh-player solve times, not instead of them.
- A puzzle whose shortest solution is far shorter than intended skips the lesson: fix the
  layout.

## Workflow
1. Export level data to the solver in CI or a script.
2. Fail the build if any puzzle is unsolvable or a logic puzzle is non-unique.
3. Report shortest-solution length per puzzle next to intended length.
4. PuzzleScript games can be tested in the editor; many designers write a solver for their own engine.

## Gotchas
- Real-time or physics puzzles need discretised states or simulation sampling; the BFS
  approach only fits discrete puzzles.
- State explosion: add canonicalisation and pruning before giving up.

## Verify
- [ ] Solver confirms every puzzle solvable.
- [ ] No unintended shortest solutions remain unreviewed.
- [ ] Logic puzzles verified unique.
