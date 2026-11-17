---
id: computing-software.game-programming.game-physics.fixed-timestep-and-collision-detection
name: fixed-timestep-and-collision-detection
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, fixed-timestep, accumulator, interpolation, semi-implicit-euler, symplectic-euler, verlet, integration, collision-detection, broad-phase, narrow-phase, aabb, sweep-and-prune, bvh, spatial-hash, sat, separating-axis-theorem, gjk, ccd, tunnelling, determinism, rigid-body, constraint-solver]
level: advanced
status: verified
description: "Make game physics stable and frame-rate independent: fixed timestep with accumulator and interpolation, semi-implicit Euler, broad/narrow phase, tunnelling and CCD, determinism."
sources: ["https://gafferongames.com/post/fix_your_timestep/", "https://box2d.org/documentation/", "https://jrouwe.github.io/JoltPhysics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed timestep and collision detection

**Goal:** physics that gives the same result at 30 or 240 fps, doesn't explode or let
fast objects pass through walls, and scales to many bodies. Applies whether you write
your own or tune an engine's (PhysX, Jolt, Box2D).

## 1. Fixed timestep with an accumulator
Variable `dt` makes springs, stacking and jumps behave differently per machine. Step the
simulation in fixed increments and render an interpolated state:
```cpp
const double DT = 1.0 / 60.0;          // physics step (Godot's default is 60 ticks per second; Unity: Project Settings > Time > Fixed Timestep)
double accumulator = 0.0;
State previous, current;

while (running) {
    double frame = std::min(clock.elapsed(), 0.25);   // clamp: avoid the spiral of death
    accumulator += frame;
    while (accumulator >= DT) {
        previous = current;
        integrate(current, DT);
        accumulator -= DT;
    }
    double alpha = accumulator / DT;                   // 0..1 into the next step
    render(lerp(previous, current, alpha));            // slerp for rotations
}
```
- **Spiral of death:** if one step costs more than `DT` of real time, the accumulator grows
  forever. The clamp (0.25 s) and a max-steps-per-frame cap trade slow-motion for survival.
- Interpolation adds up to one step of visual latency; extrapolation avoids that but
  overshoots on collisions. Interpolation is the usual choice.

## 2. Integration
Use **semi-implicit (symplectic) Euler** — update velocity first, then position with the
*new* velocity:
```
v += (F / m) * dt
x += v * dt
```
Explicit Euler (position with the old velocity) gains energy and blows up orbits and
springs (a unit-mass k=100 spring over 10 s at 60 Hz: energy 6.9e8 instead of 50); semi-implicit is just as cheap and stays
bounded (53). Semi-implicit Euler on a spring is stable only while `sqrt(k/m) * dt < 2`. Verlet
(`x_new = 2x - x_old + a*dt²`) is popular for cloth/ropes because constraints become
simple position projections. Apply damping as `v *= 1 / (1 + c*dt)` rather than
`v *= 0.99` per step (which depends on step rate: after 1 s the speed is 0.74, 0.55 and 0.30 of the start at 30, 60 and 120 Hz, versus 0.552, 0.550 and 0.550 for `1/(1+c*dt)` with c = 0.6).

## 3. Collision detection pipeline
1. **Broad phase** — cheaply find pairs that *might* touch, avoiding O(n²):
   - Uniform grid / spatial hash: great when objects are similar in size.
   - Sweep-and-prune on AABB intervals: good for mostly coherent motion.
   - Dynamic AABB tree (BVH) with fattened boxes: general-purpose default (Box2D uses one tree per body type; Jolt uses AABB quad trees per broad-phase layer).
2. **Narrow phase** — exact tests on candidate pairs:
   - Sphere–sphere: `|c1−c2|² ≤ (r1+r2)²` (compare squared distances, skip `sqrt`).
   - AABB–AABB: overlap on every axis.
   - Convex polygons/OBBs: **Separating Axis Theorem** — test face normals (and edge
     cross products in 3D); the axis with minimum overlap gives the contact normal and
     penetration depth. Measure the overlap as the translation needed to separate along
     the axis, `min(maxA - minB, maxB - minA)`: the plain intersection of the two projected intervals
     under-reports when one contains the other (it was wrong for 55 of 273 random overlapping 2D box pairs).
   - General convex shapes: **GJK** for distance/intersection, EPA for penetration depth.
3. **Contact generation** — normal, depth and 1–4 contact points (a box resting on the
   floor needs multiple points or it rocks).
4. **Resolution** — impulse-based solver with several iterations (Sequential Impulses;
   typically 4–10 velocity iterations; Jolt defaults to 10 velocity and 2 position steps, Box2D recommends 4 sub-steps), plus position correction (Baumgarte, soft contacts or split
   impulses) with a small **slop** (Box2D 0.005 m, Jolt 0.02 m) so resting contacts don't jitter.

## 4. Tunnelling and CCD
An object moving more than its own thickness per step can skip a thin wall entirely
(a 0.1 m bullet at 300 m/s moves 5 m per 60 Hz step). Fixes, cheapest first:
- Thicker colliders for static geometry; cap max speed.
- Raycast/shape-cast from previous to current position for fast small objects
  (bullets are usually hitscan or ray-marched projectiles, not physics bodies).
- Enable **continuous collision detection** only on the fast bodies (Unity:
  Continuous/Continuous Dynamic/Continuous Speculative; PhysX: `eENABLE_CCD`; Box2D `isBullet`) — it's costly.
- Smaller substeps for the whole sim as a last resort.

## 5. Determinism (lockstep, replays, rollback)
Same inputs → same output requires: fixed timestep, fixed iteration order (sort
contacts/bodies by stable IDs, not pointer addresses or hash-map order), no
frame-time-dependent code, and consistent floating point. Cross-platform float
determinism is hard: Box2D's docs say it needs precise math on MSVC, no floating-point contraction on clang/GCC and its own
`atan2`, `cos` and `sin`; Jolt has a `CROSS_PLATFORM_DETERMINISTIC` CMake option (about 8% slower) and warns that
listener callbacks and broad-phase queries are not deterministic in order. Many RTS/fighting games use fixed-point math or a deterministic
engine mode instead.

## Gotchas
- Units: keep 1 unit = 1 m and objects 0.1–10 m; tiny or huge scales break tolerances
  tuned for metres (Box2D famously warns against using pixels as units).
- Mass ratios beyond ~10:1 in stacks/joints make iterative solvers soft and wobbly.
- Moving a body by setting its position each frame skips the solver — use velocities (PhysX docs: `setGlobalPose` teleports, a kinematic target interacts properly).

## Verify
- [ ] Same scripted input gives the same trajectory at 30, 60 and 240 fps render rates.
- [ ] A frame hitch (e.g. 0.5 s pause) doesn't explode the sim.
- [ ] Fastest projectile can't pass the thinnest wall.
- [ ] Stack of 10 boxes comes to rest without jitter.
- [ ] Broad phase keeps pair tests far below n² at your max body count (profile it).

## Checked (2026-10-22)
- Ran in Python: explicit vs semi-implicit Euler on a spring (energy 6.9e8 vs 53, start 50); semi-implicit with omega*dt = 2.3 diverged (1e93) while 1.26 stayed bounded; damping at 30/60/120 Hz; accumulator loop at 30, 60 and 240 fps gives identical 120 steps and identical final x; 300 m/s / 60 = 5 m per step; SAT depth versus a 7200-direction brute-force minimum translation on 273 random box pairs (0 mismatches with the translation measure, 55 with the interval-intersection measure); sphere-sphere squared-distance test equals the sqrt test on 100,000 cases.
- Gaffer On Games 'Fix Your Timestep' (fetched): spiral of death, frame time clamp 0.25, interpolation with alpha = accumulator / dt.
- Box2D main: `B2_LINEAR_SLOP` 0.005 m, docs on sub-steps (4), pixels note (`b2SetLengthUnitsPerMeter`), determinism section (compiler flags, own trig). Jolt master: `mPenetrationSlop` 0.02, 10 velocity / 2 position steps, `Docs/Architecture.md` determinism caveats and 8% figure. PhysX docs: `setGlobalPose` vs kinematic target. Unity `CollisionDetectionMode` page (Continuous, ContinuousDynamic, ContinuousSpeculative); Godot `ProjectSettings` default 60 ticks.
- Removed Unity '0.02', Unreal and Havok/Chaos/Bullet mentions (not checked). The C++ loop is Gaffer's pattern; its behaviour was run as the Python accumulator.
