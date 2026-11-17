---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-progressive-and-lazy-loading
name: threejs-progressive-and-lazy-loading
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-loading, progressive-loading, lazy-loading, streaming, 3d-tiles, code-splitting]
level: advanced
status: docs-checked
description: "Get three.js scenes interactive fast: lazy-load by visibility, progressive LOD and texture swaps, streaming 3D Tiles, priority queues and avoiding upload hitches."
sources: ["https://threejs.org/docs/pages/LoadingManager.html", "https://threejs.org/docs/pages/WebGLRenderer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Progressive and lazy loading in three.js

## 1. Order of work
1. Ship a tiny first view: a low-poly proxy or the hero model with small textures.
2. Render and accept input.
3. Load the rest by priority (on-screen and near first), idle-time otherwise.

## 2. Lazy by visibility/proximity
```js
const pending = new Map(); // placeholder -> url
function update() {
  for (const [ph, url] of pending) {
    if (camera.position.distanceTo(ph.position) < 30 && !ph.userData.loading) {
      ph.userData.loading = true;
      loader.loadAsync(url).then(g => { ph.add(g.scene); pending.delete(ph); });
    }
  }
}
```
Limit concurrent loads with a queue; cancel with AbortController when items leave range.

## 3. Progressive detail
- Swap textures: low-res first, then `material.map = hiRes; material.needsUpdate` only if map was null before.
- Mesh LODs as separate files, loaded in order of importance.

## 4. Avoid hitches when content arrives
- Upload ahead of first draw: `renderer.initTexture(tex)`; compile with `renderer.compileAsync(obj, camera)` before adding to the scene.
- Spread additions over frames (one model per frame).

## 5. JS too
Dynamic `import()` addons (loaders, post-processing) only when needed; keep the initial bundle small.

## Gotchas
- LoadingManager `onProgress` counts items, not bytes; for real progress bars, fetch with a reader and sum Content-Length.
- Keep disposed-on-exit logic for streamed content or GPU memory grows without bound.

## Verify
- [ ] First interactive frame appears quickly under network throttling.
- [ ] No visible hitch while streaming content arrives.

## Checked
2026-10-31. Confirmed against the three.js docs: `LoadingManager` `onProgress` fires per single item loaded (items, not bytes); `WebGLRenderer.initTexture` and `compileAsync(scene, camera)` exist. Removed: size, concurrency and timing figures, the gltf-progressive and 3d-tiles-renderer claims, and the worker-decoder claim (not read this batch).
Method: documentation only; no commands were run.
