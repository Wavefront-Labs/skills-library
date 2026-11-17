---
id: creative-arts.game-design.level-design.open-world-points-of-interest
name: open-world-points-of-interest
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, open-world-design, points-of-interest, poi-density, exploration, landmarks, map-icons, curiosity, world-design]
level: advanced
status: draft
description: "Plan open-world points of interest: density by travel time, variety of POI types, visibility and landmark draw, avoiding checklist map icons, and measuring exploration."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open-world points of interest

**Goal:** an open world where something interesting is always in view or within a short
walk, and players explore because they are curious, not because icons tell them to.

## Density by time, not distance
1. Measure **traversal speed** (walk, sprint, mount, vehicle).
2. Set a target **time between discoveries** (e.g. something minor every ~30-60 s of
   travel, something significant every few minutes). These are design choices; tune
   by playtest.
3. Convert to distances per traversal mode and lay a density grid over the map.

## POI variety (mix types)
| Type | Examples |
|---|---|
| Combat | camps, roaming elites |
| Traversal challenge | climbs, races, platforming towers |
| Puzzle | shrines, environmental puzzles |
| Narrative | ruins with environmental storytelling, NPC encounters |
| Reward | chests, collectibles, vistas |
| Service | towns, vendors, fast travel |
| Dynamic | events, weather, wandering NPCs |
Avoid many POIs of the same type in a row.

## Visibility and pull
- **Landmarks** visible from far away pull exploration (towers, unusual silhouettes,
  smoke columns).
- The **"what's that?" test:** from many points, the player should see at least one
  intriguing thing they have not visited.
- Designs that encourage looking at the world (marking by sight, minimal HUD) were
  highlighted in discussions of The Legend of Zelda: Breath of the Wild's world design.

## Avoid checklist design
Filling the map with icons that reveal everything ("clear 200 question marks") turns
exploration into chores. Prefer: discover-by-sight, partial information, varied
rewards, and fewer, richer POIs.

## Measure
Heatmaps of player paths, POI discovery rates, time between discoveries per region.
Regions players skip or rush through need more draw.

## Gotchas
- Uniform density is monotonous; use rhythm (quiet stretches before big reveals).
- Rewards that are mostly crafting materials devalue discovery.

## Verify
- [ ] Target time-between-discoveries defined per traversal mode.
- [ ] POI type mix plotted per region.
- [ ] Landmark visibility check from sampled positions.
- [ ] Path heatmaps reviewed; low-traffic regions addressed.
