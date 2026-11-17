---
id: creative-arts.game-design.puzzle-design.puzzle-dependency-charts
name: puzzle-dependency-charts
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, puzzle-dependency-chart, puzzle-difficulty, parallel-puzzles, adventure-games, escape-room, ron-gilbert, critical-path, dead-ends]
level: practitioner
status: draft
description: "Plan puzzle-heavy games and escape rooms with puzzle dependency charts (Ron Gilbert): nodes, prerequisites, parallel branches, bottlenecks, and checking for dead ends."
sources:
  - https://grumpygamer.com/puzzle_dependency_charts
  - https://grumpygamer.com/why_adventure_games_suck
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Puzzle dependency charts

**Goal:** see the whole puzzle structure at once: which puzzles unlock which, where
players can work in parallel, and where they bottleneck.

Ron Gilbert (Maniac Mansion, Monkey Island) describes puzzle dependency charts on his
blog: work backwards from the goal, with each node a puzzle or item, and arrows showing
what must be done first.

## Build the chart
1. **Start at the end goal** (escape the island / open the vault).
2. **Ask "what do I need to do this?"** and add prerequisite nodes; repeat until you
   reach things available at the start.
3. **Node types:** puzzle/action (box), item/info (oval). Arrows point from prerequisite
   to dependent.
4. **Lay it out top-to-bottom** from start to goal.
```
[start] -> (key) ---------> [open chest] -> (map) --\
[start] -> [talk to guard] -> (password) -----------> [enter tower] -> [goal]
```

## Read it
| Shape | Meaning | Design use |
|---|---|---|
| Wide (many parallel branches) | players have options when stuck | reduces frustration; more to track |
| Narrow (single chain) | linear; one stuck point stops everything | good for story control, risky for stuck players |
| Bottleneck node | many branches converge | good for pacing beats (chapter end) |
| Long chain with no branch | potential frustration | add a parallel task |

## Checks
- **Dead ends:** can the player make an item or state unreachable (use up a needed item,
  close a door permanently)? Gilbert's "Why Adventure Games Suck" argues against games
  that can become unwinnable without warning.
- **Fair signposting:** each item's use is hinted before or when the item is found.
- **Parallelism:** aim for at least two open threads most of the time.

## Gotchas
- Charts drift from the build; update them with every puzzle change.
- Escape rooms use the same chart for flow and for game master hint planning.

## Verify
- [ ] Chart built backwards from the goal; every node reachable from start.
- [ ] No unwarned unwinnable states.
- [ ] Parallel branches at most points; bottlenecks placed deliberately.
