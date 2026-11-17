---
id: creative-arts.game-design.level-design.level-structures-linear-loop-hub
name: level-structures-linear-loop-hub
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, level-layout, level-flow, level-loops, hub-structure, hub-and-spoke, linear-levels, branching-paths, critical-path]
level: practitioner
status: draft
description: "Choose a level's macro structure (linear, branching, loop, hub-and-spoke, open) to fit pacing and exploration goals, and diagram it as a node graph before blockout."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Level structures: linear, loop, hub

**Goal:** pick the macro shape of a level deliberately, because structure determines
pacing control, exploration, backtracking and how lost players get.

## Structures
| Structure | Shape | Strengths | Risks |
|---|---|---|---|
| Linear | A -> B -> C | tight pacing, authored set pieces | feels like a corridor |
| Linear with side pockets | main line + dead-end optional rooms | rewards curiosity cheaply | dead ends feel like wasted walks without rewards |
| Branching | forks that rejoin | choice of approach | content seen by fewer players |
| Loop | path returns to start via a different route | no backtracking, shortcuts | needs careful landmarking |
| Hub and spoke | central hub to several branches | player chooses order; clear home base | hub travel tedium |
| Open / sandbox | many connections, few constraints | freedom | weak pacing control, getting lost |
| Metroidvania network | interconnected, ability-gated | discovery, mastery of space | heavy backtracking without fast travel |

## Procedure
1. State the level's **goals**: pacing (authored vs player-driven), exploration amount,
   replay value, combat style.
2. **Draw a node graph** (rooms as nodes, connections as edges); mark the critical path,
   optional nodes, one-way doors, gates and shortcuts.
3. Check **flow**: is there a route back after the goal (loop or shortcut) or does the
   player have to retrace?
4. Mark **landmarks** visible from multiple nodes for orientation in loops/hubs.
5. Only then move to a top-down paper map and blockout.

## Gotchas
- Pure linear levels with no side pockets can feel railroaded; pure open levels lose
  pacing. Most good levels mix (linear spine, looping pockets).
- Dead ends must pay off (item, view, lore) or be signposted as dead ends.
- Hubs need fast travel or very short spokes once revisits become common.

## Verify
- [ ] Structure chosen with goals stated.
- [ ] Node graph drawn with critical path, optional content, gates, shortcuts.
- [ ] Return route after the objective exists or retracing is intentional.
