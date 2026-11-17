---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-text-rendering
name: threejs-text-rendering
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, textgeometry, troika-text, sdf-text, msdf, fontloader]
level: practitioner
status: docs-checked
description: "Choose and implement three.js text: extruded TextGeometry, crisp SDF text with troika-three-text, MSDF atlases, canvas textures or HTML overlays."
sources: ["https://github.com/mrdoob/three.js/blob/dev/examples/jsm/geometries/TextGeometry.js", "https://protectwise.github.io/troika/troika-three-text/", "https://github.com/Chlumsky/msdfgen"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text rendering in three.js

## 1. Pick the technique
| Need | Use |
|---|---|
| 3D extruded logo/title | TextGeometry |
| Lots of crisp, dynamic labels in 3D | troika-three-text (SDF) |
| Fixed glyph set, max performance | MSDF atlas + custom shader |
| Rarely-changing label, simple | CanvasTexture on a plane/sprite |
| Accessible, selectable UI | HTML / CSS2DRenderer |

## 2. TextGeometry
```js
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
const font = await new FontLoader().loadAsync('/fonts/helvetiker_bold.typeface.json');
const g = new TextGeometry('Hello', { font, size: 0.5, depth: 0.1, curveSegments: 6,
  bevelEnabled: true, bevelThickness: 0.01, bevelSize: 0.01, bevelSegments: 2 });
g.center();
```
Convert TTF with facetype.js (the TextGeometry source points to it). Bevelled text is heavy geometry: never rebuild it per frame. The extrusion option is `depth`.

## 3. troika-three-text
```js
import { Text } from 'troika-three-text';
const t = new Text();
t.text = 'Score: 0'; t.font = '/fonts/Inter.woff'; t.fontSize = 0.2;
t.anchorX = 'center'; t.anchorY = 'middle'; t.color = 0xffffff; t.maxWidth = 2;
t.sync();           // async glyph SDF generation in a worker
scene.add(t);
// update: t.text = 'Score: 10'; t.sync();   dispose: t.dispose()
```
The troika docs cover WOFF fonts, ligatures, right-to-left and bidi text, and outlines (`outlineWidth`).

## 4. Canvas texture
Draw text on a 2D canvas at 2x resolution, `new CanvasTexture(canvas)`, `colorSpace = SRGBColorSpace`,
`texture.needsUpdate = true` after redraw. Blurry when zoomed; fine for billboards.

## Gotchas
- Fonts must include the glyphs you show; troika can load fonts by unicode range (see its docs).
- Text facing the camera: `Sprite`, or copy `camera.quaternion` each frame.

## Verify
- [ ] Text stays crisp at the closest zoom and does not shimmer far away.
- [ ] Updating text does not grow GPU memory (call `dispose()` on removed troika text).

## Checked

2026-10-28. Confirmed: `TextGeometry` options `depth`, `curveSegments`, `bevel*` and the facetype.js pointer (TextGeometry.js); troika `anchorX`, `anchorY`, `maxWidth`, `outlineWidth`, `sync()`, `dispose()`, worker-based glyph generation, WOFF, ligatures, bidi/RTL, unicode ranges (troika docs).
Removed (not in the fetched pages): r163 rename note, triangle-count claim, "any TTF" and kerning claims, lit-material and drei `<Text>` claims, transparent-sorting and polygonOffset gotcha, `renderer.info.memory.geometries`, dead docs and manual links.

Method: documentation only; no commands were run.
