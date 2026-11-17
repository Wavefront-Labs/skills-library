---
id: computing-software.game-programming.game-ai-programming.pursuit-and-evasion
name: pursuit-and-evasion
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, steering-behaviours, pursuit-evasion, pursue, evade, interception, prediction, offset-pursuit, game-programming]
level: practitioner
status: verified
description: "Chase and escape moving targets with pursue/evade steering: predicting future position, look-ahead time, exact interception for projectiles, and offset pursuit."
sources: ["https://www.red3d.com/cwr/steer/gdc99/", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pursuit and evasion

**Goal:** agents that intercept moving targets instead of trailing behind them, and flee intelligently
(Reynolds 1999; Millington, AI for Games).

## Pursue
Seek the target's **predicted** position:
```
toTarget = target.position - position
dist = |toTarget|
speed = |velocity|
lookAhead = (speed <= dist / maxPrediction) ? maxPrediction : dist / speed   # Millington's form
# or Reynolds: lookAhead = dist / (maxSpeed + |target.velocity|)
predicted = target.position + target.velocity * lookAhead
return seek(predicted)
```
- If the target is ahead and facing us (head-on), just seek the current position.
- Cap the prediction time so far-away targets do not produce wild predictions.

## Evade
Flee from the predicted position of the pursuer with the same look-ahead logic; apply only within a
threat radius, and combine with obstacle avoidance so evaders do not run into walls.

## Exact interception (projectiles, turrets)
For a projectile of speed `s` from `P` and target at `T` moving with constant `V`, solve for time `t`:
```
D = T - P
a = dot(V,V) - s*s;  b = 2*dot(D,V);  c = dot(D,D)
disc = b*b - 4*a*c
t = smallest positive root of a t^2 + b t + c = 0 (if a ~ 0: t = -c / b)
aimPoint = T + V * t        (no solution: target too fast -> aim at current position or skip)
```
Use this for lead targeting; add gravity compensation for ballistic shots separately.

## Offset pursuit and formations
Pursue a point defined in the leader's local space (e.g. 2 m behind and 1 m to the left), then arrive
there: escort and formation movement. Combine with separation to avoid followers colliding.

## Game design notes
Perfect pursuit can feel unfair; add reaction delays, limit turn rates, or reduce prediction accuracy by
difficulty. Evaders in open spaces need wander/zig-zag to look alive.

## Verify
- [ ] Pursuer intercepts a target moving in a straight line faster than plain seek (measured time-to-catch).
- [ ] Interception solver hits constant-velocity targets in a turret test; handles no-solution cases.
- [ ] Evaders do not get stuck on walls (avoidance priority higher than evade).

## Checked (2026-10-22)
- Ran the interception quadratic: P=(0,0), T=(30,10), V=(-2,3), s=10 gives t=3.0630 and the projectile's travel time to the aim point equals t exactly; target faster and moving away returns no solution; the `a ~ 0` branch (`t = -c/b`) returned 1.0 for a head-on case with t=1.
- Chase test (agent max speed 5, target speed 3 moving across): time to catch 11.98 s with plain seek, 10.37 s with Millington's look-ahead, 10.28 s with Reynolds' `dist / (maxSpeed + |target.velocity|)`.
- Reynolds page confirms pursuit and evasion steer toward or away from a predicted future position with an estimated interval T.
