---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl-context-loss-and-restoration
name: webgl-context-loss-and-restoration
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgl2-raw, context-loss, webglcontextlost, webglcontextrestored, gpu-reset]
level: advanced
status: verified
description: "Handle WebGL context loss: preventDefault on webglcontextlost, rebuild GPU resources on restore, test with WEBGL_lose_context, and three.js behaviour."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_lose_context", "https://registry.khronos.org/webgl/specs/latest/1.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL context loss and restoration

Context loss can happen when the GPU or driver is reset or when too many contexts are open (Edge/Chromium kept 16 of 40 live contexts and lost the oldest ones first, logging 'Too many active WebGL contexts. Oldest context will be lost.'). Every GL object becomes invalid (an old buffer failed `isBuffer` after restore).

## 1. Handle the events
```js
canvas.addEventListener('webglcontextlost', (e) => {
  e.preventDefault();                 // REQUIRED: without it `restoreContext()` logged 'INVALID_OPERATION: restoreContext: context restoration not allowed' and no restored event came
  cancelAnimationFrame(raf);
}, false);
canvas.addEventListener('webglcontextrestored', () => {
  initGL();                           // recreate programs, buffers, textures, FBOs, state
  raf = requestAnimationFrame(frame);
}, false);
```
Keep CPU copies (or the URLs) of all assets needed to rebuild; do not call GL during loss
(calls are no-ops, `gl.isContextLost()` is true, `getError` returned 0x9242 = `CONTEXT_LOST_WEBGL`).

## 2. Test it
```js
const ext = gl.getExtension('WEBGL_lose_context');
ext.loseContext();                    // fires webglcontextlost
setTimeout(() => ext.restoreContext(), 1000);
```

## 3. three.js
WebGLRenderer listens for these events: after `renderer.forceContextLoss()` and `WEBGL_lose_context.restoreContext()` a textured mesh rendered the same colour again with 1 program, 1 geometry and 1 texture (textures need their `image` data alive, so do not
null out `texture.image`). A WebGLRenderTarget came back EMPTY (green clear read back (0,255,0,255) before and (0,0,0,0) after): regenerate baked content.

## Gotchas
- Results of `gl.getParameter` and extension objects must be re-queried after restore (the spec sets the invalidated flag on extension objects that derive from WebGLObject).
- Creating many renderers/canvases (one per thumbnail) causes the oldest contexts to be lost;
  share one context or use `OffscreenCanvas` transfer.
- Do not free CPU-side image data after upload if you need to survive loss.

## Verify
- [ ] Force loss and restore mid-session: scene renders identically afterwards.

## Checked
- Edge on ANGLE/SwiftShader WebGL2 and three 0.186.1: `loseContext()` fired `webglcontextlost` with preventDefault, `isContextLost()` true, `getError()` 0x9242, then `restoreContext()` fired `webglcontextrestored`; without preventDefault the restore was refused with the quoted warning and no event; 40 canvases gave 16 live and 24 lost with the oldest first; the three.js round trip and render-target result as quoted; the Khronos WebGL 1.0 spec quote about extension objects; MDN WEBGL_lose_context and the spec root return 200. The Khronos wiki page HandlingContextLost timed out from here, so it was dropped from sources. The chrome://gpucrash remark and the list of loss causes (mobile backgrounding, GPU process crashes) were cut back to what was measured. The WebGL 1.0 spec text confirms the preventDefault-to-enable-restored example.
