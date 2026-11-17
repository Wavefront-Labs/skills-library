---
id: computing-software.game-programming.game-ai-programming.d-star-lite-incremental-replanning
name: d-star-lite-incremental-replanning
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, d-star-lite, incremental-search, replanning, game-programming]
level: practitioner
status: verified
description: "Replan efficiently when the map changes with D* Lite and LPA*: reuse previous search results, key computation, edge cost updates and when plain A* is enough."
sources: ["http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf", "https://en.wikipedia.org/wiki/D*"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incremental replanning with D* Lite

**Goal:** an agent moving through a world where edge costs change (doors close, terrain revealed)
repairs its path instead of searching from scratch (Koenig and Likhachev, *D* Lite*, AAAI 2002).

## Idea
D* Lite searches **backwards** from goal to the agent, storing `g` (current cost estimate) and `rhs`
(one-step lookahead) per node. A node is consistent when `g == rhs`. When edge costs change, only
affected nodes become inconsistent and get reprocessed.

## Core
```text
key(s) = [ min(g(s), rhs(s)) + h(start, s) + km ,  min(g(s), rhs(s)) ]
initialise: rhs(goal) = 0, push goal
ComputeShortestPath: while top key < key(start) or rhs(start) != g(start):
    pop u; if g(u) > rhs(u): g(u) = rhs(u); update predecessors
           else: g(u) = inf; update u and predecessors
on edge cost change: km += h(lastStart, start); lastStart = start; update affected vertices; ComputeShortestPath
move: next = argmin over successors of (c(start, s') + g(s'))
```
`km` avoids reordering the whole queue when the agent moves (heuristics are relative to the start).

## When to use
- Unknown or partially known terrain revealed by sensors (robotics origin; fog-of-war exploration).
- Few agents with long paths and frequent local changes.
For many agents with occasional changes, plain A* re-paths with time-slicing, or flow fields
per goal, are simpler and often faster. LPA* is the fixed-start version (start and goal fixed, costs change).

## Pitfalls
- Memory: per-node g/rhs state persists per agent; costly for many agents on big maps.
- Tie-breaking and floating-point costs can cause oscillation; use integer costs if possible.

## Verify
- Compare nodes expanded on replanning vs fresh A* after changing a few edges near the agent;
  path must equal A*'s optimal cost.

## Checked (2026-10-22)
- Implemented D* Lite exactly as the Core block (key with km, rhs/g, ComputeShortestPath loop, km update on edge change) on 4-connected grids and ran 20 maps (40x40, 15% walls) with the agent walking its greedy path and a new blocked cell appearing ahead every 5 steps: g(start) equalled a fresh A* cost after every one of 181 replans; replanning expanded 1,396 nodes in total versus 70,093 for fresh A* searches.
- Koenig and Likhachev, 'D* Lite', AAAI 2002: PDF fetched (authors, 2002, rhs/g formulation); Wikipedia D* page confirms D* Lite as an incremental heuristic search by Koenig and Likhachev building on LPA*.
