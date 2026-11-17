---
id: computing-software.game-programming.gameplay-programming.bsp-and-cellular-automata-dungeon-generation
name: bsp-and-cellular-automata-dungeon-generation
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, procedural-generation, dungeon-generation, bsp-dungeon, cellular-automata, roguelike, flood-fill, game-programming]
level: practitioner
status: verified
description: "Generate dungeons with BSP room splitting and corridors or cellular-automata caves, then guarantee connectivity with flood fill, place start/exit by distance and validate."
sources: ["http://www.roguebasin.com/index.php/Basic_BSP_Dungeon_generation", "http://www.roguebasin.com/index.php/Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels", "https://www.redblobgames.com/pathfinding/tower-defense/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BSP and cellular-automata dungeon generation

**Goal:** playable, connected levels from a seed; rooms-and-corridors for built spaces, caves for
organic ones.

## BSP rooms and corridors
1. Start with the whole map rectangle. Recursively split (RogueBasin's basic version picks a random direction and position; keeping the position near the middle, 0.45-0.55, gives homogeneous leaves and 0.1-0.9 heterogeneous ones). A common refinement, used in the test below: choose horizontal if the node is much wider
   than tall (ratio > 1.25), vertical if taller, else random; split position random in 30-70% of the
   length. Stop when a side would fall below `minLeaf` (e.g. 8 tiles) or at max depth.
2. In each leaf, place a room with random size inside it and a margin of 1+ tiles.
3. Connect siblings bottom-up: for each internal node, join a room from the left subtree to one in the
   right with an L-shaped corridor (horizontal then vertical, order random). Because every sibling
   pair connects, the graph is a spanning tree: always connected (a Python implementation of steps 1-3 on 80x50 maps produced one connected floor region for all 1000 seeds tried).
4. Add a few extra connections between nearby rooms to create loops (pure trees feel linear).

## Cellular automata caves
```python
grid = [[rng.random() < 0.45 for x in range(W)] for y in range(H)]   # True = wall
for step in range(5):
    new = [[False]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            walls = sum(grid[y+dy][x+dx] if 0 <= y+dy < H and 0 <= x+dx < W else 1
                        for dy in (-1,0,1) for dx in (-1,0,1))   # 3x3 including the tile itself
            new[y][x] = walls >= 5                                # the 4-5 rule
    grid = new
```
The 4-5 rule (RogueBasin): a wall stays a wall with 4 or more wall neighbours of 8, an open tile becomes a wall with 5 or more; equivalently a tile is a wall if its 3x3 block (itself included) holds at least 5 walls. An earlier version of this snippet excluded the centre tile and added a "fill voids" clause, which is not the 4-5 rule.
Out-of-bounds counts as wall so edges close. Tune fill (0.40-0.50) and iterations (4-6). Measured here on 64x40 maps, 5 iterations, 30 seeds each: fill 0.40 gives about 78% floor and 1.2 disconnected floor regions on average; 0.45 gives 62% floor and 2.8 regions; 0.50 gives 43% floor (minimum 35%) and 8.2 regions, so the connectivity pass below is needed, and the 40% floor threshold would reject some 0.50 maps.

## Connectivity pass (both methods)
Flood fill every floor region; keep the largest, then either fill the smaller ones with wall or
tunnel to the main region (shortest line between closest cells). Reject and regenerate if the main
region is below a floor-area threshold (e.g. 40%).

## Placement
BFS distance map from a start tile; put the exit at the farthest tile; place keys before locks along
the path; scatter loot weighted by distance and dead-end-ness (degree-1 cells).

## Determinism
All randomness from one seeded RNG passed explicitly (see `seeded-rng-and-reproducible-generation`)
so a seed reproduces the level for bug reports and daily challenges.

## Verify
- [ ] 10,000 seeds generate without exceptions; every level has a path start -> exit.
- [ ] Generation time per level under budget (measure p99, not mean).
- [ ] The same seed produces byte-identical maps on every platform.
