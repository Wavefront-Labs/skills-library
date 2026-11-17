---
id: creative-arts.game-design.puzzle-design.escape-room-flow-structures
name: escape-room-flow-structures
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, escape-room, room-flow, multilinear-puzzles, linear-escape-room, open-escape-room, puzzle-dependency-chart, team-play, nicholson]
level: practitioner
status: draft
description: "Choose an escape room puzzle structure (linear, open, multilinear/path-based) to fit team size and difficulty, and plan room flow, reveals and the finale."
sources:
  - http://scottnicholson.com/pubs/erfacwhite.pdf
  - https://grumpygamer.com/puzzle_dependency_charts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Escape room flow structures

**Goal:** an escape room whose puzzle structure keeps the whole team busy, paces reveals,
and builds to a finale within the time limit (commonly 60 minutes).

Scott Nicholson's 2015 survey of escape room facilities ("Peeking Behind the Locked
Door") describes puzzle organisation as **linear** (one puzzle leads to the next),
**open** (puzzles can be solved in any order, often leading to a meta-puzzle), and
**path-based / multilinear** (several linear paths in parallel that converge).

## Structures compared
| Structure | Team experience | Best for |
|---|---|---|
| Linear | everyone on one puzzle; others idle | small teams, story-driven rooms, beginners |
| Open | many puzzles available; risk of chaos and lost items | experienced players, larger teams |
| Multilinear (paths) | sub-teams work parallel paths, then converge | most commercial rooms; teams of 4-6 |

## Procedure
1. **Set targets:** team size, difficulty, target completion rate (operators often aim
   for a minority-to-half escape rate on standard rooms; set your own), duration.
2. **Draw the dependency chart** (see `creative-arts.game-design.puzzle-design.puzzle-dependency-charts`).
3. **Width:** with N players, aim for roughly N/2 parallel tasks at most times.
4. **Reveals:** new spaces (hidden doors, second room) as reward beats every 15-20 minutes.
5. **Convergence:** paths merge to a meta-puzzle or finale that involves the whole team.
6. **Finale:** a dramatic, short last puzzle with a strong physical/audiovisual payoff.
7. **Item discipline:** mark used items or remove them (a "used items" bin) to reduce
   red-herring confusion in open structures.

## Gotchas
- Red herrings in escape rooms waste limited time and frustrate; Nicholson's survey
  found many operators avoid them or label out-of-play items.
- Search-heavy rooms (hidden keys everywhere) feel tedious; signal search areas.
- Large groups in linear rooms leave people bored.

## Verify
- [ ] Structure chosen for team size; dependency chart drawn.
- [ ] Parallel task count matches team size at most times.
- [ ] Reveals and finale placed on the timeline.
- [ ] Playtest groups' completion times and stuck points recorded.
