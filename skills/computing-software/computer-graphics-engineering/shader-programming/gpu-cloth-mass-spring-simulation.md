---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-cloth-mass-spring-simulation
name: gpu-cloth-mass-spring-simulation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, cloth-simulation, mass-spring, position-based-dynamics, verlet-integration, xpbd, compute-shader]
level: advanced
status: draft
description: "Simulate cloth on the GPU with mass-spring or position-based dynamics: Verlet integration, structural/shear/bend constraints, graph colouring for parallel solves, and collisions."
sources: ["https://matthias-research.github.io/pages/publications/posBasedDyn.pdf", "https://matthias-research.github.io/pages/publications/XPBD.pdf", "https://www.cs.cmu.edu/afs/cs/academic/class/15462-s13/www/lec_slides/Jakobsen.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU cloth simulation

## 1. Representation
Grid of particles (position, previous position, inverse mass); constraints between neighbours:
structural (right, down), shear (diagonals), bend (two apart). Pinned particles have invMass = 0.

## 2. Verlet integration (Jakobsen)
```glsl
vec3 x = pos[i], xp = prev[i];
vec3 v = (x - xp) * damping;
prev[i] = x;
pos[i]  = x + v + gravity * dt * dt * invMass[i];
```

## 3. Constraint projection (PBD/XPBD)
For a distance constraint between i and j with rest length L:
```glsl
vec3 d = pj - pi; float len = length(d);
float C = len - L;
float w = wi + wj;
float alphaTilde = compliance / (dt * dt);          // XPBD; 0 = rigid
float dLambda = (-C - alphaTilde * lambda) / (w + alphaTilde);
vec3 corr = dLambda * d / len;
pi -= wi * corr;  pj += wj * corr;
```
XPBD makes stiffness independent of iteration count and time step.

## 4. Parallelisation
Constraints sharing a particle can't be solved concurrently (write races). Options:
- **Graph colouring**: partition constraints into independent sets (for a grid: 4 structural
  colours + 4 shear colours); one dispatch per colour per iteration.
- **Jacobi-style**: accumulate corrections with atomics (or gather per particle) then average;
  converges slower but fully parallel.
- Many substeps with one iteration each (Small Steps, Macklin 2019) beat few steps with many
  iterations.

## 5. Collisions
- Spheres/capsules for bodies: push particles out to the surface after constraint solving.
- Self-collision: spatial hash of particles; push apart those closer than thickness.
- Recompute normals per frame in a compute pass for rendering.

## Gotchas
- Gauss-Seidel order bias makes cloth drift; alternate solve order or use colouring.
- Large dt with stiff constraints jitters; prefer more substeps.
- fp16 positions are not enough for world-space cloth; use fp32.

## Verify
- [ ] Hanging cloth settles without jitter; stretch ratio within target (e.g. < 2%).
- [ ] Results identical regardless of dispatch order (colouring correct).
