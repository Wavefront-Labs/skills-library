---
id: computing-software.computer-graphics-engineering.rendering-techniques.bidirectional-path-tracing-and-photon-mapping
name: bidirectional-path-tracing-and-photon-mapping
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, bdpt, photon-mapping, vcm, bidirectional-path-tracing, caustics, light-transport]
level: sme
status: docs-checked
description: "Know when to use bidirectional path tracing, stochastic progressive photon mapping and VCM: light subpaths, connections with MIS, bias trade-offs, delta BSDF limits."
sources: ["https://pbr-book.org/3ed-2018/Light_Transport_III_Bidirectional_Methods", "https://cgg.mff.cuni.cz/~jaroslav/papers/2012-vcm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bidirectional path tracing and photon mapping

Sources: PBR Book 3rd edition chapter 16 (Light Transport III: Bidirectional Methods) and the
project page and abstract of Georgiev et al., "Light Transport Simulation with Vertex Connection
and Merging" (2012).

## 1. Why bidirectional methods
Integrators that build paths only from the camera and connect to lights only at the last vertex
can fail in tricky lighting. PBR Book example: a light illuminating only a small area of a
ceiling, so only paths whose second-to-last vertex lands in that area find light; most paths
contribute nothing and a few contribute a lot, giving a high-variance image. Bidirectional methods
start paths from both the camera and the light and connect them in the middle, and can be much
more efficient in such situations.

## 2. Bidirectional path tracing (BDPT)
- Generalises standard path tracing. Build a **camera subpath** (first vertex on the camera,
  next by intersection, then by sampling the BSDF and tracing rays) and a **light subpath**
  starting at the light, then connect pairs of vertices from the two subpaths with a visibility
  ray. A subset of the light subpath can also be connected directly to the camera by sampling a
  lens vertex (the light-tracing strategy, whose contributions are splatted onto the film).
- Unbiased and does not blur illumination, unlike stochastic progressive photon mapping.
- Variance is reduced further by applying multiple importance sampling to reweight the
  contributions of the connection strategies, which needs detailed information about the
  sampling densities of each path vertex.
- Limitation: a vertex whose BSDF consists only of Dirac delta components can never be
  connected to a vertex of the other subpath (zero probability of choosing a direction where
  the delta distribution is nonzero), so such vertices are flagged as not connectible.

## 3. Stochastic progressive photon mapping (SPPM)
A particle-tracing algorithm: paths start at the lights, and the integrator estimates
illumination by interpolating contributions from particles close to, but not exactly at, the
shading point. This introduces bias, but improves the convergence rate in many challenging
settings.

## 4. Vertex connection and merging (VCM)
Georgiev et al. reformulate photon mapping as a bidirectional path sampling technique, which
explains formally the relative efficiency of photon mapping and BDPT and allows combining them
via multiple importance sampling. The progressive version is consistent and handles direct
illumination, diffuse and glossy inter-reflections, and specular-diffuse-specular transport. It
inherits the high asymptotic performance of BDPT for most path types, and the efficiency of photon
mapping for specular-diffuse-specular effects. The paper's comparison: BDPT fails to reproduce
reflected caustics from a vase, while progressive photon mapping has difficulty with illumination
from a room seen in a mirror; VCM captures both.

## Gotchas
- BDPT's MIS weights need accurate per-vertex sampling densities; check that individual
  strategies agree where they overlap.
- SPPM trades bias (blur) for convergence; BDPT is the unbiased choice.

## Verify
- [ ] Caustic test scene (glass or vase on a diffuse floor) converges with a visible caustic.
- [ ] BDPT and path tracing agree on a scene without caustics.

## Checked

Method: docs-checked 2026-11-09 against the PBR Book 3ed chapter 16 introduction, the BDPT section (introduction, delta connectibility and light subpath to camera connection read) and the SPPM section introduction, and the VCM project page abstract. Dropped the kd-tree and hash-grid storage, radius-shrink details, the Veach thesis (not read), SmallVCM, the recursive dVCM formulation, the method-choice table and manifold next event estimation and path guiding remarks.
