---
id: computing-software.game-programming.game-ai-programming.pathfinding-world-representations
name: pathfinding-world-representations
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, waypoint-graph, world-representation, pathfinding, game-programming]
level: practitioner
status: verified
description: "Choose a pathfinding world representation: tile grids, waypoint graphs, navmeshes and points of visibility, with their quantisation and smoothing trade-offs."
sources: ["https://www.redblobgames.com/pathfinding/grids/graphs.html", "http://theory.stanford.edu/~amitp/GameProgramming/MapRepresentations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# World representations: grids and waypoint graphs

**Goal:** pick the graph A* searches, since it decides path quality and cost more than the search
algorithm does (see Amit Patel's Red Blob Games pathfinding notes).

## Options
| Representation | Pros | Cons | Fits |
|---|---|---|---|
| **Tile grid** (4/8-connected) | Trivial to build and update, matches tile games | Many nodes, jaggy paths, memory for large worlds | RTS, roguelikes, 2D |
| **Waypoint graph** (hand or auto placed nodes + edges) | Few nodes, fast | Agents stick to lines, poor coverage of open areas, edges must be validated | Older shooters, corridors, rail-like AI |
| **Points of visibility** (nodes at convex corners) | Short paths in polygon worlds | Edge count grows fast | 2D polygon maps |
| **Navmesh** (convex polygons) | Covers walkable area, natural paths, few nodes | Build complexity (use Recast), dynamic changes cost | 3D action games (default today) |

## Grids
- Diagonal moves cost sqrt(2); forbid corner cutting through blocked diagonals.
- Heuristic: octile distance for 8-connected, Manhattan for 4.
- Speed up with JPS (uniform cost) or hierarchical abstraction (HPA*).

## Waypoint graphs
- Generate edges by raycasting/capsule sweeping between nodes within range; store traversal type
  (walk, jump, ladder) and cost.
- Agents first path to the nearest reachable node; validate the start/end connection with a sweep.
- Use as a supplementary layer even with navmeshes: tactical points, jump links, patrol routes.

## Quantisation and smoothing
Every representation needs mapping from world position to node (quantisation) and back
(localisation). Smooth grid/waypoint paths with string pulling (remove nodes when line of sight to
the next-next node is clear), or the funnel algorithm on navmeshes.

## Verify
- Path quality: compare path length vs straight-line optimum on test maps; profile nodes expanded.

## Checked (2026-10-22)
- Grid rules re-run in this batch: octile distance is exact for 8-connected unit/sqrt(2) costs and Manhattan overestimates there (A* tests in `astar-pathfinding-and-behaviour-trees`); JPS and HPA* behaviour per their own skills.
- String pulling run on 38 A* grid paths (40x40, 15% walls): total grid-path length 2333.7, 2176.1 after pulling nodes whose line of sight is clear, straight-line lower bound 2095.9, so smoothing removed 6.8% here.
- The pros/cons table is qualitative design guidance; Millington attribution removed (book not available); the Red Blob Games site returns HTTP 200.
