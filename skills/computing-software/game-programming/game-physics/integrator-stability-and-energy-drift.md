---
id: computing-software.game-programming.game-physics.integrator-stability-and-energy-drift
name: integrator-stability-and-energy-drift
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, integrator-stability, energy-drift, numerical-integration, game-programming]
level: practitioner
status: verified
description: "Diagnose physics instability: energy plots, spring stiffness vs timestep limits, explicit Euler blow-up, symplectic choices and fixes for jitter."
sources: ["https://gafferongames.com/post/integration_basics/", "https://box2d.org/posts/2024/02/solver2d/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing instability and energy drift

**Goal:** tell numerical instability apart from logic bugs and fix it at the source.

## Measure energy
Log total energy per step: `E = sum(0.5*m*|v|^2 + 0.5*w.I.w + m*g*h) + spring energy`.
- Steadily **rising** energy in a closed system: unstable integrator or overly stiff constraint.
- Steady **falling**: damping (often fine, sometimes too much from position correction).
- **Spikes** at contacts: penetration recovery (Baumgarte) injecting velocity.

## Common causes
- **Explicit Euler** (`x += v*dt; v += a*dt`) gains energy on oscillators; switch to semi-implicit
  (symplectic) Euler: update `v` first, then `x` with the new `v`. Energy then oscillates but stays bounded.
- **Stiffness vs timestep:** a spring of stiffness k and mass m is stable with symplectic Euler only
  when `dt < 2/omega`, `omega = sqrt(k/m)` (measured on a unit oscillator: dt*omega = 1.99 stays bounded, 2.01 diverges). A light body on a stiff spring breaks first. Fix with
  substeps, soft constraints (frequency/damping-ratio form), or implicit integration.
- **Large mass ratios** (a heavy body on light stacked or jointed ones) converge slowly in iterative solvers and look
  "springy"; substep (the Small Steps paper shows this beats more iterations), or cheat masses.
- **Variable dt** fed to the solver; always fixed step with accumulator.
- **Gyroscopic term** from explicit `w x Iw` on long thin bodies blows up spin; integrate it
  implicitly or drop it (many engines do).

Measured on a unit oscillator (dt = 0.1, 10,000 steps, start energy 0.5): explicit Euler reached 8e42, symplectic Euler
stayed within 0.4936 to 0.5263, RK4 ended at 0.49993.

## Fixes in order
1. Fixed timestep, semi-implicit Euler.
2. Substepping (Box2D v3 uses soft step with substeps).
3. Soft constraints instead of raw stiff springs.
4. Clamp max angular/linear velocity as a safety net and log when it triggers.

## Verify
- Pendulum or spring test runs 10 minutes of sim time with energy within a few percent.
- Halve dt: if the bug disappears, it is stability, not logic.
