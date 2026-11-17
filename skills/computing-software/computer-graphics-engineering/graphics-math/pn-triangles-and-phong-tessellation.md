---
id: computing-software.computer-graphics-engineering.graphics-math.pn-triangles-and-phong-tessellation
name: pn-triangles-and-phong-tessellation
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, curves-surfaces, pn-triangles, phong-tessellation, curved-surfaces, tessellation, bezier-triangles]
level: advanced
status: draft
description: "Smooth coarse meshes on the GPU with PN triangles (cubic Bezier triangles from vertex normals) and Phong tessellation: control point formulas, quadratic normals and crack issues."
sources: ["https://alex.vlachos.com/graphics/CurvedPNTriangles.pdf", "https://perso.telecom-paristech.fr/boubek/papers/PhongTessellation/", "https://www.khronos.org/opengl/wiki/Tessellation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PN triangles and Phong tessellation

Both use only the triangle's vertex positions and normals (no neighbour data), so they slot into the
tessellation stage of any mesh to round silhouettes.

## PN triangles (Vlachos et al. 2001)
Build a cubic Bezier triangle with 10 control points:
```
b300 = P1, b030 = P2, b003 = P3
w_ij = dot(Pj - Pi, Ni)
b210 = (2 P1 + P2 - w12 N1) / 3        b120 = (2 P2 + P1 - w21 N2) / 3
b021 = (2 P2 + P3 - w23 N2) / 3        b012 = (2 P3 + P2 - w32 N3) / 3
b102 = (2 P3 + P1 - w31 N3) / 3        b201 = (2 P1 + P3 - w13 N1) / 3
E = (b210 + b120 + b021 + b012 + b102 + b201) / 6
V = (P1 + P2 + P3) / 3
b111 = E + (E - V) / 2
```
Evaluate at barycentric (u, v, w) with the cubic Bernstein polynomials. Normals use a separate
**quadratic** patch (6 coefficients) so inflections are shaded correctly.

## Phong tessellation (Boubekeur and Alexa 2008)
Cheaper: interpolate position linearly, project onto each vertex's tangent plane, interpolate the
projections, blend with shape factor alpha (about 0.75):
```glsl
vec3 p = u*P1 + v*P2 + w*P3;
vec3 c1 = p - dot(p - P1, N1) * N1, c2 = p - dot(p - P2, N2) * N2, c3 = p - dot(p - P3, N3) * N3;
vec3 phong = u*c1 + v*c2 + w*c3;
vec3 pos = mix(p, phong, alpha);
```

## Cracks
Hard edges (split vertices with different normals at the same position) produce cracks because each
side curves differently. Fixes: average normals for the geometry evaluation while keeping split
normals for shading, or keep crease edges straight (use the edge's linear interpolation).

## Limits
Only rounds silhouettes; cannot add detail (use displacement for that). Low-poly meshes with
non-uniform triangulation can bulge oddly.

## Verify
Tessellate a low-poly sphere (icosahedron): result should approach a sphere; check silhouettes and
crack-free hard edges in wireframe.
