---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-fluid-simulation-stable-fluids-sph
name: gpu-fluid-simulation-stable-fluids-sph
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, fluid-simulation, sph, stable-fluids, navier-stokes, jacobi-pressure, compute-shader]
level: advanced
status: draft
description: "Simulate fluids on the GPU: grid-based stable fluids (advect, divergence, Jacobi pressure, projection) and particle SPH with spatial hashing, with boundary and stability notes."
sources: ["https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu", "https://www.dgp.toronto.edu/public_user/stam/reality/Research/pdf/GDC03.pdf", "https://matthias-research.github.io/pages/publications/sca03.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU fluid simulation

## 1. Stable fluids on a grid (Stam; GPU Gems ch38)
State: velocity field `u` (RG16F), pressure `p` (R16F), dye/density (RGBA16F). Each step, all as
fullscreen or compute passes with ping-pong textures:
1. **Advect** (semi-Lagrangian, unconditionally stable):
```glsl
vec2 pos = uv - dt * texture(vel, uv).xy * texelSize;   // trace back
newQ = texture(q, pos);                                   // bilinear
```
2. **Add forces** (splats from input, buoyancy).
3. **Vorticity confinement** (optional) to restore swirl lost to numerical diffusion.
4. **Divergence**: `div = 0.5 * ((uR.x - uL.x) + (uT.y - uB.y))` (in grid units).
5. **Pressure solve**: 20-60 Jacobi iterations
   `p = (pL + pR + pB + pT - div) * 0.25`.
6. **Project**: `u -= 0.5 * vec2(pR - pL, pT - pB)` making velocity divergence-free.
7. Boundaries: no-slip velocity (negate at walls), pure Neumann pressure (copy neighbour).

Use MacCormack/BFECC advection for sharper detail; multigrid instead of Jacobi for large grids.

## 2. SPH (particles; Muller et al. 2003)
Per step:
1. **Spatial hash / grid sort**: cell = floor(pos / h); radix or counting sort particles by cell,
   build cell start/end tables.
2. **Density**: `rho_i = sum_j m * W_poly6(|r_ij|, h)` over 27 neighbouring cells.
3. **Pressure**: `p_i = k * (rho_i - rho0)` (or Tait equation for stiffer fluids).
4. **Forces**: pressure gradient with spiky kernel, viscosity with viscosity kernel, gravity.
5. **Integrate**: symplectic Euler; clamp velocity; collide with boundaries.
Position Based Fluids (Macklin & Muller 2013) allow larger time steps.

## 3. GPU implementation notes
- Grid sims map naturally to textures; use compute with shared memory tiles for the Jacobi stencil.
- SPH neighbour search dominates; sort particles each frame for memory coherence.
- Render SPH with screen-space fluid rendering (depth splat, bilateral smoothing, normal from
  depth) or marching cubes in compute.

## Gotchas
- Time step must satisfy CFL for explicit parts (`dt * maxVel < cellSize`) or SPH explodes.
- fp16 velocity fields accumulate error; use fp32 for pressure.
- Too few Jacobi iterations leave residual divergence: fluid looks compressible and loses volume.

## Verify
- [ ] Divergence after projection near zero (visualise).
- [ ] SPH rest density stays within a few percent of rho0 at equilibrium.
