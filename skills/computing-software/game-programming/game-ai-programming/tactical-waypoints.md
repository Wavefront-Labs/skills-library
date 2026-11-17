---
id: computing-software.game-programming.game-ai-programming.tactical-waypoints
name: tactical-waypoints
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, tactical-waypoints, tactical-ai, cover, game-programming]
level: practitioner
status: draft
description: "Annotate and use tactical waypoints: precomputed cover, visibility and sniping properties, runtime context scoring, and automatic generation from geometry."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter26_Tactical_Position_Selection.pdf", "http://aigamedev.com/open/article/tactical-position-selection/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tactical waypoints

**Goal:** AI that chooses good positions (cover, flanks, ambush spots) using a set of annotated
points (Millington, *AI for Games* ch. 6 tactical and strategic AI).

## Annotations (precomputed)
Per waypoint store static properties:
- Cover directions (8-16 directional slots: is there full/half cover facing that way?).
- Visibility: which other waypoints are visible (PVS bitset) for fast queries.
- Exposure: how many points can see this one; elevation; darkness (stealth).
- Type tags: sniping spot, ambush, door choke, retreat.

## Generation
- Hand-placed by designers in early games; now usually generated: sample navmesh edges near walls
  and obstacles, test cover by raycasts at crouch and standing heights in several directions, keep
  points with cover.
- Recompute affected points when destructible cover breaks.

## Runtime selection
Score candidate points within a radius using context (Tactical Position Selection, Game AI Pro):
```text
score = w1 * coverFromThreat(p, threat) + w2 * (distance in preferred range) - w3 * pathCost
      - w4 * claimedByOther + w5 * lineOfSightToTarget(p)
```
Filter first (must have cover from current threat, reachable), then score; pick best or weighted
random among top. Unreal EQS and CryEngine TPS are built on this generate-filter-score pattern.

## Dynamic properties
Some properties depend on the current enemy position: compute only for candidates, with cached
raycasts.

## Verify
- Debug draw points coloured by score for a selected agent; playtest that agents take sensible
  cover relative to the player.
