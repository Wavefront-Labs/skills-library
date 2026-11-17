---
id: computing-software.game-programming.game-physics.epsilon-and-tolerance-handling
name: epsilon-and-tolerance-handling
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, epsilon-tolerance, numerical-robustness, floating-point, linear-slop, relative-epsilon, collision-detection, game-programming]
level: advanced
status: verified
description: "Choose tolerances in physics and geometry code: absolute vs relative epsilons, units-aware slop, robust predicates, degenerate inputs, and float precision far from the origin."
sources: ["https://realtimecollisiondetection.net/pubs/Tolerances/", "https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/", "https://box2d.org/documentation/md_simulation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Epsilon and tolerance handling

**Goal:** collision and geometry code that neither misses contacts nor jitters because of a magic
`1e-6` (Ericson, *Real-Time Collision Detection*, and his "Combined absolute and relative tolerances revisited" note).

## Absolute vs relative
- Absolute `|a − b| ≤ ε` works only when magnitudes are known (distances in a game with metre units).
- Relative `|a − b| ≤ ε * max(|a|, |b|)` scales with magnitude but fails near zero.
- Combined (Ericson): `|a − b| ≤ ε * max(1, |a|, |b|)`. When one ε cannot serve both regimes use two (Catto's suggestion in
  the same note): `|a − b| ≤ max(absTol, relTol * max(|a|, |b|))`.
- `float` has ~7 significant digits: at 10,000 m from the origin the spacing between floats is
  ~1 mm; at 100 km it is ~8 mm. A fixed 1e-6 m epsilon is meaningless there.

## Units-aware slop (tolerances with meaning)
Tie tolerances to world units and document them:
- **Linear slop** (allowed penetration before correction): Box2D uses 0.005 m (`B2_LINEAR_SLOP` in v3, `b2_linearSlop` in
  v2.4); prevents contact flicker.
- **Speculative/contact margin** (distance at which contacts are created early): Box2D v3 uses 4 x linear slop = 2 cm.
- **Angular slop**: Box2D v2.4 `b2_angularSlop` is 2 degrees; v3 has no such constant.
- Minimum feature size (smallest triangle edge, thinnest wall) should be several times the slop.
Put them in one header (`b2_linearSlop`, `PhysicsSettings`) so they stay consistent.

## Degenerate inputs
- Normalising a near-zero vector: check `lengthSq > ε²` first and choose a fallback direction.
- Parallel lines/planes in intersection tests: denominators near zero; handle the parallel case
  explicitly instead of dividing.
- Triangles with zero area (sliver triangles) in collision meshes: weld and remove at import.
- Raycast exactly along an edge or through a vertex: use consistent tie-breaking (half-open
  intervals) so a ray doesn't hit both or neither of two adjacent triangles.

## Robust techniques
- Prefer formulations that avoid subtraction of nearly equal large numbers: compute relative to a
  local origin (subtract the object position first).
- Fat tolerances in **tests** (did they touch?) and thin in **corrections** (how far to push).
- Use doubles for offline tools (mesh baking, navmesh) and large-world coordinates (Unreal 5 Large
  World Coordinates use doubles for positions); or rebase the origin (floating origin) when the
  player moves far away.
- Integer/exact predicates (orientation tests in fixed point) for robust geometry in tools.

## Verify
- [ ] Slop and margins defined once with units; no stray literal epsilons in collision code (grep).
- [ ] Resting-contact test at the origin and at 50 km away: jitter compared (motivates floating origin). 32-bit float spacing
  measured: 1000 m 0.061 mm, 10 km 0.98 mm, 100 km 7.8 mm.
- [ ] Fuzz intersection routines with parallel and degenerate inputs: no NaNs.
