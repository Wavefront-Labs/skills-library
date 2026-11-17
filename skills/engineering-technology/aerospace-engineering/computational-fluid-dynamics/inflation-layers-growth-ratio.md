---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.inflation-layers-growth-ratio
name: inflation-layers-growth-ratio
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, meshing, mesh-generation, inflation-layers, prism-layers, growth-ratio, boundary-layer-mesh, near-wall-mesh]
level: practitioner
status: draft
description: "Design prism or inflation layers: total thickness against boundary-layer thickness, growth ratio, layer count, and a smooth transition to the core mesh."
sources:
  - "Solver and mesher user guides (prism or inflation layer sections)"
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
  - "AIAA CFD best-practice papers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Inflation layers and growth ratio

**Goal:** a near-wall mesh that resolves the boundary layer without bad transitions.

## Rules of thumb
1. Boundary-layer thickness estimate: turbulent flat plate `delta ~ 0.37 x / Re_x^0.2`. Layers should cover at least that, preferably 1.5 times, near the trailing edge where it is thickest.
2. Growth ratio 1.1-1.2 (up to 1.3 with care); 20-40 layers for y+ about 1 meshes on aircraft wings, fewer with wall functions.
3. Last layer thickness near the neighbouring core cell size: avoid a jump larger than about 1.5-2 in cell size.
4. Prism layers must follow concave corners and trailing edges: use collapse or reduce the layers near sharp edges rather than allowing negative volumes.
5. Keep first-layer aspect ratio (streamwise to normal) in the hundreds to thousands, not millions: set streamwise spacing at the wing at 1-2% chord.

## Procedure
- Compute the first-layer height from `y+` (see that skill), choose growth ratio, layer count to reach target total thickness.
- Check volume mesh quality at the tips, junctions and trailing edges; fix collapsed layers.

## Failure modes
- Too few layers: the boundary layer edge falls in the stretched core mesh, giving wrong skin friction and early separation.
- Abrupt layer termination causes spurious vorticity.

## Verify
- [ ] Plot of the layer stack vs estimated boundary-layer thickness shows layer coverage.
- [ ] Mesh quality metrics remain acceptable after the layers are added.
