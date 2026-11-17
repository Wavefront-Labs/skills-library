---
id: computing-software.game-programming.game-ai-programming.influence-maps
name: influence-maps
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, tactical-ai, influence-map, threat-map, propagation, falloff, strategic-ai, rts-ai, spatial-reasoning, game-programming]
level: practitioner
status: verified
description: "Give AI spatial awareness with influence maps: grid layers, stamping and propagation with falloff, combining threat/control/opportunity layers and querying them."
sources: ["https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter30_Modular_Tactical_Influence_Maps.pdf", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Influence maps

**Goal:** let AI reason about space: where enemies are strong, which areas are contested, where the
safe flank is, where to expand (Millington, AI for Games; Dave Mark, Game AI Pro 2 ch. 30).

## Representation
A 2D grid (or navmesh polygons/waypoints) over the world, each cell holding a float per layer. Cell
size trades precision for cost (finer for shooters, larger tiles for RTS).

## Building a layer
1. **Stamp** each unit's influence: value at its position, decaying with distance up to a radius.
   Precompute stamp templates per radius/falloff (linear, quadratic, inverse) and add them.
   ```
   influence(d) = strength * max(0, 1 - d / radius)          # linear falloff
   ```
2. Or **propagate**: seed sources then iterate, each cell taking max/decayed neighbour values
   (`v = max(v, neighbour * decay)`), so influence flows around walls instead of through them.
   Momentum (blend with last frame's map) smooths noise.

## Common layers
| Layer | Built from |
|---|---|
| Proximity / control (per faction) | Unit positions, weighted by unit strength. |
| Threat | Enemy weapon ranges and damage; line-of-sight optional. |
| Visibility / exposure | Number of enemy sight lines to a cell. |
| Opportunity | Resources, objectives, cover value. |

## Combining and querying
Working maps are formulas over layers, built per decision:
```
safe_attack_spot = my_proximity * 0.5 + opportunity - enemy_threat * 2
tension = my_control + enemy_control     # high wherever either side is strong (10+0 and 5+5 both give 10)
vulnerability = tension - abs(my_control - enemy_control)   # = 2 * min(...): high only where both are high (contested front)
```
Query the working map within a search area (around the agent, within path distance) for max/min
cells. Normalise layers to 0..1 first so weights are meaningful.

## Performance
- Update layers at low frequency and/or incrementally; time-slice across frames.
- Only build working maps in the local region needed for a query (modular approach from Game AI Pro 2).
- SIMD/compute-friendly: grids are flat float arrays.

## Debugging
Overlay heatmaps in-game per layer; essential for tuning weights. Log the chosen cell and its layer
components for each decision.

## Verify
- [ ] Heatmap overlay shows threat flowing around walls (propagation) rather than through them where intended.
- [ ] AI chooses flank positions with lower threat in test scenarios.
- [ ] Update cost within your frame budget, amortised.

## Checked (2026-10-22)
- Ran a 15x15 grid with a wall that has one gap: propagation `v = max(v, neighbour*decay)` (decay 0.8) gives 0.410 on the near side of the wall, 0.0115 on the far side (flowing round through the gap) and 0 inside the wall, while a linear stamp (radius 10) gives 0.4 at distance 6 straight through the wall, which is the difference the skill describes.
- Tension and vulnerability formulas computed for (my, enemy) = (10,0), (0,10), (5,5): tension 10, 10, 10; vulnerability 0, 0, 10. The previous comment on `tension` was misleading and is corrected.
- Game AI Pro 2 ch. 30 chapter PDF fetched (author Dave Mark, modular tactical influence maps). Removed unsourced figures (cell sizes in metres, 2-10 Hz, 0.5 ms).
