---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-alpha-maps-alphatest-alphahash
name: threejs-alpha-maps-alphatest-alphahash
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, alphatest, alphahash, alphamap, alpha-to-coverage, cutout]
level: practitioner
status: docs-checked
description: "Render cutout and fading surfaces in three.js without sorting bugs: alphaMap, alphaTest, alphaHash dithering, alphaToCoverage with MSAA, and shadow handling."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/materials/Material.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/MeshStandardMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLShadowMap.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js alpha maps, alphaTest and alphaHash

## 1. alphaMap vs map alpha
- `map` with an alpha channel (PNG/WebP) uses `map.a`.
- `alphaMap` is a greyscale texture read from the **green** channel; it multiplies opacity. Linear colour space.

## 2. alphaTest (cutout)
```js
mat.alphaTest = 0.5;           // fragments with alpha < 0.5 discarded
mat.transparent = false;       // stays in the opaque pass: no sorting, writes depth
mat.side = THREE.DoubleSide;   // leaves, fences
```
Edges can alias. `alphaToCoverage: true` smooths alphaTest-clipped edges, but only works when the
renderer was created with `antialias: true` (MSAA).

## 3. alphaHash (stochastic transparency)
```js
mat.alphaHash = true;  mat.opacity = 0.4;  mat.transparent = false;
```
The material is not rendered where its opacity is below a random threshold, which approximates alpha
blending without sorting problems. The randomisation adds visible grain; TAA can reduce it.

## 4. Shadows
Shadow passes use a depth material. In r186 it copies `map`, `alphaMap` and `alphaTest` from the
casting material (a cutout shadow needs `alphaTest > 0` with a `map` or `alphaMap`), approximates
`alphaToCoverage` with a fixed alphaTest of 0.5, and does not copy `alphaHash`. For custom shaders or
hashed materials provide `customDepthMaterial` (and `customDistanceMaterial` for point lights) with the same discard.

## Gotchas
- A material using `alphaHash` casts a solid shadow with the built-in depth material; give it a custom depth material.
- Changing a material setting that alters the generated shader needs `material.needsUpdate = true`.

## Verify
- [ ] Foliage casts leaf-shaped shadows, not quads.
- [ ] No sorting flicker when cards intersect.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0, released 2026-09-24), source of the files listed in `sources`.
Confirmed: `alphaHash` and `alphaToCoverage` descriptions and the MSAA requirement (Material.js); `alphaMap` reads the
green channel and holds non-colour data (MeshStandardMaterial.js); which properties the shadow depth material copies and
that `alphaHash` is not among them (WebGLShadowMap.js).

Method: documentation only; no commands were run.
