---
id: computing-software.game-programming.game-ai-programming.hierarchical-pathfinding-hpa-star
name: hierarchical-pathfinding-hpa-star
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, pathfinding, a-star, hierarchical-pathfinding, hpa-star, abstract-graph, clusters, entrances, path-refinement, game-programming]
level: advanced
status: draft
description: "Speed up pathfinding on large maps with HPA*: clustering the grid, building entrance graphs, abstract search, path refinement, dynamic updates and when it beats plain A*."
sources: ["https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972", "https://www.gameaipro.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchical pathfinding (HPA*)

**Goal:** long-distance paths on big grids (RTS maps, open worlds) in a fraction of the time of plain
A*, with near-optimal results (Botea, Mueller, Schaeffer 2004; Millington ch. 4.6).

## Preprocessing
1. Divide the grid into square **clusters** (e.g. 10x10 or 16x16 cells).
2. Along each border between adjacent clusters, find **entrances**: maximal runs of walkable cells on
   both sides. For each entrance create one transition (two nodes, one in each cluster) in the middle,
   or two at the ends for long entrances.
3. Inside each cluster, connect every pair of its entrance nodes with an intra-cluster edge whose cost
   is the A* path length restricted to that cluster (cache the paths if memory allows).
Result: an abstract graph with few nodes per cluster.

## Query
1. Insert start and goal temporarily into the abstract graph: connect each to the entrance nodes of its
   own cluster (local A* inside the cluster).
2. A* on the abstract graph (small) -> sequence of entrance nodes.
3. **Refine**: replace each abstract edge with its cached low-level path (or compute it lazily as the
   agent moves: path only the next segment, which also handles changes along the way).
4. Optional smoothing (string pulling) because cluster entrances add detours (paths within ~1-10% of
   optimal).

## Dynamic changes
A door closing or building placed only invalidates the clusters it touches: recompute their entrances
and intra-cluster edges. Agents with paths through the changed cluster re-plan from the abstract level.

## Multiple levels and sizes
More levels (clusters of clusters) for very large worlds. Different agent sizes need clearance
annotations (cells store clearance; entrances per size class) or separate graphs.

## Alternatives to weigh
- Navmesh + A* already reduces node count massively for 3D worlds; HPA* matters most for big grids.
- Jump Point Search (uniform-cost grids, no preprocessing) or flow fields (many agents to one goal).
- Precomputed all-pairs tables for small static maps.

## Verify
- [ ] Benchmark: average/max query time vs plain A* on large maps (expect order-of-magnitude gains on long paths).
- [ ] Path length overhead vs optimal measured (with and without smoothing).
- [ ] Changing one cluster updates only that cluster's graph and keeps queries correct.
