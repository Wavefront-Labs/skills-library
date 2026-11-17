---
id: computing-software.game-programming.game-physics.soft-constraints-and-stable-springs
name: soft-constraints-and-stable-springs
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, constraint-solver, soft-constraints, spring-damper, stiffness-damping, frequency-damping-ratio, implicit-spring, stable-springs, game-programming]
level: advanced
status: verified
description: "Make springs and soft joints stable at game timesteps: specify frequency and damping ratio, soft constraint coefficients (Catto), and avoiding explicit-spring explosions."
sources: ["https://box2d.org/files/ErinCatto_SoftConstraints_GDC2011.pdf", "https://box2d.org/posts/2024/02/solver2d/", "https://gafferongames.com/post/spring_physics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft constraints and springs

**Goal:** suspension, ropes, mouse-drag joints and camera springs that stay stable at 60 Hz without
tuning by trial and error.

## Explicit springs explode
`F = -k x - c v` integrated explicitly is only stable when `dt` is small relative to the spring's
period (roughly `dt < 2/omega`, omega = sqrt(k/m)). Stiff springs or light bodies at 60 Hz exceed this
and the simulation blows up. Raising `k` to make it "stiffer" makes it worse. Catto (GDC 2011) puts the practical
rule as at least 4 steps per oscillation period for semi-implicit Euler (a 60 Hz oscillation needs 15 Hz steps or faster).

## Tune in frequency and damping ratio, not k and c
- `f` (Hz): how fast it oscillates. Keep `f` at most a quarter of the simulation rate (Catto's 4-steps-per-period rule,
  e.g. <= 15 Hz at 60 Hz); Jolt's docs state frequencies above half the simulation rate are unstable. The implicit form
  below stayed bounded in a test even at f = 60 Hz with a 30 Hz step, but the motion is then meaningless.
- `zeta`: 0 = undamped, 1 = critically damped (fastest settle without overshoot), >1 overdamped.
Convert with the effective mass `m`:
```
omega = 2*pi*f
k = m * omega^2
c = 2 * m * zeta * omega
```
These parameters mean the same thing whatever the body mass: designers can tune them.

## Soft constraint formulation (Catto, GDC 2011)
Treat the spring as a constraint with softness, solved implicitly inside the velocity solver:
```
gamma = 1 / (dt * (c + dt * k))         # constraint softness (CFM-like)
beta  = dt * k / (c + dt * k)           # position error feedback (ERP-like)
bias  = C * beta / dt
effectiveMass = 1 / (invMass + gamma)
lambda = -effectiveMass * (Cdot + bias + gamma * accumulatedLambda)
```
This is unconditionally stable for any `k`, `c` and `dt` (checked: f = 5 to 60 Hz at a 30 Hz step all decay to zero); a rigid
constraint is the limit k -> inf (gamma -> 0, beta -> 1). Catto notes that for impulse-based solvers gamma is divided by `h`.
Box2D's joints expose exactly `hertz` and `dampingRatio` for this reason; Box2D v3 also uses soft
contacts ("soft step") for contact stability.

## Simple stable springs without a solver
- **Implicit Euler for one spring:** solve `v' = (v - dt*(k/m)*x) / (1 + dt*c/m + dt*dt*k/m)` then `x' = x + dt*v'` (equals the
  exact backward-Euler 2x2 solve; checked numerically).
- **Critically damped smoothing** (cameras, UI): use the analytic `SmoothDamp` form instead of a
  physical spring.
- **Sub-stepping**: run the spring 4-8 sub-steps per frame when it must be explicit.

## Engine mapping
- Unity: `SpringJoint` uses `spring`/`damper` (k/c); `ConfigurableJoint` drives use
  `positionSpring`/`positionDamper`; 2D joints (`SpringJoint2D`) expose `frequency` and `dampingRatio`.
- Godot: `Generic6DOFJoint3D` springs, `DampedSpringJoint2D` (stiffness/damping).

## Verify
- [ ] Spring at the chosen f/zeta behaves identically when body mass is doubled (parameters in f/zeta).
- [ ] No explosion at 30 Hz simulation with f = 5 Hz.
- [ ] Critically damped setting settles with no visible overshoot.
