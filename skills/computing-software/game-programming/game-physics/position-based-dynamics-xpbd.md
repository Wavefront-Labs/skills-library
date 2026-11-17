---
id: computing-software.game-programming.game-physics.position-based-dynamics-xpbd
name: position-based-dynamics-xpbd
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, constraint-solver, xpbd, position-based-dynamics, pbd, cloth, ropes, soft-bodies, substepping, compliance, game-programming]
level: advanced
status: verified
description: "Simulate ropes, cloth and soft bodies with XPBD: predict positions, project constraints with compliance, substepping, and stiffness independent of iterations."
sources: ["https://matthias-research.github.io/pages/publications/XPBD.pdf", "https://matthias-research.github.io/pages/publications/smallsteps.pdf", "https://matthias-research.github.io/pages/tenMinutePhysics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Position-based dynamics (PBD / XPBD)

**Goal:** stable ropes, cloth, hair and soft bodies that are cheap, controllable and never explode,
using Mueller's position-based dynamics with the XPBD compliance extension.

## Algorithm (one substep)
```
for each particle i:
    v_i += dt * f_ext / m_i          # gravity etc.
    p_prev_i = x_i
    x_i += dt * v_i                  # predict
for each constraint j:               # one Gauss-Seidel pass per substep is enough when substepping
    project(j, dt)
for each particle i:
    v_i = (x_i - p_prev_i) / dt      # velocities derived from position change
```
Run N substeps per frame (Small Steps paper, Macklin et al.): n substeps of one iteration each are more accurate than
one step with n iterations.

## Distance constraint with compliance (XPBD)
```
C      = |x1 - x2| - restLength
n      = (x1 - x2) / |x1 - x2|
w      = w1 + w2                    # inverse masses (0 = pinned)
alpha  = compliance / (dt * dt)     # compliance = 1/stiffness; 0 = rigid
dLambda = -C / (w + alpha)          # per-substep (lambda reset to 0 each substep when 1 iteration)
x1 += w1 * dLambda * n
x2 -= w2 * dLambda * n
```
Plain PBD (alpha = 0 with a stiffness factor 0..1) has stiffness that depends on iteration count and
timestep; XPBD's compliance gives physically meaningful stiffness independent of both.

## Building things
- **Rope:** chain of particles + distance constraints; add bending via distance between i and i+2.
- **Cloth:** grid of particles; stretch constraints on edges, shear on diagonals, bending on
  i/i+2 or dihedral constraints; pin top row (inverse mass 0).
- **Soft body:** tetrahedral mesh with edge distance + tetra volume constraints.
- **Collisions:** as inequality constraints projected in the same loop (only when `C < 0`); for
  friction, limit tangential displacement relative to normal correction.
- **Damping:** scale velocities or apply velocity-level damping after deriving `v`.

## Performance
- Constraints sharing particles cannot be solved in parallel naively; use graph coloring (batches with
  no shared particles) or Jacobi iteration with averaging for GPU.
- Store particles as SoA arrays; constraints as index pairs.

## Rigid bodies
Rigid bodies can be done with XPBD too (Mueller et al. 2020, "Detailed Rigid Body Simulation with Extended Position
Based Dynamics"), but most game engines keep impulse solvers for rigid bodies.

## Verify
- [ ] Rope stretch under gravity matches the chosen compliance regardless of substep count (a 1 kg particle on a rigid
  anchor with compliance 1e-3 stretched 0.00981 m at 5 substeps vs the expected m*g*compliance = 0.00981; 0.0099 at 20
  and 0.0107 at 50, so expect small residual differences).
- [ ] Pinned cloth hangs without jitter after 10 s; no explosions when grabbing and yanking it.
- [ ] Frame cost scales linearly with substeps and constraint count.
