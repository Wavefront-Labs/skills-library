---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl-mobile-precision-limits-quirks
name: webgl-mobile-precision-limits-quirks
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-limits, webgl-mobile, mediump, getshaderprecisionformat, driver-quirks]
level: advanced
status: docs-checked
description: "Ship WebGL that works on phones: mediump vs highp precision, querying limits instead of assuming them, and handling context loss."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices", "https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/getShaderPrecisionFormat", "https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/getParameter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL on mobile: precision, limits and quirks

## 1. Precision
- In WebGL 2 (ESSL 3.00) fragment shaders `highp float` is IEEE float32, and `mediump float` is
  float16 (relative precision 2^-10, range about +-2^14). Mobile GPUs really use that reduced precision, so
  corruption shows on phones but not on a typical desktop.
- In WebGL 1 `highp float` in fragment shaders is optional: use
  `#ifdef GL_FRAGMENT_PRECISION_HIGH` to select `highp`, else `mediump`.
- A 32-bit int passed between shaders needs `highp` (works on desktop, not on Android with mediump).
- On iOS a float texture needs `highp sampler2D`, or samples come back as `lowp`.
- Keep positions, UVs on big textures, depth reconstruction and long-running time values in `highp`.
- Query: `gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.MEDIUM_FLOAT)` returns an object with
  `rangeMin`, `rangeMax` and `precision` (or null on error).
- Do not use `#ifdef GL_ES` in WebGL shaders; it is always true.

## 2. Limits to query, not assume
```js
const L = n => gl.getParameter(gl[n]);
console.table({ tex: L('MAX_TEXTURE_SIZE'), units: L('MAX_TEXTURE_IMAGE_UNITS'),
  vUnits: L('MAX_VERTEX_TEXTURE_IMAGE_UNITS'), vUniforms: L('MAX_VERTEX_UNIFORM_VECTORS'),
  fUniforms: L('MAX_FRAGMENT_UNIFORM_VECTORS'), varyings: L('MAX_VARYING_VECTORS'),
  samples: L('MAX_SAMPLES'), drawBuffers: L('MAX_DRAW_BUFFERS') });
```
Skinning with many bones can exceed uniform vectors: use bone textures (three does automatically).
WebGL cannot query the amount of video memory, so keep VRAM use conservative.

## Gotchas
- Mipmaps cost about 30% extra memory; skip them for 2D textures that are never minified.
- Handle context loss in every long-lived page.

## Verify
- [ ] Test matrix includes one low-end Android phone and one iPhone.

## Checked
2026-10-31. Confirmed against MDN "WebGL best practices" (precision tables, GL_FRAGMENT_PRECISION_HIGH, highp int and
iOS sampler notes, GL_ES, VRAM query, mipmap overhead, CONTEXT_LOST) and MDN getShaderPrecisionFormat (return
fields, constants). Removed unconfirmed claims: typical limit floors, tile-based GPU advice, driver quirks, iOS memory
figures, device pixel ratio and powerPreference advice, specific GPU models.
Method: documentation only; no commands were run.
