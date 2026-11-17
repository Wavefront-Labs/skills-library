---
id: creative-arts.game-design.level-design.player-metrics-and-grid
name: player-metrics-and-grid
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, player-metrics, level-metrics, blockout, greybox, grid, jump-distance, corridor-width, gym-level, metrics-map]
level: practitioner
status: draft
description: "Establish player metrics (jump distance/height, run speed, crouch and cover heights, corridor widths) in a gym level and build blockouts on a grid that respects them."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Player metrics and grid

**Goal:** a fixed table of player capabilities and spatial standards that every level is
built against, so gaps are jumpable (or deliberately not), doors fit, cover covers, and
levels stay consistent across designers.

## 1. Measure the character (in a gym level)
Build a "gym" / metrics map: a test level with labelled blocks at incremental sizes.
Record:
| Metric | Example values to measure |
|---|---|
| Walk/run/sprint speed | units per second |
| Max jump height / distance (standing, running) | units |
| Ledge grab / mantle heights | units |
| Crouch height, cover heights (low / high) | units |
| Character capsule width/height | units |
| Fall damage thresholds | units |
| Interaction reach | units |
Engines differ (Unreal uses centimetres by default; Unity units are conventionally
metres), so write units explicitly.

## 2. Derive spatial standards
- Doors: width = capsule width + generous clearance (camera needs room in third person).
- Corridors: minimum width for one/two characters and for the camera.
- Steps and slopes: max step height and walkable slope angle from the character
  controller settings.
- Jumps: "comfortable" gaps well below max distance, "hard" near max, "impossible" well
  above (so players don't try).
- Cover: low cover below crouch eye-line, high cover above standing head.

## 3. Grid
- Choose a base grid matching the metrics (e.g. a unit that divides door width, wall
  thickness and jump distances evenly).
- Snap blockout geometry to the grid; it keeps modular art compatible
  (see `creative-arts.game-design.level-design.modular-kit-planning`).

## 4. Lock it
Metrics must be frozen before mass level production; changing jump height later breaks
every level. Treat changes as a formal decision with a re-test of all levels.

## Gotchas
- Third-person cameras need more space than the character; corridors sized only for
  the capsule cause camera clipping.
- Players read distances visually; a jumpable gap that *looks* too far won't be tried.
- Abilities that change metrics (double jump, sprint) need separate tables.

## Verify
- [ ] Gym level with labelled metric tests exists.
- [ ] Metrics table with units published to the team.
- [ ] Blockouts snap to a grid derived from the metrics.
- [ ] Metric changes after lock trigger a level re-test.
