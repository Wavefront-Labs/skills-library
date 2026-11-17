---
id: computing-software.game-programming.game-ai-programming.tactical-pathfinding-and-flanking
name: tactical-pathfinding-and-flanking
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, tactical-pathfinding, flanking, pathfinding, game-programming]
level: practitioner
status: draft
description: "Make AI paths tactically aware: add threat exposure and danger costs to A*, compute flanking routes, and keep paths varied without breaking admissibility."
sources: ["https://www.redblobgames.com/pathfinding/a-star/introduction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tactical pathfinding and flanking

**Goal:** agents choose routes that avoid enemy fire and approach from the side, not the shortest
line through the kill zone (Millington, *AI for Games*: tactical pathfinding).

## Cost modification
Augment edge cost with tactical terms:
```text
cost(e) = length(e) * (1 + wExposure * exposure(e.to) + wDanger * danger(e.to))
exposure(node) = fraction of known enemies with line of sight to node (precomputed visibility sets
                 or influence map lookup)
```
- Heuristic stays admissible because costs only increase (use plain distance).
- Search explores more nodes; budget accordingly or use a coarser tactical graph.

## Flanking
1. Compute target's facing / the direction allies are attacking from.
2. Penalise nodes inside the target's view cone or near the main assault line; reward nodes in an
   arc to the side.
3. Path to a flank position chosen by tactical position scoring, with exposure-weighted costs.
Coordinate through squad claims so only some agents flank while others suppress.

## Influence maps
A danger influence map (enemy positions spread with falloff, recent deaths, grenade landings) gives
cheap per-node danger values; update at a few Hz.

## Variety
Add small random noise to costs per agent or per request so groups don't follow identical lines;
keep noise bounded so paths remain sensible.

## Pitfalls
- Exposure costs from stale enemy positions; use team knowledge with confidence.
- Overly high weights produce huge detours; cap the detour ratio and fall back to shortest path.

## Verify
- Visualise path choices with and without tactical costs on test maps; measure damage taken by AI
  approaching a turret along each.
