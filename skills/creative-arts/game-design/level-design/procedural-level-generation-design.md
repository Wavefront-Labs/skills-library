---
id: creative-arts.game-design.level-design.procedural-level-generation-design
name: procedural-level-generation-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, procedural-generation, procgen, roguelike, room-templates, constraints, seeds, wave-function-collapse, cellular-automata]
level: advanced
status: docs-checked
description: "Design procedural level generation as a level designer: hand-made room templates plus rules, critical-path guarantees, pacing constraints, seeds and validation checks."
sources:
  - https://www.procjam.com/tutorials/
  - https://github.com/mxgmn/WaveFunctionCollapse
  - http://pcgbook.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Procedural level generation design

**Goal:** generated levels that are always completable, well paced and varied, by
combining authored pieces with generation rules a designer controls.

## Common approaches
| Approach | Description | Good for |
|---|---|---|
| Room templates + graph | build a room graph (critical path + branches), fill nodes with authored rooms | action roguelikes; strong authorial control |
| Template chunks with variation | hand-made chunks with randomised internal elements | platformers |
| Wave Function Collapse | generates bitmaps or tilemaps locally similar to an example; tilesets define which tiles may be adjacent | tile-based maps, textures |
| Grammars | rewrite rules for level structure | mission/space structure (the PCG book has a chapter on grammars and levels) |

## Designer procedure
1. **Define invariants** (must always hold): start and exit reachable; required keys
   before locks; no softlocks; maximum length.
2. **Generate structure first** (graph of rooms with roles: start, combat, treasure,
   shop, boss), then geometry.
3. **Pacing rules:** e.g. no two treasure rooms adjacent; rest room before boss;
   difficulty budget rising along the critical path.
4. **Author templates** with tags (size, exits, difficulty, theme) so the generator can
   select; quality comes from these.
5. **Seeds:** deterministic generation from a seed for debugging, sharing and daily
   challenges. Log the seed with every bug report.
6. **Validation pass:** after generation, run path-finding checks (reachability),
   count rewards/enemies against budgets, reject and regenerate on failure.
7. **Batch-test:** generate thousands of levels, collect stats (length, branch count,
   difficulty), and visually review a random sample.

## Gotchas
- "Infinite variety" often reads as sameness; variety must be perceptible and meaningful.
- Pure random placement breaks pacing; constraints matter more than algorithms.
- Generators without validation eventually produce an unwinnable level in front of a
  streamer.

## Checked

2026-11-09. Confirmed against the WaveFunctionCollapse README (generates output locally
similar to an input example; tilemap mode uses lists of allowed adjacent tiles) and the
pcgbook.com contents (a grammars and L-systems chapter covering levels). Removed the cellular
automata and BSP rows, the Spelunky reference and the oatmeal attribution, which the pages
read do not support. The designer procedure is judgement.
Method: documentation only; no commands were run.

## Verify
- [ ] Invariants documented and checked by an automated validator.
- [ ] Seeds reproducible and logged.
- [ ] Batch statistics reviewed for 1,000+ generated levels.
- [ ] Random sample visually reviewed for pacing and variety.
