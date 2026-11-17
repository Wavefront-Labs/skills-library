---
id: computing-software.game-programming.game-ai-programming.time-sliced-pathfinding
name: time-sliced-pathfinding
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, time-sliced-pathfinding, pathfinding, ai-budget, game-programming]
level: practitioner
status: draft
description: "Spread pathfinding over frames: incremental A* with node budgets, request queues and priorities, partial paths while searching and stale request handling."
sources: ["https://recastnav.com/classdtNavMeshQuery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time-sliced pathfinding

**Goal:** hundreds of agents request paths without any frame spending more than its pathfinding budget.

## Incremental search
Make A* resumable: keep open list, closed set and parents in a per-request search object.
```cpp
enum class Status { InProgress, Found, Failed };
Status PathRequest::step(int maxNodes) {
    for (int i = 0; i < maxNodes && !open.empty(); ++i) {
        Node n = open.pop();
        if (n == goal) return Status::Found;
        expand(n);
    }
    return open.empty() ? Status::Failed : Status::InProgress;
}
```
Detour has this built in: `dtNavMeshQuery::initSlicedFindPath`, `updateSlicedFindPath(maxIter, &done)`,
`finalizeSlicedFindPath` (or `finalizeSlicedFindPathPartial` to get the best partial result).

## Scheduler
- Global budget per frame (e.g. 2000 node expansions or 0.5 ms), shared round-robin or by priority
  among active requests.
- Priority: player-visible agents, agents in combat, and nearer agents first.
- Limit concurrent searches (memory for search state); queue the rest.
- De-duplicate: if an agent requests again before completion, replace the old request.

## Keeping agents moving
- While searching, move toward the goal directly or along a partial path (best node so far).
- Use a cheap hierarchical path (HPA*) immediately, refine the next segment in slices.

## Stale requests
Validate results: if the agent moved far or the target moved, re-path from the current position, or
patch the path start. Nav changes (doors) invalidate in-flight searches touching modified tiles.

## Verify
- Stress test 500 agents re-pathing: frame time spike-free; measure average request latency in frames.
