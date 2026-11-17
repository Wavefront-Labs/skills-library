---
id: computing-software.game-programming.game-physics.tire-friction-models
name: tire-friction-models
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, vehicle-physics, tire-model, slip-angle, slip-ratio, pacejka, magic-formula, friction-circle, drifting, game-programming]
level: advanced
status: verified
description: "Model tire forces for driving games: slip ratio and slip angle, Pacejka vs simplified curves, combined slip via the friction circle, and low-speed stability fixes."
sources: ["https://www.edy.es/dev/docs/pacejka-94-parameters-explained-a-comprehensive-guide/", "https://docs.unity3d.com/Manual/class-WheelCollider.html", "https://www.asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tire friction models

**Goal:** tire forces that produce believable grip, slides and drifts, from arcade-forgiving to
sim-like, without low-speed jitter.

## Inputs per wheel
- **Slip ratio** (longitudinal): `(wheelAngularVel * radius - forwardSpeed) / max(|forwardSpeed|, eps)`.
  Positive when spinning (acceleration), negative when locking (braking).
- **Slip angle** (lateral): `atan2(lateralSpeed, |forwardSpeed|)` at the contact patch.
- **Load** `Fz`: suspension force from the wheel (see game-physics raycast-vehicle-suspension).

## Force curves
Real tires: force rises roughly linearly with slip, peaks, then falls off to a lower sliding value. Monster's Car Physics
for Games shows a longitudinal peak at about 6% slip ratio; the exact shape varies per tyre and surface.
**Pacejka Magic Formula**:
```
F = Fz * D * sin(C * atan(B*x - E*(B*x - atan(B*x))))
x = slip (ratio or angle); B stiffness, C shape, D peak (friction coefficient), E curvature
```
Illustrative starting values (lateral): B = 10, C = 1.9, D = 1.0, E = 0.97 peak at a slip angle of 10.3 degrees (computed;
lower B moves the peak later). Treat them as a tuning start, not tyre data. The full Pacejka sets make coefficients depend
on load and camber; games often use the simplified 4-parameter form.
**Arcade simplification**: piecewise linear (linear up to peak slip, then constant or slowly falling),
or Unity WheelCollider's friction curve (extremum slip 0.4 / value 1, asymptote slip 0.8 / value 0.5, stiffness 1 by default).

## Combined slip (friction circle)
A tire cannot deliver full longitudinal and lateral force at once:
```
Fx_raw, Fy_raw from separate curves
total = sqrt(Fx_raw^2 + Fy_raw^2); limit = mu * Fz
if total > limit: scale both by limit / total
```
(Better: compute combined slip magnitude, evaluate one curve, distribute by slip direction.) This is
what makes braking while turning reduce cornering grip, and enables power-oversteer drifts.

## Low-speed problems and fixes
Slip formulas divide by speed: near zero they explode, causing jitter and creeping. Fixes:
- Blend to a simple velocity-damping/static-friction model below a low-speed threshold (tune per game).
- Relaxation length: filter slip over distance travelled rather than time, which also adds realistic tire lag.
- Higher physics rate for the tyre model, with sub-stepping.

## Tuning for feel
Arcade: high peak, gentle falloff (forgiving slides), strong yaw damping. Drift games: low lateral
falloff, strong rear power, counter-steer assist. Expose curves in data and visualise slip/force per
wheel in a debug HUD.

## Verify
- [ ] Car at rest on a slope with handbrake does not creep or jitter.
- [ ] Debug plot of lateral force vs slip angle shows the intended peak and falloff.
- [ ] Hard braking in a corner reduces lateral grip (friction circle active).
