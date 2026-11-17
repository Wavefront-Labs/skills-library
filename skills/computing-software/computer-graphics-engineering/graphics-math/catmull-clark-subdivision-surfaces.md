---
id: computing-software.computer-graphics-engineering.graphics-math.catmull-clark-subdivision-surfaces
name: catmull-clark-subdivision-surfaces
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, curves-surfaces, subdivision-surfaces, catmull-clark, loop-subdivision, opensubdiv, creases]
level: sme
status: draft
description: "Implement and use subdivision surfaces: Catmull-Clark and Loop rules, creases and boundaries, limit positions, OpenSubdiv evaluation, and GPU tessellation."
sources: ["https://graphics.pixar.com/opensubdiv/docs/subdivision_surfaces.html", "https://graphics.pixar.com/opensubdiv/docs/intro.html", "https://www.realtimerendering.com/", "https://dl.acm.org/doi/10.1145/280814.280826"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subdivision surfaces

## 1. Catmull-Clark rules (one step, quads or general polygons)
1. **Face point** F = average of the face's vertices.
2. **Edge point** E = average of the edge's two endpoints and the two adjacent face points.
   Boundary/sharp edge: midpoint of the edge.
3. **Vertex point** V' = (Q + 2R + (n-3)S) / n, where n = valence, Q = average of adjacent face points,
   R = average of adjacent edge midpoints, S = old vertex.
   Boundary vertex: (E1 + 6S + E2)/8 using the two boundary neighbours (B-spline curve rule).
4. Connect: each n-gon becomes n quads (face point, edge points, vertex point).
After one step the mesh is all quads; extraordinary vertices (valence != 4) remain and stay isolated.

## 2. Loop subdivision (triangles)
Edge point = 3/8 (endpoints) + 1/8 (opposite vertices); vertex = (1 - n beta) S + beta * sum(neighbours),
beta = 3/16 for n = 3, else 3/(8n).

## 3. Creases
Semi-sharp creases (DeRose et al. 1998): an edge with sharpness s uses sharp rules for floor(s) levels, then
smooth rules, with fractional blending. Vertex rules: smooth / dart / crease / corner depending on the
number of sharp incident edges. Standard in USD, Pixar, Blender (edge crease).

## 4. Production evaluation
- **OpenSubdiv**: build a `Far::TopologyRefiner` from the base mesh, `RefineUniform` or `RefineAdaptive`, then
  evaluate with `Osd` on CPU/GPU every frame (topology analysed once, only positions change for animation).
- Limit positions/normals: evaluate the surface at infinite subdivision directly (stencils), for
  displacement baking and accurate normals.
- Feature-adaptive subdivision refines only near extraordinary vertices and creases; regular regions become
  bicubic B-spline patches drawn with hardware tessellation.

## Gotchas
- Triangles and n-gons under Catmull-Clark produce poles and pinching; model in quads with even edge flow.
- Displacement maps must be baked against the same subdivision scheme and level, including boundary
  interpolation rules (OpenSubdiv `VTX_BOUNDARY_EDGE_ONLY` vs `EDGE_AND_CORNER`) and UV interpolation mode.
- Memory grows 4x per level; render at adaptive level, not uniform level 4+.

## Verify
- [ ] A cube subdivides toward a sphere-like shape; with all edges creased at infinity it stays a cube; limit
  normals are continuous across patch boundaries (shading has no seams).
