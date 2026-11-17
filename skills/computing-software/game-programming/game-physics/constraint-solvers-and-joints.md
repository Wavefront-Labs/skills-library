---
id: computing-software.game-programming.game-physics.constraint-solvers-and-joints
name: constraint-solvers-and-joints
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, constraint-solver, joints, sequential-impulse, pgs, projected-gauss-seidel, solver-iterations, baumgarte-stabilization, hinge-joint, ragdoll-joints, jitter, constraint-explosion, warm-starting, position-correction, game-programming]
level: advanced
status: verified
description: "Tune rigid-body joints and the iterative constraint solver underneath them (sequential impulse/PGS) without jitter, sinking, or explosive instability."
sources: ["https://box2d.org/files/ErinCatto_SequentialImpulses_GDC2006.pdf", "https://box2d.org/posts/2024/02/solver2d/", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constraint solvers and joints

**Goal:** understand what "solver iterations" actually does so joints (hinges,
ragdolls, vehicle suspensions) hold their shape under load instead of jittering,
sinking into the ground, or exploding — this builds on
`computing-software.game-programming.game-physics.fixed-timestep-and-collision-detection`,
which covers integration and detecting contacts; this skill is about resolving
them and the explicit constraints (joints) layered on top.

## What the solver is actually doing
Common game physics engines (Box2D, PhysX, Jolt) use
**sequential impulse** (a form of Projected Gauss-Seidel; PhysX offers PGS and TGS solvers, Box2D v3 uses a soft-step variant with sub-stepping): every contact and
joint is a constraint ("these two bodies must not interpenetrate," "this hinge
angle stays within range"), and the solver iterates over all constraints
multiple times per step, applying small corrective impulses to each in turn,
letting the correction from one constraint propagate into the next iteration.
It is **not an exact solve** — it's an approximation that converges toward a
consistent solution with more iterations, which is why **solver iteration
count** is a real, visible quality/performance tradeoff: too few iterations
(the default is often fine for simple stacks, not for a tall stack or many
simultaneous joints) and constraints don't fully propagate within the frame,
showing up as **jitter** (objects vibrating in place) or a stack slowly sinking
through its own unresolved overlap. Measured on a 1D stack of ten unit boxes at 60 Hz (my own sequential-impulse
solver, accumulated-impulse clamping): without warm starting the residual speed after 2 s was 1.78 m/s at 4 iterations,
0.66 at 10 and 0.17 at 30; with warm starting it was 0.0004, 0 and 0. Defaults for scale: Jolt uses 10 velocity and 2 position
iterations; Box2D recommends 4 sub-steps.

## Baumgarte stabilization and position correction
Velocity-only constraint resolution corrects *future* motion but not *existing*
penetration (two bodies already overlapping stay overlapping if the solver only
fixes velocity). Engines add a position-correction term (Baumgarte
stabilization, or a separate split-impulse/position-solver pass in PhysX/Bullet)
that pushes overlapping bodies apart over a few frames rather than instantly (Jolt's `mBaumgarte` defaults to 0.2; Box2D v3 instead uses soft contacts with `contactHertz` 30 and a `contactSpeed` cap) —
tuned too aggressively, this itself causes visible popping/explosion on deep
penetration (common when a fast object tunnels partway into another before
collision is caught, see CCD in the fixed-timestep skill); tuned too gently,
objects visibly sink into each other before separating.

## Joints: what each type actually constrains
| Joint | Locks | Common use | Failure mode when misconfigured |
|---|---|---|---|
| Fixed/Weld | all 6 DOF | attach a static prop rigidly | over-constraining a long chain of welds amplifies tiny solver error into visible stretching |
| Hinge/Revolute | 1 rotational DOF free | door, wheel axle | wrong axis/anchor → spins around the wrong point or flings on contact |
| Ball/Spherical | 3 rotational DOF free | shoulder joint in a ragdoll | no limits set → limbs rotate through the body (ragdoll "spaghetti") |
| Slider/Prismatic | 1 translational DOF free | piston, elevator platform | missing travel limits → infinite travel through geometry |
| Spring/Distance | soft constraint toward a target distance | suspension, cloth-like tethers | stiffness too high behaves like a rigid joint and can explode; too low feels like nothing is connected |

Ragdolls are the joint case that goes wrong most often in practice: use angular
limits on every ball joint (shoulders, hips) matching real range of motion, and
keep **mass ratios between connected bodies reasonable** (a tiny hand bone
attached to a heavy torso with a stiff joint is a classic explosion source —
extreme mass ratios make the solver's impulses overshoot).

## Debugging instability — a checklist, not a guess
- **Jitter at rest**: raise solver iteration count first; if that doesn't fix
  it, check for near-duplicate/overlapping colliders on the same body (the
  solver fights itself resolving redundant contacts).
- **Explosion** (velocity suddenly huge): almost always deep initial
  penetration (objects spawned overlapping, or a fast collider tunneling) —
  the position-correction term is overcorrecting a large error in one step.
  Clamp max correction velocity (Jolt `mMaxPenetrationDistance` 0.2 m; Box2D `contactSpeed`, default 3 m/s) and fix the spawn
  overlap at the source.
- **Sinking**: solver iterations too low for the stack depth/joint chain
  length, or position correction disabled/too weak. Box2D notes that long joint chains stretch less with more sub-steps.
- **Warm-starting** (reusing last frame's impulse as the next frame's initial
  guess) is what makes resting stacks stable at low iteration counts in the
  first place — if you've written a custom solver and skipped it, expect to
  need far more iterations for the same stability.

## Verify
- [ ] A tall stack / long ragdoll chain at rest shows no visible jitter at the
      shipped solver iteration count on the actual target hardware.
- [ ] Every joint with rotational freedom has angular limits set to a plausible
      real-world range, not left unlimited by default.
- [ ] No object spawns pre-overlapping another collider (checked, not assumed).
- [ ] Mass ratios between directly-jointed bodies are within roughly one order
      of magnitude; extreme ratios are either avoided or iteration count is
      raised specifically for that joint chain. Measured (10 iterations, warm started, heavy box on top of the stack): residual speed 0.0003 m/s at 1:10,
      0.096 at 1:100 and 3.5 at 1:1000, versus 0 at 1:1.

## Checked (2026-10-22)
- Wrote a 1D vertical stack solver in Python (sequential impulse, accumulated clamping, 10 boxes, 60 Hz, 120 frames). Warm start off: residual max speed 6.98 / 1.78 / 0.66 / 0.17 m/s at 1/4/10/30 iterations; on: 0 / 0.00035 / 0 / 0. Mass ratio 1/10/100/1000 with the heavy box on top, 10 iterations, warm: 0 / 0.00027 / 0.096 / 3.46. Per-iteration clamping with warm start diverged (9.9 m/s) while accumulated clamping gave 1e-7, confirming the skill's warm-start and accumulation advice.
- Jolt master `PhysicsSettings.h`: `mBaumgarte = 0.2`, `mNumVelocitySteps = 10`, `mNumPositionSteps = 2`, `mMaxPenetrationDistance = 0.2`. Box2D main: `contactHertz = 30`, `contactSpeed = 3 * lengthUnits` (`src/types.c`), docs: soft constraints and sub-stepping ('long joint chains will stretch less with more sub-steps'), README 'Soft Step'. PhysX 5.4.1 docs list 'Projected Gauss-Seidel and Temporal Gauss-Seidel'.
- Catto GDC 2006 PDF (pypdf): bias impulse proportional to penetration, accumulated impulse clamping, several iterations. Removed Havok and Bullet from the engine list (not checked) and the dead GDC Vault source.
- The joint table and ragdoll advice is qualitative design guidance; the quantitative parts above were run.
