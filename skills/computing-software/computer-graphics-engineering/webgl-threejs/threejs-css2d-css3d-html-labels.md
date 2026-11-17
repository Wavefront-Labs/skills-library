---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-css2d-css3d-html-labels
name: threejs-css2d-css3d-html-labels
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-picking, css2drenderer, css3drenderer, html-labels, annotations]
level: practitioner
status: docs-checked
description: "Attach HTML labels and panels to three.js objects with CSS2DRenderer and CSS3DRenderer, including occlusion, pointer events, layering and performance limits."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/renderers/CSS2DRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/renderers/CSS3DRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/align-html-elements-to-3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTML labels with CSS2DRenderer and CSS3DRenderer

## 1. CSS2D labels (screen-aligned)
```js
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(innerWidth, innerHeight);
Object.assign(labelRenderer.domElement.style, { position: 'absolute', top: '0', pointerEvents: 'none' });
document.body.appendChild(labelRenderer.domElement);
const div = Object.assign(document.createElement('div'), { className: 'label', textContent: 'Pump A' });
div.style.pointerEvents = 'auto';               // clickable label, rest passes through
const label = new CSS2DObject(div); label.position.set(0, 1.2, 0); mesh.add(label);
// loop: renderer.render(scene, camera); labelRenderer.render(scene, camera);
```
Resize both renderers together. `label.center` (a Vector2, default 0.5, 0.5) sets the anchor point; `label.center.set(0.5, 1)`
places the bottom-centre of the div on the projected position. CSS2DRenderer only supports 100% browser and display zoom.

## 2. CSS3D (perspective-transformed DOM)
CSS3DRenderer applies CSS `matrix3d` transforms so HTML elements (including iframes) sit in the 3D scene. See the
three.js CSS3D examples for how to combine it with a WebGL canvas.

## 3. Occlusion
CSS labels draw on top of everything. Hide occluded labels with a throttled raycast from camera
to label world position, or fade by distance (the manual has `align-html-to-3d-w-hiding` and `-w-sorting` examples).

## 4. Performance
Every label is a DOM node whose style transform is rewritten on each render. For very large label counts use WebGL
text or sprites, or see the manual's `too-many-labels` example.

## Gotchas
- In r186 CSS2DRenderer sets `display: none` only when a label's clip-space depth is outside the near/far range or its
  layers do not match the camera; it does not hide labels that are off-screen sideways.
- The label layer sits above the canvas; keep `pointer-events: none` on it (as above) so OrbitControls on the canvas still receives events.
- Accessibility: labels are real text, so screen readers and translation tools work; keep them meaningful.

## Verify
- [ ] Labels track objects without lag during camera moves and resizes.
- [ ] Orbiting still works with labels on top; labels are clickable.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), CSS2DRenderer.js and CSS3DRenderer.js source.
Confirmed: `CSS2DObject.center` is a Vector2 defaulting to (0.5, 0.5) and drives the transform origin; the visibility
test is depth in [-1, 1] plus layers; 100% zoom limitation; CSS3DRenderer builds `matrix3d` transforms.

Method: documentation only; no commands were run.
