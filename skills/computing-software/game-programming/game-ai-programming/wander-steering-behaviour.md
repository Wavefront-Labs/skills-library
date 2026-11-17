---
id: computing-software.game-programming.game-ai-programming.wander-steering-behaviour
name: wander-steering-behaviour
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-behaviours, wander-behaviour, reynolds-steering, ambient-ai, noise, game-programming]
level: intro
status: verified
description: "Implement Reynolds wander steering: the projected wander circle with jitter, frame-rate-independent tuning, noise-based alternatives, and keeping wanderers inside an area."
sources: ["https://www.red3d.com/cwr/steer/gdc99/", "https://www.red3d.com/cwr/steer/Wander.html", "https://www.aiforgames.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wander behaviour

**Goal:** smooth, natural-looking aimless motion for ambient creatures, idle NPCs and flock members,
not random direction changes every frame (which looks like jitter).

## Reynolds wander circle
Project a circle ahead of the agent; a target point lives on the circle and is nudged by small random
displacements each step. Steering seeks that point.
```csharp
float wanderAngle;                       // persistent per agent
Vector3 Wander(float dt) {
    wanderAngle += Random.Range(-1f, 1f) * jitterRadiansPerSqrtSecond * Mathf.Sqrt(dt);   // sqrt(dt): see below
    Vector3 center = velocity.normalized * circleDistance;
    Vector3 offset = new Vector3(Mathf.Cos(wanderAngle), 0, Mathf.Sin(wanderAngle)) * circleRadius;
    Vector3 desired = (center + offset).normalized * maxSpeed;
    return Vector3.ClampMagnitude(desired - velocity, maxForce);          // steering force
}
```
Tuning knobs:
| Knob | Larger means |
|---|---|
| circleDistance | straighter, more purposeful paths |
| circleRadius | sharper possible turns |
| jitter | more frequent direction changes |

Scale the random increment by `sqrt(dt)`, not `dt`. The angle is a random walk, so its variance after a
fixed time is proportional to (increment scale)^2 x steps. Measured variance of the angle after 10 s (jitter 3,
uniform -1..1 increments, 4000 runs): unscaled 896 / 1795 / 4284 at 30 / 60 / 144 fps; scaled by `dt` 0.995 / 0.499 /
0.207; scaled by `sqrt(dt)` 29.9 / 29.9 / 29.7 (frame-rate independent). Scaling by `dt` makes high-frame-rate
agents wander far less.

## Noise-based alternative
`heading += (noise(time * freq + seed) - 0.5f) * turnRate * dt` (noise in 0..1, e.g. Perlin) gives smooth, deterministic,
seedable wander; easy to replay and network.

## Staying in bounds
- Blend with **containment**: when the predicted position leaves the area (or navmesh), add a
  seek-to-centre force weighted by how far out it is.
- On navmeshes, wander by picking random reachable points nearby (use your engine's random-reachable-point
  query) and pathing there; pure steering ignores walls.
- Combine with obstacle avoidance at higher priority (see steering blending).

## Gotchas
- `velocity.normalized` at zero velocity: use the facing direction.
- Too high jitter looks like buzzing; too low looks like orbiting. Visualise the circle and target
  with debug draw while tuning.

## Verify
- [ ] Agents wander smoothly at 30 and 144 fps with the same character.
- [ ] Over 5 minutes, no agent leaves the allowed area or gets stuck against a wall.

## Checked (2026-10-22)
- The `sqrt(dt)` correction is computed (numpy variance table above); the old text said `dt` or `sqrt(dt)`, and `dt` is the wrong one for frame-rate independence.
- C# is Unity-flavoured and not compiled here; the wander angle update was re-implemented in numpy. Removed three engine function names (Unity, Godot, Unreal) that were not checked, and the Unity-specific Perlin call.
- Reynolds page confirms the circle ahead of the vehicle with a jittering target ('wander rate').
