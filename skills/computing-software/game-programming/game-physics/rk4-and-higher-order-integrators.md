---
id: computing-software.game-programming.game-physics.rk4-and-higher-order-integrators
name: rk4-and-higher-order-integrators
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, integration, rk4, runge-kutta, numerical-integration, springs, orbital-mechanics, energy-drift, semi-implicit-euler, game-programming]
level: advanced
status: verified
description: "Know when RK4 beats semi-implicit Euler in games: implementing RK4 for state derivatives, its cost with collisions, and choosing integrators for springs and orbits."
sources: ["https://gafferongames.com/post/integration_basics/", "https://www.gafferongames.com/post/fix_your_timestep/", "https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RK4 and higher-order integrators

**Goal:** pick an integrator per simulation: semi-implicit Euler for contact-heavy rigid bodies,
RK4 (or smaller steps) where accuracy over long horizons matters and forces are smooth.

## What RK4 does
For state `x` (position, velocity) and derivative function `f(x, t)` (velocity, acceleration):
```
k1 = f(x,             t)
k2 = f(x + k1*dt/2,   t + dt/2)
k3 = f(x + k2*dt/2,   t + dt/2)
k4 = f(x + k3*dt,     t + dt)
x_next = x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
```
In code (Gaffer On Games style):
```cpp
struct State { float x, v; };
struct Deriv { float dx, dv; };
Deriv evaluate(const State& s, float t, float dt, const Deriv& d) {
    State st{ s.x + d.dx*dt, s.v + d.dv*dt };
    return { st.v, acceleration(st, t+dt) };
}
void rk4(State& s, float t, float dt) {
    Deriv a = evaluate(s, t, 0.0f, {});
    Deriv b = evaluate(s, t, dt*0.5f, a);
    Deriv c = evaluate(s, t, dt*0.5f, b);
    Deriv d = evaluate(s, t, dt, c);
    float dxdt = (a.dx + 2*(b.dx + c.dx) + d.dx) / 6.0f;
    float dvdt = (a.dv + 2*(b.dv + c.dv) + d.dv) / 6.0f;
    s.x += dxdt*dt; s.v += dvdt*dt;
}
```
Error per step is O(dt^5) (global O(dt^4)) versus O(dt^2) local (global O(dt)) for Euler variants. Measured on a damped
spring at t = 1: RK4 global order 3.6 to 3.8 at coarse steps (approaching 4), explicit Euler 1.02.

## Why most game physics engines still use semi-implicit Euler
- Contacts and constraints are discontinuous: RK4's intermediate evaluations would need collision
  detection and constraint solving 4 times per step; the accuracy gain is lost at each impact.
- Semi-implicit (symplectic) Euler conserves energy well on average for oscillators; it does not
  explode the way explicit Euler does.
- Cost: 4 force evaluations per step. Halving dt with Euler often buys more stability per CPU.

## Where RK4 (or similar) is worth it
- Smooth force fields without contacts: orbital mechanics, n-body, projectile ballistics with drag
  computed precisely for long ranges, camera springs needing exact settling, procedural animation.
- Offline/tool calculations (trajectory prediction lines) where determinism with the runtime matters
  less than accuracy. If the prediction line must match runtime exactly, use the **same** integrator
  and timestep as the runtime instead.
- Long-term orbits: symplectic integrators (velocity Verlet, leapfrog) conserve energy over very long
  times better than RK4, which slowly drifts.

## Stiff springs
Very stiff springs need tiny steps with any explicit method. Options: implicit integration, sub-stepping,
or soft-constraint formulations (see game-physics soft-constraints-and-stable-springs); analytic damped
spring solutions for camera smoothing.

## Verify
- [ ] Energy plot of a frictionless spring over 10,000 steps: Euler explicit grows, semi-implicit
  oscillates bounded, RK4 decays slowly (measured at dt = 0.1: explicit 8e42, symplectic 0.4936 to 0.5263, RK4 0.49993
  from 0.5).
- [ ] Orbit test: period and radius after 100 orbits within tolerance for the chosen integrator.
- [ ] Same results at fixed dt regardless of frame rate (fixed timestep in place).
