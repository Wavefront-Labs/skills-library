---
id: computing-software.game-programming.game-physics.impulse-based-collision-response
name: impulse-based-collision-response
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, impulse-resolution, coulomb-friction, restitution, sequential-impulses, contact-solver, warm-starting, game-programming]
level: advanced
status: verified
description: "Resolve contacts with impulses: normal impulse with restitution, Coulomb friction clamping, accumulated impulses, warm starting, and Baumgarte vs split-impulse correction."
sources: ["https://box2d.org/files/ErinCatto_SequentialImpulses_GDC2006.pdf", "https://box2d.org/posts/2024/02/solver2d/", "https://www.chrishecker.com/images/e/e7/Gdmphys3.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Impulse-based collision response

**Goal:** stacked boxes that rest, bounce and slide correctly, using sequential impulses (Catto,
Box2D).

## Normal impulse for one contact point
Contact normal `n` (from B to A or vice versa, be consistent), offsets `rA`, `rB` from each centre of
mass. Relative velocity at the point: `vRel = (vB + ωB × rB) − (vA + ωA × rA)`, `vn = dot(vRel, n)`.
Effective mass:
```
kN = mA⁻¹ + mB⁻¹ + dot(n, (IA⁻¹ (rA × n)) × rA + (IB⁻¹ (rB × n)) × rB)
λ  = −(1 + e) vn / kN                      // e = restitution
```
Apply `P = λ n`: `vA −= mA⁻¹ P; ωA −= IA⁻¹ (rA × P); vB += mB⁻¹ P; ωB += IB⁻¹ (rB × P)`. Checked numerically with random
masses, inertias and offsets: post-impact `vn` equals `−e * vn` exactly (n points from A to B, so approach is `vn < 0`).

## Accumulate and clamp (the key to stable stacking)
Iterate all contacts several times (4-10 velocity iterations). Clamp the **accumulated** impulse, not
the incremental one:
```
old = c.normalImpulse
c.normalImpulse = max(old + dλ, 0)         // contacts push, never pull
dλ = c.normalImpulse − old                 // apply only the change
```

## Friction (Coulomb)
Two tangent directions `t1, t2` (or one in 2D). Same effective-mass formula with `t` in place of `n`;
target relative tangential velocity 0. Clamp accumulated friction to the cone (pyramid
approximation per axis): `|λt| ≤ μ λn`, using the current accumulated normal impulse. Combine
materials with `μ = sqrt(μA μB)` (Box2D v3 default, `b2MixFriction`; restitution is mixed separately and both can be
overridden by callbacks) or engine-specific min/max/average modes.

## Restitution done right
- Compute `vn` **before** the solver iterations (store it as the restitution target), otherwise
  bounce depends on iteration order.
- Apply restitution only if `−vn > threshold` (Box2D v3 `restitutionThreshold` defaults to 1 m/s); below it set `e = 0`, or
  resting objects jitter.

## Warm starting
Keep each contact's accumulated impulses across frames (match contacts by feature id, see
`contact-manifold-generation`) and apply them at the start of the step. Stacks converge in a few
iterations instead of sinking.

## Position error
Penetration remains after velocity solving. Options:
- **Baumgarte:** add a bias `β/dt * max(depth − slop, 0)` to the velocity target (β ~ 0.1-0.2, slop ~ 0.005 m, the
  Box2D v2.4 `b2_linearSlop`). Simple, adds energy (objects pop).
- **Split impulses / NGS / soft step:** solve position separately or with soft constraints so
  correction does not become bounce velocity. Box2D v3 uses soft step with relax iterations.

## Verify
- [ ] A 10-box stack rests without sinking or jitter for 60 s.
- [ ] e = 1 ball bounces to roughly its drop height; e = 0 stays down.
- [ ] A box on a slope at angle `atan(μ)` is on the verge of sliding.
