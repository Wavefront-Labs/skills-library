---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-layers-visibility-and-frustum-culling
name: threejs-layers-visibility-and-frustum-culling
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, three-layers, frustumculled, visibility, bounding-sphere]
level: practitioner
status: verified
description: "Control what each three.js camera renders and raycasts with Layers, visible flags and frustumCulled, and fix objects vanishing from stale bounding spheres."
sources: ["https://threejs.org/docs/pages/Layers.html", "https://threejs.org/docs/pages/Object3D.html", "https://threejs.org/docs/pages/Raycaster.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js layers, visibility and frustum culling

## 1. visible
`obj.visible = false` skips the object **and its children** for rendering and shadows (a hidden parent gave 0 draw calls and a black pixel). Raycasters IGNORE `visible` (a hidden mesh is still hit), so filter hits yourself. It still costs matrix updates. Cheapest render toggle for whole groups.

## 2. Layers (32 bit masks)
An object renders for a camera only if their layer masks intersect (channels 0 to 31; `layers.set(32)` wraps to channel 0).
```js
const BLOOM = 1, DEBUG = 2;
glowMesh.layers.enable(BLOOM);       // on layers 0 and 1
helper.layers.set(DEBUG);            // only on layer 2
camera.layers.enable(DEBUG);         // camera now sees 0 and 2
raycaster.layers.set(0);             // picks ignore helpers (the raycaster has its own layers)
```
- Layers are **not inherited**: set them on every child (`obj.traverse(o => o.layers.set(n))`).
- Lights obey layers too: a DirectionalLight on layer 1 only, with a camera on layer 0, lit nothing (ground pixel 0 instead of 238), and enabling layer 0 on the light restored it. Keep lights on the layers every camera sees.
- Use cases: selective bloom, per-eye content in XR (WebXRManager gives the left eye camera layer 1 and the right eye layer 2 in its masks),
  minimap cameras, editor-only gizmos.

## 3. Frustum culling
Each mesh is tested with its `geometry.boundingSphere` transformed by `matrixWorld`.
- Vertex-shader displacement (a +1000 offset in the vertex shader was culled: 0 draw calls until `frustumCulled = false`), skinning outside bind pose, or instances moved after the bounds were computed
  break the bounds; the mesh pops out near the screen edge. (r186: an InstancedMesh with instances at x=0 and x=1000 got a sphere of centre 500 radius 500.35 from its instance matrices, but after moving the only instance from x=1000 back to the origin it drew nothing until `computeBoundingSphere()`.)
- Fixes, in order: recompute/enlarge bounds (`geometry.boundingSphere.radius *= 2`,
  `instancedMesh.computeBoundingSphere()`, present since r151), or `obj.frustumCulled = false` for a few
  always-visible objects.
- Culling is per object, not per triangle: a single giant terrain mesh is never culled; split
  large meshes into chunks.

## 4. Render order interaction
`renderOrder` sorts within opaque and transparent lists; layers and visibility filter before sorting.

## Gotchas
- `camera.layers.set(1)` disables layer 0: the scene disappears. Use `enable` to add.
- Hidden parents hide children even if the child's layer matches.
- Shadow casting is tested against the MAIN camera's layers, not the light's: a caster on layer 1 with the camera on layer 0 cast no shadow, and enabling layer 1 on the camera brought it back (source: `WebGLShadowMap.renderObject` calls `object.layers.test(camera.layers)`).

## Verify
- [ ] `renderer.info.render.calls` drops when looking away from content.
- [ ] Displaced or skinned meshes stay visible at screen edges.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): parent `visible=false` gave 0 draw calls; mesh on layer 1 with camera on layer 0 rendered black and became white after `camera.layers.enable(1)`; `camera.layers.set(1)` hid a layer-0 mesh; DirectionalLight on layer 1 with camera layer 0 lit nothing and `layers.enable(0)` restored it; a caster on layer 1 cast no shadow for a layer-0 camera and did for a camera with layer 1 enabled (pixel rows 238 vs 0); a mesh looked away from gave `info.render.calls` 1 then 0; `new Layers().set(31)` gave mask 2147483648 and `set(32)` wrapped to 1; a hidden mesh is still hit by Raycaster (raycaster batch); `InstancedMesh.computeBoundingSphere` exists at r151, not r150. InstancedMesh bounds as quoted above; WebXRManager.js sets `cameraL.layers.mask = ... & ~0b100` and `cameraR ... & ~0b010`; `projectObject` tests layers before pushing to the render list (source). A ShaderMaterial that displaces vertices by +1000 in x, with the camera at x=1000, drew 0 calls under default frustum culling and 1 call with `frustumCulled = false`.
