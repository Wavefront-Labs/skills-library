---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-uv-offset-repeat-texture-transforms
name: threejs-uv-offset-repeat-texture-transforms
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, texture-repeat, uv-offset, texture-transform, sprite-sheet, khr-texture-transform]
level: practitioner
status: verified
description: "Tile, scroll, rotate and atlas textures in three.js via offset, repeat, rotation and center, per-map channels, sprite-sheet animation and KHR_texture_transform."
sources: ["https://threejs.org/docs/pages/Texture.html", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_texture_transform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js UV offset, repeat and texture transforms

## 1. The transform
```js
tex.wrapS = tex.wrapT = THREE.RepeatWrapping;   // needed for repeat > 1 or scrolling (set before first use, or set tex.needsUpdate = true after changing it)
tex.repeat.set(4, 2);
tex.offset.set(0.25, 0);
tex.center.set(0.5, 0.5);                       // pivot for rotation
tex.rotation = Math.PI / 4;
// three builds tex.matrix automatically (matrixAutoUpdate true)
```
Each texture has its own transform (since r151: `normalMapUv` and the other per-map UV varyings exist at r151 and not at r150), so `normalMap` and `roughnessMap` must be given the same repeat as `map` explicitly.

## 2. Animated effects
- Scrolling water/conveyor: `tex.offset.x = (t * speed) % 1` each frame (no needsUpdate needed).
- Sprite sheet (cols x rows):
```js
tex.repeat.set(1 / cols, 1 / rows);
const f = frame % (cols * rows);
tex.offset.set((f % cols) / cols, 1 - (Math.floor(f / cols) + 1) / rows);
```
  Use NearestFilter or padding between frames to avoid bleeding; per-instance frames need a
  shader attribute instead (one texture transform per material).

## 3. Second UV set
`tex.channel = 1` samples `uv1` (glTF TEXCOORD_1), typical for aoMap/lightMap baked in a separate
unwrap; the default `channel` is 0. (Releases before r151 named the second set `uv2` and aoMap always used it.)

## 4. glTF
GLTFLoader applies `KHR_texture_transform` to texture offset/repeat/rotation; GLTFExporter writes it.
glTF defines the UV transform as T*R*S while three.js composes T*S*R, so GLTFLoader writes the matrix itself and sets `matrixAutoUpdate = false` when a rotation is present (GLTFLoader source); set `rotation` by hand on such a texture and it will not follow. Let the loader convert.

## Gotchas
- Repeat with ClampToEdgeWrapping smears the edge pixels.
- Sharing one texture between materials with different repeat: clone it (`tex.clone()`), image is shared.
- World-scale tiling across different-sized meshes: scale UVs in geometry or use triplanar in a shader rather than per-mesh repeat.

## Verify
- [ ] All maps on a material line up after changing repeat.
- [ ] Sprite-sheet frames show no neighbour bleeding at mip levels.

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): sprite-sheet formulas for a 4x2 sheet mapped frames 0, 1, 4, 7 to the UV rectangles (0,0.5)-(0.25,1), (0.25,0.5)-(0.5,1), (0,0)-(0.25,0.5), (0.75,0)-(1,0.5), i.e. top-left first, row-major; `Texture.clone()` shares `image`; `matrixAutoUpdate` defaults true and `channel` 0; rotating 90 degrees about `center` (0.5,0.5) leaves (0.5,0.5) fixed; GLTFLoader's KHR_texture_transform source comment and matrix override read; GLTFExporter mentions KHR_texture_transform; per-map UV varyings (`normalMapUv`) exist from tag r151; the Khronos KHR_texture_transform link returns 200. In headless Edge on a 2x1 red|blue DataTexture: `repeat.set(2,1)` with ClampToEdge smeared the blue edge pixel across the right half; changing `wrapS` to RepeatWrapping after a render had no effect until `needsUpdate = true`, then the texture tiled; moving `offset.x` through 0, 0.5, 1 swapped halves and returned without any `needsUpdate`.
