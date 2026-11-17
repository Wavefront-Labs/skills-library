---
id: computing-software.game-programming.game-ai-programming.seek-flee-and-arrive-steering
name: seek-flee-and-arrive-steering
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-behaviours, arrive-behaviour, seek, flee, wander, reynolds, kinematic-movement, max-acceleration, game-programming, path-following-steering]
level: practitioner
status: verified
description: "Implement Reynolds' basic steering behaviours: seek, flee, arrive with slowing radius, wander, path following, and blending them with max force/speed limits."
sources: ["https://www.red3d.com/cwr/steer/gdc99/", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Seek, flee and arrive steering

**Goal:** natural-looking agent movement from simple force rules (Craig Reynolds, "Steering
Behaviors For Autonomous Characters", 1999 Game Developers Conference; Millington, AI for Games).

## Agent model
```
position, velocity, maxSpeed, maxForce (max acceleration), mass
each tick:
    steering = truncate(sum of weighted behaviours, maxForce)
    velocity = truncate(velocity + steering / mass * dt, maxSpeed)
    position += velocity * dt
    face velocity direction (smoothly)
```

## Seek and flee
```
seek(target):  desired = normalize(target - position) * maxSpeed;  return desired - velocity
flee(threat):  desired = normalize(position - threat) * maxSpeed;  return desired - velocity
```
Steering = desired velocity minus current velocity, which produces smooth curves instead of instant
turns. Flee usually only within a panic distance.

## Arrive (seek that stops)
Seek overshoots and orbits the target. Arrive slows inside a radius:
```
toTarget = target - position; d = |toTarget|
if d < arriveTolerance: return -velocity                 # brake to stop
speed = maxSpeed * min(d / slowingRadius, 1)
desired = toTarget / d * speed
return desired - velocity
```
Tune `slowingRadius` and measure overshoot. A radius equal to the braking distance `maxSpeed^2 / (2 * maxForce)`
is NOT enough with this linear speed ramp: starting at full speed it overshot by 1.5 to 6.3 units (maxSpeed 5/10/20,
maxForce 10/10/40). Overshoot reached zero at about 16x the braking distance (8x for maxSpeed 10). The
cause is that the steering force is capped while the desired speed falls only linearly with distance.

## Wander
Project a circle ahead of the agent, keep a target point on it that jitters randomly each tick, seek
that point: smooth random roaming without twitching.

## Path following
Seek the point a short look-ahead distance along the path from the agent's projected position (or
seek the next waypoint and switch when within a radius; arrive at the last one).

## Combining behaviours
- **Weighted sum**: `steer = w1*seek + w2*separation + w3*avoid`, truncated. Simple; behaviours can
  cancel each other.
- **Prioritised**: evaluate in priority order (obstacle avoidance first) and accumulate until the force
  budget is used: safety behaviours win.
Most engines' crowd systems (Detour crowd, RVO) replace avoidance terms; seek/arrive still drive the
desired velocity.

## Verify
- [ ] Arrive stops within tolerance without oscillating, for several max speeds.
- [ ] Behaviour identical at different frame rates (integration uses dt).
- [ ] Debug draw of desired velocity and steering vectors per agent.

## Checked (2026-10-22)
- Integrated the agent model, seek and arrive exactly as written (numpy, dt 1/60, target 100 units away, start at max speed): final distance under 0.05 and speed 0 in every case, identical at 30 and 144 fps, overshoot numbers above.
- Reynolds page (red3d.com/cwr/steer/gdc99): 1999 Game Developers Conference, arrival has a stopping radius with desired speed ramped inside it. Flee, wander and path following are standard Reynolds behaviours; the skill's pseudocode for them is not separately run here.
