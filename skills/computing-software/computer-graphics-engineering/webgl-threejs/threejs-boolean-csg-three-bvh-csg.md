---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-boolean-csg-three-bvh-csg
name: threejs-boolean-csg-three-bvh-csg
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, three-bvh-csg, csg, boolean-geometry, constructive-solid-geometry]
level: advanced
status: docs-checked
description: "Run fast boolean union, subtract and intersect on three.js meshes with three-bvh-csg: Brush/Evaluator setup, materials, manifold requirements and real-time use."
sources: ["https://github.com/gkjohnson/three-bvh-csg", "https://github.com/gkjohnson/three-mesh-bvh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boolean geometry with three-bvh-csg

## 1. Setup
```js
import { Brush, Evaluator, SUBTRACTION, ADDITION, INTERSECTION, DIFFERENCE } from 'three-bvh-csg';
const a = new Brush(new THREE.BoxGeometry(2, 2, 2), matA);
const b = new Brush(new THREE.SphereGeometry(1.3, 48, 24), matB);
b.position.set(0.5, 0.5, 0); b.updateMatrixWorld();      // brushes use world matrices
const ev = new Evaluator();
ev.attributes = ['position', 'normal', 'uv'];            // attributes copied to the result (README default: position, uv, normal)
ev.useGroups = true;                                      // keep per-brush materials as groups
const result = ev.evaluate(a, b, SUBTRACTION);            // returns a Brush (a Mesh)
scene.add(result);
```
Chain operations by passing a result as an input. Pass a target brush: `ev.evaluate(a, b, op, result)` modifies it in place instead of creating a new one.

## 2. Input requirements
- Brush geometry must be **two-manifold** (watertight, no triangle interpenetration); the README warns that numerical precision can leave results not perfectly two-manifold.
- `HOLLOW_SUBTRACTION` and similar operations let brush A be non-manifold, but brush B must still be watertight.

## 3. Real-time use
When a brush moves, call `updateMatrixWorld()` and re-evaluate. The README says a brush's geometry should not be modified once created: build a new brush instead.

## 4. Post-process the result
- Normals: the result copies the attributes listed in `ev.attributes`; `computeVertexNormals` would smooth hard edges.
- Export: `GLTFExporter` on the result.

## Gotchas
- Result triangle count grows with every operation; simplify or rebuild from originals.

## Verify
- [ ] Result is watertight (no see-through seams) from all angles.
- [ ] Materials of the cutting brush appear on cut faces when useGroups is true.

## Checked

2026-10-28. Confirmed in the three-bvh-csg README: `Brush`, `Evaluator`, `SUBTRACTION`/`DIFFERENCE`/`HOLLOW_SUBTRACTION`, `attributes` default `[ 'position', 'uv', 'normal' ]`, `useGroups` (default true; material array and groups on the result), `evaluate(brushA, brushB, operation, target)`, two-manifold requirement, geometry not to be modified after creating a brush, `updateMatrixWorld()` in the usage example.
Removed (not in the fetched pages): `disposeCacheData`, `mergeVertices`, `toCreasedNormals`, timing and speed-up figures, coplanar-face claim, three-csg-ts comparison, Manifold library advice.

Method: documentation only; no commands were run.
