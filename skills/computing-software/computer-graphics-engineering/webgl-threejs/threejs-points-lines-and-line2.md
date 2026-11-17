---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-points-lines-and-line2
name: threejs-points-lines-and-line2
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-geometry, three-points, line2, fat-lines, point-cloud, linesegments]
level: practitioner
status: verified
description: "Draw point clouds and lines in three.js: Points with sized sprites, Line/LineSegments limits, and wide anti-aliased lines with Line2/LineMaterial."
sources: ["https://threejs.org/docs/pages/Points.html", "https://threejs.org/docs/pages/LineBasicMaterial.html", "https://threejs.org/examples/webgl_lines_fat.html", "https://threejs.org/docs/pages/Line2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js points, lines and Line2

## 1. Points
```js
const geo = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(pos, 3));
geo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
const mat = new THREE.PointsMaterial({ size: 0.05, sizeAttenuation: true, vertexColors: true,
  map: discTex, alphaTest: 0.5, transparent: false });
scene.add(new THREE.Points(geo, mat));
```
- `size` is pixels without attenuation (size 10 drew a 10x10 = 100 px square), and with `sizeAttenuation: true` it scales by distance on a PERSPECTIVE camera only (size 0.5 at distance 5 in a 64 px viewport drew 4x4 px; an orthographic camera drew 1 px, i.e. no attenuation). The result is capped by `gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE)` (read [1, 1023] in this headless Edge build; query it on target devices).
- Round points: a disc texture with alphaTest, or in a ShaderMaterial `if (length(gl_PointCoord - 0.5) > 0.5) discard;`.
- Millions of points: per-point size via a custom attribute in ShaderMaterial; raycast with
  `raycaster.params.Points.threshold` or a BVH, since the default is O(n).

## 2. Line, LineSegments, LineLoop
`LineBasicMaterial({ linewidth })` is ignored on almost every platform: a linewidth-10 `Line` drew 1 px and `ALIASED_LINE_WIDTH_RANGE` read [1, 1] here (ANGLE). `LineDashedMaterial` needs `line.computeLineDistances()`. LineSegments takes pairs of vertices.

## 3. Wide lines: Line2
```js
import { Line2 } from 'three/addons/lines/Line2.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { LineGeometry } from 'three/addons/lines/LineGeometry.js';
const g = new LineGeometry().setPositions(flatXYZ).setColors(flatRGB);
const m = new LineMaterial({ linewidth: 4, vertexColors: true, worldUnits: false, dashed: false });
// m.resolution is filled from the renderer viewport by LineSegments2.onBeforeRender (r186 source); Line2 at linewidth 10 drew 10 px without setting it
const line = new Line2(g, m); line.computeLineDistances(); scene.add(line);
```
Line2 renders instanced screen-space quads; `LineSegments2` + `LineSegmentsGeometry` for pairs;
`Wireframe` for wide wireframes. Picking works through `raycaster.params.Line2.threshold` (read in LineSegments2.js, present since at least r140).

## 4. Alternatives
- Tubes (TubeGeometry) for 3D-looking lines that light and shade.
- Ribbon meshes for trails.

## Gotchas
- Many separate Line objects = many draw calls; combine into one LineSegments (500 `Line` objects drew in 500 calls, one `LineSegments` with the same 500 segments in 1).
- Points with `transparent: true` sort per object only; use alphaTest or additive blending with depthWrite false.

## Verify
- [ ] Line width identical on Chrome/Windows (ANGLE) and macOS.
- [ ] Point size consistent across devices (check the GL limit).

## Checked
- three 0.186.1 in Node 24 and headless Edge WebGL2 (SwiftShader): a linewidth-10 LineBasicMaterial line lit 1 pixel in a column and a Line2 with linewidth 10 lit 10, with and without `material.resolution.set`; Points size 10 without attenuation lit 100 pixels, an orthographic camera with `sizeAttenuation: true` and size 0.5 lit 1, a perspective camera at distance 5 lit 16 (4x4, expected 3.2 px); ALIASED_POINT_SIZE_RANGE [1,1023] and ALIASED_LINE_WIDTH_RANGE [1,1]; `LineMaterial.resolution` is set in `LineSegments2.onBeforeRender` from `renderer.getViewport`; `Line2.js`, `LineSegments2.js`, `LineGeometry.js`, `LineSegmentsGeometry.js`, `LineMaterial.js` and `Wireframe.js` exist under examples/jsm/lines; `computeLineDistances()` on Line2 ran without error; `params.Line2` read in the source at tags r140 to r151; all five source URLs returned 200.
