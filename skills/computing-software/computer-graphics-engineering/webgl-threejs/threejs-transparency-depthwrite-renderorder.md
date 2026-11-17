---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-transparency-depthwrite-renderorder
name: threejs-transparency-depthwrite-renderorder
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, renderorder, depthwrite, transparency, alpha-blending, sorting]
level: practitioner
status: docs-checked
description: "Fix three.js transparency artefacts: how transparent objects are sorted, depthWrite and depthTest, renderOrder, double-sided glass, and blending modes."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLRenderLists.js", "https://github.com/mrdoob/three.js/blob/r186/src/core/Object3D.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/Material.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/transparency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js transparency, depthWrite and renderOrder

## 1. How three renders
Opaque objects are sorted by group order, `renderOrder`, material id, then depth; transparent objects by group order,
`renderOrder`, then back to front by the object's projected centre depth. Sorting is **per object**, never per triangle.

## 2. The knobs
```js
mat.transparent = true;  mat.opacity = 0.5;
mat.depthWrite = false;      // transparent things should usually not occlude each other
mat.depthTest = true;        // still hidden behind opaque geometry
mesh.renderOrder = 2;        // higher draws later, within its list
mat.side = THREE.DoubleSide;
mat.blending = THREE.AdditiveBlending;   // glows/particles: order-independent
```
- `renderOrder` overrides distance sorting; when set on a `Group` all descendants are sorted and rendered together (Object3D docs).
- Override the sorter: `renderer.setTransparentSort(fn)`.

## 3. Recipes
- **Glass box seen from inside/out**: two meshes with the same geometry, one `side: BackSide`
  renderOrder 1, one `FrontSide` renderOrder 2. (three already renders double-sided transparent materials in two
  passes, back faces then front faces, unless `forceSinglePass` is true.)
- **Particles / smoke**: `depthWrite: false` + additive or premultiplied blending.
- **Foliage, fences, hair cards**: avoid blending; use `alphaTest` or `alphaHash`.
- **UI always on top**: `depthTest: false`, high `renderOrder`.
- **Physically refractive glass**: MeshPhysicalMaterial `transmission` (renders a transmission
  pass, sorting handled separately, costs an extra scene render).

## Gotchas
- Intersecting transparent meshes will always flicker one way or the other; split them or use alphaHash.
- `opacity < 1` with `transparent: false` does nothing.
- Transparent objects in the opaque list (forgot `transparent`) write depth and hide what is behind.
- Premultiplied textures: set `mat.premultipliedAlpha = true` and match blending, or edges darken.

## Verify
- [ ] Rotate the camera 360 degrees: no transparent objects popping in front/behind.
- [ ] Inside view of glass shows back faces.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources` and the manual page on transparency.
Confirmed: the opaque and transparent comparison functions in WebGLRenderLists.js (group order, `renderOrder`, material id and
depth for opaque; group order, `renderOrder`, then reverse depth for transparent); `renderOrder` semantics for Groups;
`setTransparentSort` exists; double-sided transparent materials render in two passes unless `forceSinglePass`; the manual's
BackSide-then-FrontSide recipe and `alphaTest` alternative; transmissive objects have their own render list.

Method: documentation only; no commands were run.
