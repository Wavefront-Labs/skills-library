---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-framebuffers-mrt-float-targets
name: webgl2-framebuffers-mrt-float-targets
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-framebuffer, ext-color-buffer-float, drawbuffers, blitframebuffer, msaa-renderbuffer]
level: advanced
status: verified
description: "Render to textures in raw WebGL2: framebuffer completeness, drawBuffers MRT, float targets via EXT_color_buffer_float, MSAA renderbuffers and blitFramebuffer resolves."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/drawBuffers", "https://registry.khronos.org/webgl/extensions/EXT_color_buffer_float/", "https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/blitFramebuffer", "https://webgl2fundamentals.org/webgl/lessons/webgl-render-to-texture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL2 framebuffers, MRT and float targets

## 1. FBO with two colour targets and depth
```js
gl.getExtension('EXT_color_buffer_float');          // required to render to RGBA16F/32F
const fbo = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
const attach = (i, fmt) => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
  gl.texStorage2D(gl.TEXTURE_2D, 1, fmt, w, h);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
  gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0 + i, gl.TEXTURE_2D, t, 0); return t; };
const color = attach(0, gl.RGBA16F), normal = attach(1, gl.RGBA8);
const depth = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, depth);
gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT24, w, h);
gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, depth);
gl.drawBuffers([gl.COLOR_ATTACHMENT0, gl.COLOR_ATTACHMENT1]);
const st = gl.checkFramebufferStatus(gl.FRAMEBUFFER);
if (st !== gl.FRAMEBUFFER_COMPLETE) throw new Error('FBO incomplete 0x' + st.toString(16));
```
Fragment shader: `layout(location=0) out vec4 o0; layout(location=1) out vec4 o1;`.
Remember `gl.viewport(0, 0, w, h)` when switching to the FBO and back to the canvas size.

## 2. Float rendering rules
- Without EXT_color_buffer_float, RGBA16F/32F, R16F and R11F_G11F_B10F attachments were incomplete (status 0x8cd6) and became complete (0x8cd5) after `gl.getExtension('EXT_color_buffer_float')`. Devices may only offer `EXT_color_buffer_half_float` (16F): read `gl.getSupportedExtensions()` on the target. Blending into a 32F target needs `EXT_float_blend` (its spec: a draw with blending enabled on a 32-bit float colour buffer is INVALID_OPERATION without it).
- Prefer RGBA16F (half the bytes of RGBA32F) or R11F_G11F_B10F (4 bytes per pixel) for HDR colour.

## 3. MSAA then resolve
```js
gl.renderbufferStorageMultisample(gl.RENDERBUFFER, Math.min(4, gl.getParameter(gl.MAX_SAMPLES)), gl.RGBA8, w, h);
// render into msFbo, then:
gl.bindFramebuffer(gl.READ_FRAMEBUFFER, msFbo); gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, resolveFbo);
gl.blitFramebuffer(0, 0, w, h, 0, 0, w, h, gl.COLOR_BUFFER_BIT, gl.NEAREST);
```
Textures cannot be multisampled in WebGL2 (`texStorage2DMultisample` is undefined; a multisample texture target gave INVALID_ENUM): use multisampled renderbuffers and blit (a 4-sample RGBA8 renderbuffer filled with (1, 0.5, 0) resolved to 255,128,0). Resolve each MRT attachment separately with `readBuffer`/`drawBuffers`.

## 4. Feedback loops
Sampling a texture that is attached to the bound FBO is a feedback loop: the draw raised INVALID_OPERATION (1282). Ping-pong
two FBOs for iterative passes.

## Gotchas
- `gl.invalidateFramebuffer` exists in WebGL2 and tells the driver an attachment's contents are no longer needed; any bandwidth saving on tile-based GPUs was not measured here.
- Clearing integer targets needs `clearBufferuiv`/`clearBufferiv`, not `gl.clear`: `gl.clear` on an RGBA32UI attachment raised INVALID_OPERATION and `clearBufferuiv` then read back 7 in red.

## Verify
- [ ] checkFramebufferStatus complete on desktop and a mid-range Android phone.
- [ ] Each attachment visualised correctly in a debug blit.

## Checked
- headless Edge (ANGLE/SwiftShader) WebGL2 raw-GL runs: RGBA16F, RGBA32F, R16F and R11F_G11F_B10F framebuffers gave 0x8cd6 before the extension and 0x8cd5 after; the skill's two-target FBO (RGBA16F + RGBA8 + DEPTH24 renderbuffer, `drawBuffers`) was complete and a two-output shader wrote (2.5,0,0,1) as float and (0,255,0,255) to the second target; the feedback-loop draw gave 1282; MAX_SAMPLES 4, the multisample renderbuffer was complete and `blitFramebuffer` to a texture FBO resolved (255,128,0,255); texStorage2D on a multisample texture target gave 1280 and `texStorage2DMultisample` is undefined; RGBA32UI target: `gl.clear` gave 1282, `clearBufferuiv` worked; EXT_color_buffer_float and EXT_float_blend Khronos pages fetched. MDN WebGL best practices says EXT_color_buffer_half_float is present on systems that only support rendering to float16 textures. The tiler bandwidth claim was removed.
