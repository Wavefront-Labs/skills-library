---
id: computing-software.game-programming.game-ai-programming.astar-pathfinding-and-behaviour-trees
name: astar-pathfinding-and-behaviour-trees
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, game-ai, a-star, astar, pathfinding, heuristic, manhattan, octile, navmesh, recast, detour, path-smoothing, string-pulling, funnel-algorithm, behaviour-tree, behavior-tree, blackboard, selector, sequence, decorator, utility-ai, steering-behaviours, fsm, perception, unreal-behavior-tree, unity-navmesh, simple-stupid-funnel]
level: practitioner
status: verified
description: "Give agents believable movement and decisions: A* with the right heuristic, navmeshes and path smoothing, behaviour trees with a blackboard, and when to use utility AI instead."
sources: ["https://www.redblobgames.com/pathfinding/a-star/introduction.html", "https://github.com/recastnavigation/recastnavigation", "Millington, AI for Games (3rd ed.)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# A* pathfinding and behaviour trees

**Goal:** agents that reach destinations along sensible routes and choose actions in a
way designers can read and tune — the two pillars of most action-game AI.

## Part 1 — A*
```python
import heapq
def astar(start, goal, neighbours, cost, h):
    open_ = [(h(start, goal), 0, start)]
    came_from = {start: None}
    g = {start: 0}
    while open_:
        _, gc, cur = heapq.heappop(open_)
        if cur == goal: break
        if gc > g[cur]: continue                 # stale heap entry (lazy deletion)
        for n in neighbours(cur):
            ng = g[cur] + cost(cur, n)
            if ng < g.get(n, float("inf")):
                g[n] = ng; came_from[n] = cur
                heapq.heappush(open_, (ng + h(n, goal), ng, n))
    # walk came_from back from goal (check goal in came_from: unreachable otherwise)
```
**Heuristic must match movement** and never overestimate (admissible) to guarantee
shortest paths:
- 4-way grid: Manhattan `dx + dy`. On an 8-way grid Manhattan overestimates (it returned longer-than-optimal paths on 12 of 21 random 40x40 maps).
- 8-way grid with diagonal cost √2: octile `(dx + dy) + (√2 − 2)·min(dx, dy)`.
- Free movement / navmesh: Euclidean distance.
Multiplying h by a weight ("weighted A*") explores far fewer nodes for
slightly longer paths — often the right game trade. Measured on 21 random 40x40 8-way maps:
weight 1.2 expanded 44% of the nodes (paths 0.4% longer in total, worst single path 1.8%), weight 1.5
expanded 22% (2.6% longer in total, worst 7.9%). Tie-breaking toward the goal
(nudge h by a tiny factor) avoids exploring huge equal-cost plateaus on open grids (empty 60x60 4-way grid, goal (59,20): 1259 expansions
with plain h, 79 with h x 1.001, same cost 79).

**Navmeshes over grids** for 3D worlds: convex polygons covering walkable space, far fewer
nodes, and agents can stand anywhere. Recast builds them from level geometry (key
parameters in `rcConfig`: `walkableRadius`, `walkableHeight`, `walkableClimb`, `walkableSlopeAngle`, cell size `cs` and `ch`); Detour does queries.
The Recast README says Recast powers AI navigation in Unity, Unreal, Godot and O3DE.
Then **smooth the path**: the polygon-corridor path is jagged; the funnel
("string-pulling") algorithm gives the shortest line through the corridor. Agent radius
must be baked into the mesh (erode by radius) or agents hug corners and clip walls.

Performance: cap search per frame (time-slice long searches over frames), cache paths
and re-plan only when the goal moves significantly or the path is blocked; use
hierarchical pathfinding (HPA*) for very large maps; flow fields when hundreds of units
share one goal (RTS).

## Part 2 — Behaviour trees
A tree ticked every frame (or every few frames); each node returns **Success, Failure
or Running**.
- **Sequence** (→): runs children in order; fails on the first failure. "Do all of these."
- **Selector / Fallback** (?): tries children in order; succeeds on the first success.
  "Do the first that works." Put higher priorities left.
- **Decorators:** Inverter, Repeat, Cooldown, **conditions/guards** ("has line of sight").
- **Leaves:** actions (`MoveTo`, `Attack`, `PlayAnim`) and condition checks.
- **Blackboard:** shared key-value memory (`TargetActor`, `LastKnownPosition`,
  `Ammo`). Perception writes to it; the tree reads it.

Example guard AI:
```
Selector
├─ Sequence [has Target && can see Target]
│   ├─ Selector
│   │   ├─ Sequence [in range]  → Attack
│   │   └─ MoveTo(Target)
├─ Sequence [has LastKnownPosition]
│   ├─ MoveTo(LastKnownPosition)
│   ├─ Wait(3 s, look around)
│   └─ Clear LastKnownPosition
└─ Patrol(waypoints)
```
**Re-evaluation:** a running `Patrol` must be interrupted when an enemy appears.
Either re-tick from the root every frame (reactive) or use event-driven aborts (Unreal's
decorator "Observer Aborts": Self, Lower Priority or Both). Missing aborts is the #1 "AI ignores
me" bug.

## When to use something else
- **FSM:** a handful of states with clear transitions (a door, a simple enemy). Fine.
- **Utility AI:** many competing options scored by curves over inputs (hunger, threat,
  distance) — good for sims and "life-like" choices; harder to make deterministic for
  designers.
- **GOAP / HTN planners:** agents that chain actions toward goals (F.E.A.R.-style);
  powerful, costlier to debug.
- **Steering behaviours** (seek, arrive, separation, obstacle avoidance) sit *under*
  any of these to turn a path into smooth movement and keep crowds from overlapping.

## Gotchas
- Believability beats optimality: add reaction delays (a few hundred ms, tuned per game), imperfect aim, and
  telegraphs; an AI that reacts instantly and perfectly feels like cheating.
- Debug visualisation (draw paths, current BT node, blackboard values over heads) is
  not optional; build it first.

## Verify
- [ ] Heuristic is admissible for the movement model (paths are shortest when weight = 1).
- [ ] Agents don't clip corners; radius baked into navigation.
- [ ] Path requests are time-sliced/cached; no frame spikes with 50 agents re-planning.
- [ ] Patrolling agent reacts within a frame or two when the player becomes visible.
- [ ] Debug overlay shows path and active BT branch.

## Checked (2026-10-22)
- Ran the A* snippet verbatim on random 8-way grids: octile is optimal (equals h=0 Dijkstra on all 21 reachable maps), Manhattan is not, weighted and tie-break figures above are measured.
- Fetched `Recast.h` (rcConfig field names) and the Recast README (engines list); Unreal Observer Aborts options from Epic's localised decorator reference.
- Behaviour-tree semantics (Success/Failure/Running, abort) re-implemented in Python for `behaviour-tree-runtime-implementation`; the guard tree here is pseudocode of those semantics.
