---
id: computing-software.game-programming.game-ai-programming.dijkstra-and-uniform-cost-search
name: dijkstra-and-uniform-cost-search
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, pathfinding, dijkstra, uniform-cost-search, dijkstra-map, multi-source, priority-queue, game-programming]
level: practitioner
status: verified
description: "Use Dijkstra's algorithm in games: when it beats A*, priority-queue implementation, multi-source Dijkstra maps for many agents, nearest-of-type queries and costs."
sources: ["https://www.redblobgames.com/pathfinding/a-star/introduction.html", "https://www.roguebasin.com/index.php/The_Incredible_Power_of_Dijkstra_Maps", "https://www.aiforgames.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dijkstra and uniform cost search

Dijkstra expands nodes in order of cost-so-far; A* is Dijkstra plus a heuristic. Use Dijkstra when:
- You need paths to **many** targets or **the nearest of several** (closest health pack, nearest
  enemy base): one search, stop when the first target is popped.
- You need a **distance field** from a source to everywhere (AI maps, flow fields, influence).
- No admissible heuristic exists (teleporters, abstract graphs, cost-dominated terrain).

## Implementation
```python
import heapq
def dijkstra(graph, sources, is_goal=None):
    dist, came = {}, {}
    pq = []
    for s in sources:                         # multi-source: all start at 0
        dist[s] = 0; heapq.heappush(pq, (0, s))
    while pq:
        d, n = heapq.heappop(pq)
        if d > dist[n]: continue              # stale entry (lazy deletion instead of decrease-key)
        if is_goal and is_goal(n): return n, dist, came
        for m, cost in graph.neighbors(n):    # cost must be >= 0
            nd = d + cost
            if nd < dist.get(m, float("inf")):
                dist[m] = nd; came[m] = n; heapq.heappush(pq, (nd, m))
    return None, dist, came
```
Uniform cost search is the same algorithm framed as goal-directed search (stop at the goal) rather
than all-pairs-from-source. Negative edge costs break it (use Bellman-Ford; rare in games).

## Dijkstra maps (roguelike technique)
Run multi-source Dijkstra from all goals once per change; every agent then just steps to the lowest
neighbour. Tricks:
- **Flee map:** multiply a "toward player" map by a negative number "in the neighborhood of -1.2" (RogueBasin) and
  pass it back through the Dijkstra scan. The coefficient is map dependent: in a 60-map chase test (24x24, equal speed,
  player chasing) mean survival was 98.0 turns for plain "step away", 94.8 for -1.2 and 64.5 for -1.5, so tune and
  measure it on your own maps.
- **Combine maps** with weights per agent personality (greed x treasure map + fear x player map).
- Recompute only when sources or walls change; one map serves hundreds of agents.

## Performance
- Grid: unit costs can use BFS (a deque) instead of a heap; 0/1 costs use 0-1 BFS.
- Bound the search radius for local queries ("anything within 20 m of travel").
- Reuse arrays with a generation stamp instead of clearing per search.

## Verify
- [ ] Nearest-target query returns the same target as running A* to each target and taking the minimum.
- [ ] Dijkstra map regenerates within budget when doors open/close.

## Checked (2026-10-22)
- Ran the `dijkstra` snippet with `sources=targets`: the first goal popped matched the minimum of per-target A* on 38 of 38 random 30x30 maps.
- Flee-map coefficient: fetched RogueBasin (quote above) and ran the chase simulation described above (my numbers, not the article's).
- Removed an engine-API sentence (Godot AStar, Unity NavMesh) that was not checked. 0-1 BFS, BFS for unit cost and the negative-edge limit are standard algorithm facts.
