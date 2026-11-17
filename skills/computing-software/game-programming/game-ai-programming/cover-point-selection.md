---
id: computing-software.game-programming.game-ai-programming.cover-point-selection
name: cover-point-selection
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, cover-system, tactical-ai, cover-points, eqs, tactical-scoring, line-of-sight, game-programming]
level: advanced
status: draft
description: "Build AI cover systems: generating cover points from geometry, per-threat protection tests, scoring and reservation, EQS-style queries, peeking and re-evaluation."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter26_Tactical_Position_Selection.pdf", "https://dev.epicgames.com/documentation/en-us/unreal-engine/environment-query-system-overview-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cover point selection

**Goal:** soldiers that move to cover which actually protects them from the current threat, spread
across positions, and leave when it is flanked.

## Generate cover points
- **Offline/at load:** sample along navmesh boundary edges next to tall geometry; at each sample,
  raycast outward at crouch and stand heights. Hit within ~0.5-1 m = cover; record position, cover
  normal (away from the wall), height (low/high), and edge flags (can lean/peek left/right at corners).
- **Hand-placed** markers for key spots; **dynamic** points on destructible/moving cover recomputed
  or invalidated when the object changes.
- Store in a spatial grid for fast radius queries.

## Evaluate against threats (runtime)
For a candidate point and each known threat (from perception memory, see `perception-and-memory-systems`):
- **Protected:** ray from the threat's eye to the point at crouch/stand chest height is blocked, and
  the cover normal faces the threat (`dot(normal, dirToThreat) > 0.5`).
- **Can shoot from it:** clear ray from the peek position (step-out or stand-up) to the threat.
Cache ray results per (point, threat) for a few hundred ms; time-slice queries across frames.

## Score (utility)
```
score = w1*protection + w2*canAttack + w3*(1 − pathDistance/maxDist)
      + w4*distanceToPreferredRange + w5*flankAngle − w6*nearAllies − w7*exposedPathPenalty
```
Filter first (reachable, not reserved, inside the combat zone), then score the survivors. Unreal EQS
expresses this as a generator (grid/points) plus tests (Trace, Distance, Dot, PathExists) with
filter/score modes.

## Reservation and coordination
Reserve the chosen point (release on death/leave) so two agents never pick the same one; penalise
points near allies so the squad spreads (see `squad-coordination-ai`).

## Using cover
Move with a run-to-cover animation, slide into the pose aligned to the cover normal, then cycle
peek-shoot / hide on timers and suppression. Re-evaluate when: a threat flanks (point no longer
protected), cover is destroyed, a grenade lands nearby, or periodically (2-5 s), with hysteresis so
agents do not hop constantly.

## Debug
Draw points coloured by score, reserved state and protection per threat; show the chosen point and
the top 3 alternatives with scores.

## Verify
- [ ] Moving the player around a cover object makes the AI switch sides or relocate once flanked.
- [ ] Two AIs never occupy the same point.
- [ ] Query time stays within budget with 20 agents (time-sliced).
