---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-custom-buffergeometry
name: threejs-custom-buffergeometry
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, buffergeometry, three-geometry, bufferattribute, custom-geometry, computevertexnormals, setindex, dynamic-geometry, setdrawrange, bounding-sphere, needsupdate, drawrange]
level: practitioner
status: verified
description: "Build and update three.js BufferGeometry by hand: position/normal/uv attributes, indices, groups, dynamic updates with needsUpdate and drawRange."
sources: ["https://threejs.org/manual/#en/custom-buffergeometry", "https://threejs.org/docs/pages/BufferGeometry.html", "https://threejs.org/docs/pages/BufferAttribute.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# three.js custom BufferGeometry

**Goal:** procedural meshes (terrain, extrusions, plots, point clouds) generated in typed
arrays and updated per frame without reallocating.

## 1. Build
```js
const geo = new THREE.BufferGeometry();
const positions = new Float32Array(vertexCount * 3);
const uvs = new Float32Array(vertexCount * 2);
// ...fill...
geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
geo.setIndex(indices);                         // array or Uint16/Uint32 BufferAttribute
geo.computeVertexNormals();                    // smooth normals from indexed faces
geo.computeBoundingSphere();                   // needed for frustum culling & raycasting
```
- Attribute names map to shader inputs: `position`, `normal`, `uv`, `color` (requires
  `material.vertexColors = true`), `uv1` (second UV set; a texture only reads it when `texture.channel = 1`, the default channel 0 reads `uv`), custom names for ShaderMaterial.
- Index type: three picks Uint16 or Uint32 from the max index when passed a plain array (max index 2 gave Uint16; 65535 already gave Uint32).
- Flat shading without duplicating vertices: `material.flatShading = true`.

## 2. Groups (multi-material)
```js
geo.addGroup(0, 600, 0);   // start (index count), count, materialIndex
geo.addGroup(600, 300, 1);
const mesh = new THREE.Mesh(geo, [matA, matB]);
```
Each group is a separate draw call.

## 3. Dynamic updates
```js
const pos = geo.attributes.position;
pos.setUsage(THREE.DynamicDrawUsage);          // hint before first render
for (let i = 0; i < pos.count; i++) pos.setY(i, height(i, t));
pos.needsUpdate = true;                        // re-upload
pos.addUpdateRange(0, changedCount * 3);       // r159+: upload only the changed span
geo.computeVertexNormals();                    // only if shape changed meaningfully
geo.computeBoundingSphere();
```
Growing data: preallocate the maximum size and use `geo.setDrawRange(0, liveCount)` — never
replace attributes every frame. Measured with WebGLRenderer: 5 replacements of `position` created 5 GL
buffers and deleted none, and `geometry.dispose()` freed only the attribute attached at that moment
(`BufferAttribute.dispose()` is documented as WebGPURenderer-only), so replaced buffers stay leaked.

## 4. Interleaved and quantised attributes
`THREE.InterleavedBuffer` + `InterleavedBufferAttribute` for cache-friendly layouts;
`new THREE.BufferAttribute(new Int16Array(...), 3, true)` for normalised compressed
attributes (with a matching position scale).

## Gotchas
- Mesh disappears (or draws when it should not): stale bounding sphere. A triangle moved from x=500 to the
  origin stayed culled (0 triangles) until `computeBoundingSphere()`, then drew. Recompute after edits or
  set `mesh.frustumCulled = false` for always-visible dynamic meshes.
- Resizing an attribute **in place** after first render throws `Resizing buffer attributes is not
  supported`. Swapping in a new attribute object works but leaks the old GL buffer (see above), so
  create a new geometry and `dispose()` the old one.
- Winding order: counter-clockwise = front face; flipped triangles render black/invisible
  with `side: FrontSide`.

## Verify
- [ ] `renderer.info.memory.geometries` stays constant during dynamic updates (it counts geometries, not buffers: it did NOT change while attributes leaked; count `gl.createBuffer` calls to catch that).
- [ ] Normals helper (`VertexNormalsHelper`, from `three/addons/helpers/VertexNormalsHelper.js`, not the `THREE` namespace) shows outward normals.
- [ ] Raycasting hits the updated shape (bounds recomputed).

## Checked
- three 0.186.1 in Node 24: plain-array index gave Uint16Array for max 2 and Uint32Array for 65535, 65536 and 70000; `addUpdateRange` appears at tag r159 (absent at r158), stored in `attribute.updateRanges`; `setDrawRange`, `addGroup`, `setUsage(DynamicDrawUsage)`, InterleavedBufferAttribute (bounding sphere radius 0.707) and a normalised Int16 attribute (32767 reads 1, -32768 reads -1) behaved as written; a clockwise triangle seen from +Z got normal z -1; `Texture.channel` defaults to 0. Run in headless Edge (WebGL2 via SwiftShader): two groups gave 2 draw calls; 5 dynamic updates left `info.memory.geometries` at 1; in-place resize threw the quoted error; `setDrawRange(0,6)` drew 2 triangles; a GL-buffer counter showed 5 created and 0 deleted for 5 attribute replacements, and 1 deleted by `geometry.dispose()`; the `BufferAttribute.dispose` doc comment in source reads WebGPURenderer only; a stale bounding sphere culled a moved-in triangle (0 tris) until recomputed and `frustumCulled=false` drew it; VertexNormalsHelper lives in examples/jsm/helpers.
