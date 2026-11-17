---
id: computing-software.game-programming.game-ai-programming.ai-lod-and-update-throttling
name: ai-lod-and-update-throttling
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, perception, ai-lod, update-throttling, time-slicing, significance, ai-budget, game-programming]
level: advanced
status: draft
description: "Scale AI cost with relevance: LOD tiers by distance/visibility, update frequency throttling, time-sliced scheduling under a per-frame budget, and simplified off-screen simulation."
sources: ["https://www.gameaipro.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/significance-manager-in-unreal-engine", "https://www.aiforgames.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI level of detail and update throttling

**Goal:** hundreds of agents within a fixed AI budget (e.g. 2 ms/frame), with nearby/visible agents
getting full fidelity.

## LOD tiers
| Tier | Who | Decision rate | Perception | Movement/animation |
|---|---|---|---|---|
| 0 | near, visible, in combat | every frame or 30 Hz | full raycasts | full navmesh + avoidance, full anim |
| 1 | mid range or not visible | 5-10 Hz | reduced rays, cached | path following, simplified avoidance |
| 2 | far | 1-2 Hz | event-driven only | move along path without collision, anim off or at low rate |
| 3 | off-screen far / unloaded area | on demand | none | statistical/abstract simulation (schedule, teleport along route) |

Compute a **significance** score per agent (distance, on-screen, in combat, is targeting player) and
map it to a tier with hysteresis so agents don't flip-flop at boundaries. Unreal's Significance
Manager is a ready-made registry for this; tie it to `SetComponentTickInterval` and URO (update rate
optimisation) for skeletal meshes.

## Time-sliced scheduler
```cpp
// round-robin under a budget; agents carry their own "next think time"
void AIScheduler::update(double now, double budgetMs) {
    Timer t;
    while (!queue.empty() && t.ms() < budgetMs) {
        Agent* a = queue.front();
        if (a->nextThink > now) break;           // queue sorted by nextThink (heap)
        queue.pop(); a->think(now);
        a->nextThink = now + a->tierInterval();  // e.g. 0.033, 0.1, 0.5, 2.0 s
        queue.push(a);
    }
}
```
Stagger initial think times (random offset) so agents spawned together don't all think on one frame.
Expensive queries (pathfinding, EQS, LOS) go through their own budgeted request queues.

## Rules
- Think and act separately: low-tier agents still **move** smoothly every frame using the last decision.
- Promote immediately on events (took damage, heard gunshot, player looked at them).
- Hide low LOD: never let a visible agent drop below tier 1; turn-and-react delays read as
  "noticing" if short.
- Abstract simulation must hand back plausible state when promoted (position on its route, not where
  it was frozen).

## Measure
Track per-tier counts and AI ms per frame in a debug HUD; set budgets per platform. Spikes usually
come from synchronized events (alarm wakes everyone): spread reactions over frames.

## Verify
- [ ] 300-agent stress test stays within the AI budget at target frame rate.
- [ ] Agents promoted by a gunshot react within ~0.2 s; distant agents arrive at destinations on schedule.
