---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-builtin-geometries
name: threejs-builtin-geometries
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, three-primitives, boxgeometry, extrudegeometry, lathegeometry, tubegeometry]
level: practitioner
status: verified
description: "Pick and parameterise three.js built-in geometries (Box, Sphere, Plane, Cylinder, Torus, Lathe, Extrude, Tube, Shape) with sane segment counts and UVs."
sources: ["https://threejs.org/manual/#en/primitives", "https://threejs.org/docs/pages/BoxGeometry.html", "https://threejs.org/docs/pages/ExtrudeGeometry.html", "https://threejs.org/docs/pages/TubeGeometry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js built-in geometries

## 1. Parameters that matter
```js
new THREE.BoxGeometry(w, h, d, wSeg, hSeg, dSeg);          // segments only for displacement
new THREE.SphereGeometry(r, 32, 16);                        // widthSeg, heightSeg
new THREE.PlaneGeometry(w, h, 128, 128);                    // lies in XY: rotateX(-PI/2) for ground
new THREE.CylinderGeometry(rTop, rBottom, h, 32, 1, openEnded);
new THREE.TorusKnotGeometry(1, 0.3, 128, 16);
new THREE.CapsuleGeometry(r, height, capSeg, radialSeg, heightSeg); // height = straight middle section
new THREE.IcosahedronGeometry(r, detail);                   // even triangles, good for planets
new THREE.LatheGeometry(points2D, 32);                      // revolve profile around Y (vases)
new THREE.ExtrudeGeometry(shape, { depth: 0.2, bevelEnabled: true, bevelSize: 0.02, bevelSegments: 3, curveSegments: 12 });
new THREE.TubeGeometry(curve, 200, 0.05, 8, false);         // along a CatmullRomCurve3
new THREE.ShapeGeometry(shape, curveSegments);              // flat 2D fill
new THREE.EdgesGeometry(geo, thresholdAngle);               // outlines with LineSegments
```
Bake orientation into the geometry once (`geo.rotateX`, `geo.translate`, `geo.center()`) instead of
rotating the mesh, so the pivot and bounding box match intent.

## 2. Segment budgets
- Flat shading or no displacement: minimal segments (box 1x1x1, plane 1x1).
- Sphere cost (measured, indexed): 24x12 = 325 vertices / 528 triangles, 32x16 = 561 / 960, 64x32 = 2,145 / 3,968. Silhouette quality is driven by width segments.
- Vertex displacement: segment count = displacement resolution; use a displacement map only with dense meshes.

## 3. UV and normals notes
- Box: each face has its own 0..1 UVs and split normals (hard edges).
- Sphere: UV seam and pole pinching; for planets use a cube-sphere or icosphere with triplanar mapping.
- ExtrudeGeometry has two groups (caps 0, sides 1): pass `[capMat, sideMat]`; side UVs scale with shape units, so tune `texture.repeat`.
- SVG to shapes: `SVGLoader.createShapes(path)` then ExtrudeGeometry; flip Y (SVG is Y-down).

## Gotchas
- Sharing one geometry across many meshes is free; creating a new one per mesh wastes memory.
- Parametric/legacy `Geometry` class is gone (r125); everything is BufferGeometry.
- Holes in Shape: `shape.holes.push(path)`. ShapeGeometry reverses an outline or hole itself when needed (it checks `isClockWise`), so a hole wound either way gave the same 8 triangles.

## Verify
- [ ] Triangle counts per primitive known (`geo.index.count / 3`; `IcosahedronGeometry` and the other Polyhedron shapes are NON-indexed, `geo.index` is null, so use `position.count / 3`).
- [ ] Ground plane faces up and lights correctly (normals +Y).

## Checked
- three 0.186.1 in Node 24: Box 24 verts 12 tris 6 groups, UVs 0..1; Sphere 32x16 gives 561 verts 960 tris; Cylinder has 3 groups; ExtrudeGeometry groups were caps 0 then sides 1; Icosahedron detail 0 is non-indexed with 20 triangles; PlaneGeometry normal (0,0,1), after `rotateX(-PI/2)` (0,1,0); Lathe of a profile at x=1 spans x and z from -1 to 1; TubeGeometry 200x8 gives 1809 verts; EdgesGeometry of a box gives 24 verts; CapsuleGeometry constructor read from source is (radius, height, capSegments, radialSegments, heightSegments), the skill wrote `length`; `Geometry.js` exists at tag r124 and 404s at r125; `SVGLoader.createShapes` is a static method in the addon source; sphere vertex and triangle counts for 24x12, 32x16 and 64x32 as quoted. Source links moved to threejs.org/docs/pages/<Name>.html because the old `#api/en/` hashes no longer load.
