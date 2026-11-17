---
id: computing-software.game-programming.game-ai-programming.steering-blending-and-priority-arbitration
name: steering-blending-and-priority-arbitration
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-blending, priority-arbitration, steering-behaviours, game-programming]
level: practitioner
status: verified
description: "Combine steering behaviours: weighted blending, prioritised truncation, context steering maps, and fixing oscillation and cancellation between behaviours."
sources: ["https://www.red3d.com/cwr/steer/gdc99/", "https://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter18_Context_Steering_Behavior-Driven_Steering_at_the_Macro_Scale.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Steering blending and priority arbitration

**Goal:** an agent that avoids obstacles, keeps formation and seeks its target at once, without
jittering or walking into walls because behaviours cancel out.

## Weighted blending
```text
# pseudocode
force = truncate(w_seek * seek() + w_separate * separation() + w_avoid * avoid_walls(), max_force)
```
Simple, but opposing forces cancel (target behind a wall -> seek and avoid sum to zero, agent stops).

## Prioritised arbitration (Reynolds; Millington's priority steering)
Group behaviours by priority; evaluate highest first, accumulate until the force budget is used:
```text
# pseudocode
total, remaining = Vec2(0, 0), max_force
for b in by_priority:                    # avoid walls > avoid agents > formation > seek
    f = b.weight * b.compute()
    n = length(f)
    if n > remaining: total += f * (remaining / n); break
    total += f; remaining -= n
```
Or simpler: take the first group whose result exceeds a small epsilon.

## Context steering (Andrew Fray, Game AI Pro 2)
Each behaviour writes into **interest** and **danger** maps over N directions (N slots). Mask
directions whose danger exceeds the minimum, pick the highest-interest remaining direction
(interpolate between slots). Behaviours never cancel; avoidance is explicit. Excellent for racing
and swarm games.

## Oscillation fixes
- Smooth output direction over time (low-pass filter) and hysteresis on behaviour switching.
- Use predicted positions for avoidance, not current ones.
- Clamp turn rate in locomotion, not steering.

## Verify
- Test cases: target behind wall, narrow corridors, crowd crossing; record stuck time and jitter
  (heading change per second).

## Checked (2026-10-22)
- Ran both blends with numpy vectors: seek (+1,0) plus wall avoidance (-1,0) sums to (0,0) (the stall described); with maxForce 10, avoidance 8 then seek 6 gives (-6, 0) (seek is trimmed to the remaining budget), and avoidance 12 then seek 6 gives (-10, 0) (seek gets nothing). The `cpp` blocks are now Python-style pseudocode for these tested loops (`truncate`, `length` are the obvious helpers).
- Game AI Pro 2 ch. 18 PDF: Andrew Fray, context steering with interest and danger maps; Reynolds' page describes prioritised acceleration allocation. Removed the unsourced slot count.
