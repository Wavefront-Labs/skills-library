---
id: computing-software.game-programming.game-ai-programming.flow-field-pathfinding
name: flow-field-pathfinding
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, pathfinding, flow-field, integration-field, dijkstra-map, crowd-pathfinding, rts-movement, vector-field, game-programming]
level: advanced
status: verified
description: "Move hundreds of units to a shared goal with flow fields: cost, integration and direction fields, sampling with steering, sectoring big maps, and when per-unit A* wins."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter23_Crowd_Pathfinding_and_Steering_Using_Flow_Field_Tiles.pdf", "https://www.redblobgames.com/pathfinding/tower-defense/", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow field pathfinding

**Goal:** one computation gives every cell a direction toward the goal, so any number of units can
path there at constant cost per unit (Elijah Emerson, Game AI Pro ch. 23 "Crowd Pathfinding and
Steering Using Flow Field Tiles"; Red Blob Games tower-defense article).

## Three fields
1. **Cost field**: per cell traversal cost (an 8-bit value: 1-254 = path cost, 255 = wall/impassable).
2. **Integration field**: Dijkstra / breadth-first flood fill from the goal(s) outward, accumulating
   cost: `dist[goal] = 0`; relax neighbours with `dist[n] = dist[c] + cost[n]`.
3. **Flow (direction) field**: each cell points to its neighbour with the lowest integrated distance
   (8 directions, or a gradient vector for smoother motion).
```
queue = [goal]; dist[*] = INF; dist[goal] = 0
while queue:
    c = pop_min(queue)                # BFS deque if all costs equal
    for n in neighbours(c):
        nd = dist[c] + cost[n]
        if nd < dist[n]: dist[n] = nd; push(queue, n)
for each cell: dir[cell] = argmin_n dist[n] - cell   (skip diagonal moves cutting blocked corners)
```

## Moving units
Each unit samples the direction at its position (bilinear between cells for smoothness) as its desired
velocity, then applies local steering (separation, obstacle avoidance) so units do not stack. Units near
the goal switch to arrival/formation behaviour.

## Scaling to big maps
- Divide the map into sectors (Supreme Commander 2: 10x10 cells of 1 m); run a high-level search over sector portals to find
  which sectors the path crosses, then build flow fields only for those sectors (Emerson's flow field tiles).
- Cache fields per goal; many units with the same destination share one.
- Recompute incrementally when costs change locally (buildings placed).

## When to use
Great: RTS group moves, tower defense, zombie hordes chasing a player (goal = player, refresh at low
rate), many agents with few destinations. Poor: many units with distinct goals (fields per goal cost a
full-map flood each) where per-unit A*/navmesh is cheaper.

## Verify
- [ ] Every reachable cell has a direction that strictly decreases integrated distance (validation pass).
- [ ] 1,000 units to one goal: frame cost dominated by steering, not pathfinding.
- [ ] Changing terrain cost updates affected sectors and units re-route without global recompute.

## Checked (2026-10-22)
- Read Game AI Pro ch. 23 (Emerson): author, three fields, cost range 0-255 with 255 = walls, 10x10 sectors and portal windows (PDF text).
- Built a Dijkstra integration field on a random 40x40 grid with costs 1/5 and 20% walls: every one of 1,242 reachable cells has an 8-neighbour with strictly lower integrated distance, and BFS equals Dijkstra on uniform costs (the 'BFS deque' remark).
