---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl-extensions-and-capability-checks
name: webgl-extensions-and-capability-checks
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, webgl2-raw, webgl-extensions, capability-detection, float-render-targets, compressed-textures]
level: practitioner
status: verified
description: "Detect WebGL2 capabilities and extensions (float render targets, texture compression, anisotropy, timer queries) and choose fallbacks safely."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Using_Extensions", "https://registry.khronos.org/webgl/extensions/", "https://web3dsurvey.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL extensions and capability checks

## 1. Query
```js
const gl = canvas.getContext('webgl2', { antialias: false, powerPreference: 'high-performance' });
if (!gl) return fallback2D();
const caps = {
  floatRT: !!gl.getExtension('EXT_color_buffer_float'),       // render to RGBA16F/32F
  floatLinear: !!gl.getExtension('OES_texture_float_linear'), // filter 32F textures
  aniso: gl.getExtension('EXT_texture_filter_anisotropic'),   // object: read aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT
  s3tc: !!gl.getExtension('WEBGL_compressed_texture_s3tc'),
  etc: !!gl.getExtension('WEBGL_compressed_texture_etc'),
  astc: !!gl.getExtension('WEBGL_compressed_texture_astc'),
  bptc: !!gl.getExtension('EXT_texture_compression_bptc'),
  timer: gl.getExtension('EXT_disjoint_timer_query_webgl2'),
  maxTex: gl.getParameter(gl.MAX_TEXTURE_SIZE),
  maxSamples: gl.getParameter(gl.MAX_SAMPLES),
};
```
`getExtension` both checks and enables; an extension's enums/functions only work after it (RGBA16F was not renderable, status 0x8cd6, until `EXT_color_buffer_float` was requested; repeated calls returned the same object).

## 2. Common decisions
- HDR rendering: needs `EXT_color_buffer_float` (or half-float via `EXT_color_buffer_half_float`);
  fall back to RGBA8 with tone mapping in the scene shader.
- Texture formats: ship KTX2/Basis and transcode to whichever of ASTC/BC7/ETC2/S3TC exists.
- Anisotropy: `const max = gl.getParameter(aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT); gl.texParameterf(gl.TEXTURE_2D, aniso.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(8, max))` (max read 16; the value 8 read back).

## 3. GPU identity
`gl.getParameter(gl.RENDERER)` returned the masked string 'WebKit WebGL' in this Edge; the real GPU string only came through `WEBGL_debug_renderer_info` (`UNMASKED_RENDERER_WEBGL`, e.g. 'ANGLE (AMD, AMD Radeon RX 6900 XT ... Direct3D11 ...)'). MDN notes Firefox disables that extension when `privacy.resistFingerprinting` is true. Treat either string as a hint only, never for feature gating.

## Gotchas
- Feature-test `EXT_disjoint_timer_query_webgl2` (exposed in this headless Edge; browsers may hide it).
- Compression families differ by backend: on ANGLE/D3D11 (desktop AMD GPU) S3TC and BPTC were exposed and ETC and ASTC were not; on ANGLE/SwiftShader all four were. Always test per device.
- Read `MAX_TEXTURE_SIZE` instead of assuming (8192 on SwiftShader, 16384 on D3D11).
- Use web3dsurvey.com support percentages before relying on an extension.

## Verify
- [ ] App runs with each optional extension disabled (simulate by forcing caps false).

## Checked
- headless Edge WebGL2 on ANGLE/SwiftShader and, where noted, ANGLE/D3D11 (AMD RX 6900 XT): the skill's `caps` object and context options ran: `getContextAttributes` returned antialias false and powerPreference high-performance; extension results on SwiftShader: float and half-float colour buffers, float linear, anisotropy, s3tc, etc, astc, bptc and the timer query all true, MAX_TEXTURE_SIZE 8192, MAX_SAMPLES 4; on D3D11: etc and astc false, the rest true, MAX_TEXTURE_SIZE 16384, MAX_SAMPLES 8; anisotropy max 16 and `texParameterf` with 8 read back 8; `getSupportedExtensions` counted 30 and 32; MDN's WEBGL_debug_renderer_info page mentions resistFingerprinting; MDN Using_Extensions, Khronos extension registry, web3dsurvey.com return 200. Removed unsupported claims (Mobile Safari lacks S3TC, 4096 common on old mobile, deprecated in Firefox).
