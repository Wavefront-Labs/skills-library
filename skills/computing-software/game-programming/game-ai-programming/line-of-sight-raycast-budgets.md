---
id: computing-software.game-programming.game-ai-programming.line-of-sight-raycast-budgets
name: line-of-sight-raycast-budgets
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, los-budget, line-of-sight, perception, game-programming]
level: practitioner
status: draft
description: "Budget AI line-of-sight checks: async batched raycasts, per-frame quotas, prioritising by distance and threat, caching results and multi-point visibility tests."
sources: ["https://docs.unity3d.com/ScriptReference/RaycastCommand.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line-of-sight raycast budgets

**Goal:** 100 agents checking visibility to several targets without blowing the physics query budget.

## Cheap rejections first
1. Distance check against sight radius.
2. Field-of-view cone (dot product).
3. Then raycast.
Most pairs never reach step 3.

## Quotas and scheduling
- Global per-frame raycast budget for perception (e.g. 50-200 rays); queue requests and process
  round-robin. Unreal's AI Perception sight config has `MaxTracesPerTick` style limits in
  `AISightTargetEvaluator` settings.
- Priority: targets currently visible (to detect loss quickly), agents near the player, agents in
  combat; distant idle agents check every 0.5-1 s.
- Results carry a timestamp; memory systems treat them as valid for a short time.

## Async and batched
Issue raycasts as batched or async queries (Unreal async line traces, Unity `RaycastCommand` jobs,
PhysX batch queries) and consume results next frame. One frame of latency is invisible for perception.

## Multi-point tests
A single ray to the target's centre misses partially visible targets (head over cover). Test a few
points (head, chest, a random point) over successive frames rather than all at once; accumulate
visibility fraction for stealth meters.

## Caching
Share results: if agent A sees the player from roughly the same position as B, nearby squad members
can reuse it within a short window. Use any-hit queries with a visibility collision channel that
excludes foliage the designers want see-through.

## Verify
- Perception debug draw (rays green/red) and a counter of rays per frame vs budget; test detection
  latency stays below design targets (e.g. 0.3 s near, 1 s far).
