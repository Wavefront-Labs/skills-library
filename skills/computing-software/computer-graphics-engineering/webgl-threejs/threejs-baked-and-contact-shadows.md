---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-baked-and-contact-shadows
name: threejs-baked-and-contact-shadows
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-shadows, baked-shadows, contact-shadows, shadow-texture, aomap, lightmap, blob-shadow, product-viewer, uv1]
level: practitioner
status: draft
description: "Use cheap shadows in three.js: baked shadow/AO textures from Blender, lightMap/aoMap with uv1, blob and contact shadows for product viewers."
sources: ["https://threejs.org/manual/#en/shadows", "https://threejs.org/examples/#webgl_shadow_contact", "https://threejs.org/docs/#api/en/materials/MeshStandardMaterial.aoMap", "https://threejs.org/docs/#api/en/materials/MeshStandardMaterial.lightMap"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# three.js baked and contact shadows

**Goal:** grounded-looking objects at a fraction of shadow-map cost — essential on mobile and
for product configurators.

## 1. Blob shadow (cheapest)
A plane with a radial-gradient texture under each object:
```js
const blob = new THREE.Mesh(new THREE.PlaneGeometry(1, 1),
  new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false }));
blob.rotation.x = -Math.PI / 2; blob.position.y = 0.001;     // avoid z-fighting with ground
blob.renderOrder = 1;
```
Scale/opacity by object height above ground. The three.js manual "fake shadows" approach.

## 2. Contact shadows (product viewers)
Render the object from below with an orthographic camera into a render target using a depth
material, blur it (two separable Gaussian passes), and display on a ground plane — see the
`webgl_shadow_contact` example; R3F/drei exposes `<ContactShadows />` and
`<AccumulativeShadows />` (soft, progressive, static scenes). Re-render only when the object
moves.

## 3. Baked shadow and AO textures
Bake in Blender (Cycles → Bake → Shadow/AO/Combined) into a texture:
- Static environment: bake lighting into `lightMap` (multiplies diffuse); dynamic objects use
  a light probe or real-time light only for themselves.
- Ambient occlusion: `aoMap` + `aoMapIntensity`.
- Both read the **second UV set** (`uv1` in r151+, `uv2` before) — export a non-overlapping
  lightmap UV from Blender and ensure glTF carries `TEXCOORD_1`.
```js
material.aoMap = aoTex; material.aoMapIntensity = 1;
aoTex.channel = 1;          // r151+: choose UV set per texture
aoTex.colorSpace = THREE.NoColorSpace;     // data, not colour
lightTex.colorSpace = THREE.SRGBColorSpace; // if baked as colour image
```
A baked shadow can also be a separate transparent plane textured with the baked ground
shadow — the simplest path for a single hero object.

## 4. Choosing
| scene | approach |
|---|---|
| static architecture/viz | bake lightmaps + AO, no real-time shadows |
| product on turntable | contact/accumulative shadows |
| many characters on mobile | blob shadows |
| dynamic sun + moving objects | real shadow maps (tuned) |

## Gotchas
- Lightmap resolution vs file size: use KTX2/Basis compression; check texel density.
- Baked shadows don't move with objects — only for static geometry.
- Overlapping UVs in uv1 = blotchy bakes.

## Verify
- [ ] Objects read as grounded in screenshots without shadow maps enabled.
- [ ] GPU frame time and draw calls lower than the shadow-map version.
- [ ] uv1 present in exported glTF (`gltf-transform inspect`).
