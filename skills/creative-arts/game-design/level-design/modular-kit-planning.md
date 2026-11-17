---
id: creative-arts.game-design.level-design.modular-kit-planning
name: modular-kit-planning
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, modular-kit, modular-environment, snapping, grid, pivot-points, blockout, environment-art, reuse]
level: practitioner
status: draft
description: "Plan a modular environment kit with art: grid size, piece list (walls, corners, doors, floors, trims), pivots and snapping, so levels can be built and reskinned fast."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modular kit planning

**Goal:** a set of reusable, grid-snapping pieces agreed between level design and
environment art, so blockouts convert to final art quickly and levels stay on metrics.

## Procedure
1. **Start from player metrics** (see `creative-arts.game-design.level-design.player-metrics-and-grid`).
   Pick a kit grid that fits door widths, wall heights and floor heights.
2. **Piece list (typical interior kit):**
   | Category | Pieces |
   |---|---|
   | Walls | straight (1, 2, 4 grid units), inner corner, outer corner, end cap |
   | Openings | door frame, window, archway |
   | Floors/ceilings | tiles at grid sizes, stairs, ramps at the allowed slope |
   | Transitions | trims, skirting, wall-to-floor pieces to hide seams |
   | Vertical | pillars, ledges at mantle heights, railings |
   | Variety | damaged variants, decals, props to break repetition |
3. **Pivot convention:** all pieces pivot at a consistent corner (or bottom centre) on
   grid; document it. Mixed pivots make snapping painful.
4. **Blockout parity:** create grey versions of every kit piece at exact dimensions for
   level designers to block out with. Swapping grey for art then requires no layout
   change.
5. **Test kit:** build a sample room with every piece; check seams, lighting and
   collision.
6. **Collision:** simple collision per piece; check doorways don't snag.

## Gotchas
- Repetition is visible fast; plan variants, decals and hero props from the start.
- Kits that don't support the angles levels need (45-degree walls, curves) force
  custom geometry later.
- Changing the grid after the kit exists rebuilds everything.
- Overly fine pieces (tiny wall chunks) inflate draw calls and placement time;
  balance granularity.

## Verify
- [ ] Kit grid derived from metrics, documented.
- [ ] Piece list and pivot convention agreed by level design and art.
- [ ] Grey blockout pieces match art pieces dimensionally.
- [ ] Sample room built with no seams or collision snags.
