---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-multiple-scenes-viewports-scissor
name: threejs-multiple-scenes-viewports-scissor
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-fundamentals, scissor-test, multiple-viewports, split-screen, multiple-scenes, minimap]
level: practitioner
status: docs-checked
description: "Render many three.js scenes or cameras in one canvas with setViewport and setScissor: split screens, minimaps, product grids and picture-in-picture views."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/multiple-scenes.html", "https://github.com/mrdoob/three.js/blob/r186/examples/webgl_multiple_elements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple scenes, viewports and scissor in three.js

The three.js manual notes that browsers limit live WebGL contexts (typically around 8; creating the 9th loses the
oldest) and that WebGL resources cannot be shared between contexts. Use one full-page canvas and draw each view
into its own rectangle.

## 1. One canvas, many element-aligned views
```js
renderer.setScissorTest(true);
function render() {
  renderer.setClearColor(0xffffff); renderer.setScissorTest(false); renderer.clear();
  renderer.setScissorTest(true);
  for (const { elem, scene, camera } of views) {
    const r = elem.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
    const w = r.right - r.left, h = r.bottom - r.top;
    const left = r.left, bottom = renderer.domElement.clientHeight - r.bottom; // GL origin bottom-left
    renderer.setViewport(left, bottom, w, h);
    renderer.setScissor(left, bottom, w, h);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }
}
```
Canvas (as in the manual): `position: fixed; left: 0; top: 0; width: 100%; height: 100%; z-index: -1` behind the
HTML. If fixed positioning lags while scrolling, the manual's alternative is `position: absolute` with
`transform: translateY(${window.scrollY}px)` set each frame.

## 2. Minimap / picture-in-picture
```js
renderer.setViewport(0, 0, W, H); renderer.setScissor(0, 0, W, H); renderer.render(scene, mainCam);
renderer.clearDepth();                                     // inset draws on top
renderer.setViewport(W - 210, H - 210, 200, 200); renderer.setScissor(W - 210, H - 210, 200, 200);
renderer.render(scene, topDownOrthoCam);
```
Set `renderer.autoClear = false` when stacking renders and clear manually.

## 3. Alternatives
- Render each view to a `WebGLRenderTarget` and draw it as a texture.
- Copy the shared canvas into per-element 2D canvases with `drawImage` (the manual's alternative approach).

## Gotchas
- Viewport/scissor values are CSS pixels; three multiplies by pixel ratio internally.
- Raycasting in a sub-view: compute NDC relative to that element's rect, not the canvas.

## Verify
- [ ] 50+ item views render from one context with no "too many WebGL contexts" warning.
- [ ] Views stay aligned while scrolling.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), the manual page `multiple-scenes` and WebGLRenderer.js.
Confirmed: the manual's context limit (around 8) and CSS (`position: fixed`, `z-index: -1`, or `position: absolute` with
`translateY(scrollY)`); the bottom-left origin conversion (`clientHeight - bottom`) and the off-screen test with
`getBoundingClientRect`; viewport and scissor values are multiplied by the pixel ratio in `setViewport`/`setScissor`
handling; `clearDepth`, `autoClear`, `setScissorTest` exist.

Method: documentation only; no commands were run.
