---
id: computing-software.game-programming.game-physics.time-of-impact-solving
name: time-of-impact-solving
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, ccd, continuous-collision-detection, time-of-impact, toi, conservative-advancement, bullet-bodies, substepping, box2d, game-programming, conservative-advancement-ccd]
level: advanced
status: verified
description: "Compute time of impact for rotating convex bodies: conservative advancement, separation root finding, TOI sub-stepping, bullet flags and robustness trade-offs."
sources: ["https://box2d.org/files/ErinCatto_ContinuousCollision_GDC2013.pdf", "https://realtimecollisiondetection.net/books/rtcd/", "https://box2d.org/documentation/md_simulation.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Time of impact (TOI) solving

**Goal:** find the first moment two moving, rotating bodies touch within a step, and resolve the
step so fast bodies never pass through each other (Erin Catto, GDC 2013 "Continuous Collision").

## Problem
Linear sweeps handle translation; rotation makes the motion of each point non-linear (a spinning
thin plank can tunnel even when its centre moves slowly). TOI finds `t` in [0, 1] where the separation
distance first reaches a small target (linear slop), considering both translation and rotation.

## Conservative advancement (simple, robust)
```
t = 0
loop:
    d = distance(A at t, B at t)                 # GJK closest distance
    if d < target: return t
    bound = |v_rel| + |w_A| * rmax_A + |w_B| * rmax_B   # max approach speed along any direction
    dt = (d - target) / bound
    t += dt
    if t > 1: return no hit
```
Always safe (never steps past contact), but can need many iterations for rotating bodies.

## Box2D approach (separating-axis root finding)
1. Compute closest features with GJK at current t.
2. Build a separation function along the separating axis from those features (point-point,
   point-face or face-face).
3. Root-find (bisection + secant) the time where that separation equals the target.
4. Repeat with new features until converged. Faster convergence than plain conservative advancement.

## Integrating TOI into the step
- Run the normal discrete step, then for bodies flagged as fast/**bullets** (or all dynamic vs static),
  compute TOI events, advance the involved bodies to the earliest TOI, solve a small contact
  sub-problem for just those bodies, and continue the remaining time (TOI sub-stepping).
- Typical policy: dynamic vs static always continuous; dynamic vs dynamic only for bodies marked bullet
  (cost grows quickly).
- Cap TOI iterations and sub-steps; when the cap is hit, accept a small penetration and let position
  correction push out.
- Box2D v3 simplified this with "speculative" margins plus continuous for fast bodies vs static; `isBullet` bodies also run
  a continuous check against dynamic and kinematic bodies after the non-bullet pass (see `b2BodyDef` comments).

## Artifacts to know
- **Time loss**: bodies stopped at TOI lose the remaining fraction of motion that step (they appear
  to stick briefly). Accepted trade-off in most engines.
- Thin geometry: target separation (slop) must be smaller than the thinnest shape.

## Verify
- [ ] A spinning thin plank at high angular velocity does not pass through a thin wall.
- [ ] Bullet-flagged projectile vs moving dynamic target registers contact at 30 Hz.
- [ ] Per-step TOI iteration counts logged; stay under the cap in stress scenes.
