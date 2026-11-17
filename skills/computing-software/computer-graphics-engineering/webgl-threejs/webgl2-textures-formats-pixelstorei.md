---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-textures-formats-pixelstorei
name: webgl2-textures-formats-pixelstorei
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-textures, texstorage2d, pixelstorei, internal-formats, texture-arrays]
level: practitioner
status: verified
description: "Upload WebGL2 textures correctly: immutable texStorage2D, sized internal formats and matching format/type, pixelStorei flags, mipmaps, arrays and 3D textures."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/texStorage2D", "https://registry.khronos.org/webgl/specs/latest/2.0/#TEXTURE_TYPES_FORMATS_FROM_DOM_ELEMENTS_TABLE", "https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/pixelStorei", "https://webgl2fundamentals.org/webgl/lessons/webgl-data-textures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGL2 textures, formats and pixelStorei

## 1. Immutable storage + upload
```js
const tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, tex);
const levels = Math.floor(Math.log2(Math.max(w, h))) + 1;
gl.texStorage2D(gl.TEXTURE_2D, levels, gl.SRGB8_ALPHA8, w, h);    // allocate once
gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);          // IGNORED when the source is an ImageBitmap (see section 3)
gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, imageBitmap);
gl.generateMipmap(gl.TEXTURE_2D);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
```
`texStorage2D` storage is immutable: a second `texStorage2D` on the same texture raised INVALID_OPERATION, as did asking for 10 levels on a 300x200 texture (the formula above gives 9). Size and format can no longer change.

## 2. Format/type triples (common)
| internalFormat | format | type | notes |
|---|---|---|---|
| RGBA8 / SRGB8_ALPHA8 | RGBA | UNSIGNED_BYTE | colour (sRGB decodes on sample) |
| R8 | RED | UNSIGNED_BYTE | masks; set UNPACK_ALIGNMENT 1 |
| RG8 | RG | UNSIGNED_BYTE | 2-channel data |
| RGBA16F | RGBA | HALF_FLOAT or FLOAT | HDR, filterable |
| RGBA32F | RGBA | FLOAT | LINEAR sampling reads 0 (black) until `gl.getExtension('OES_texture_float_linear')` has been called, then works |
| R32UI | RED_INTEGER | UNSIGNED_INT | ids; NEAREST only, usampler2D |
| DEPTH_COMPONENT24 | DEPTH_COMPONENT | UNSIGNED_INT | depth textures |
A mismatched triple gives INVALID_OPERATION (checked: RGBA8 with `RED`, and R32UI with `RED` instead of `RED_INTEGER`); every row of the table uploaded with no error.

## 3. pixelStorei
- `UNPACK_ALIGNMENT` default 4 (checked): rows are padded to 4 bytes, so tightly packed R8/RGB8 data whose width is not a multiple of 4 either raises INVALID_OPERATION (a 3x2 R8 array of exactly 6 bytes) or, with a larger array, skews diagonally. Set 1 (the same upload then read back the right pixel).
- `UNPACK_FLIP_Y_WEBGL` and `UNPACK_PREMULTIPLY_ALPHA_WEBGL` apply to DOM sources such as a canvas (flip put the bottom row first; premultiply turned red 255 at alpha 0.5 into 128) but are IGNORED for an ImageBitmap (the WebGL spec says flip applies 'except for ImageBitmap arguments'; both flags gave identical results). Use decode-time options instead: `createImageBitmap(src, { imageOrientation: 'flipY', premultiplyAlpha: 'none' })` flipped the rows and kept red at 255.
- `UNPACK_ROW_LENGTH`/`UNPACK_SKIP_ROWS`/`SKIP_PIXELS` upload a sub-rectangle of a larger buffer.

## 4. Arrays and 3D
`texStorage3D(gl.TEXTURE_2D_ARRAY, levels, gl.RGBA8, w, h, layers)` + `texSubImage3D` per layer;
`sampler2DArray` with `texture(s, vec3(uv, layer))`. Great for atlas-free terrain splats and sprite sets.

## Gotchas
- Integer textures with LINEAR filter are incomplete (R32UI sampled 0 with LINEAR and 200 with NEAREST).
- RGBA32F with a mipmapped LINEAR filter sampled black without the filterable extension, like plain LINEAR.
- `createImageBitmap` decodes asynchronously (it returns a promise), so decode before upload.

## Verify
- [ ] No WebGL errors in console (`gl.getError()` in a debug build after uploads).
- [ ] Odd-width single-channel data displays without skew.

## Checked
- headless Edge WebGL2 on ANGLE/SwiftShader (the KHR_parallel_shader_compile and HLSL-translation checks used the same Edge on ANGLE/D3D11, since SwiftShader does not expose that extension): every table row uploaded via `texStorage2D` + `texSubImage2D` with error 0 and the two mismatches gave 1282; levels for 300x200 = 9, double storage and 10 levels gave 1282; R8 3x2 with alignment 4 gave 1282 and with alignment 1 read 40 (the first pixel of row 2); canvas vs ImageBitmap flip and premultiply readbacks as quoted; RGBA32F LINEAR black before `getExtension('OES_texture_float_linear')` and red after, mipmapped LINEAR black, RGBA16F LINEAR red, R32UI LINEAR 0 and NEAREST 200; `texStorage3D` plus `texSubImage3D` on a 2D array ran with error 0; Khronos WebGL 1.0 spec text about flip and ImageBitmap fetched; MDN and webgl2fundamentals links return 200. Also run: an SRGB8_ALPHA8 texel of 128 sampled to 55 (RGBA8 stayed 128; the sRGB transfer gives 55), `UNPACK_ROW_LENGTH` 4 with SKIP_PIXELS 1 and SKIP_ROWS 1 uploaded the sub-rectangle 50,60,90,100 from a 4x4 array, a 3-layer `sampler2DArray` returned red, green, blue for layers 0 to 2, and a 2x2x2 `texStorage3D` + `texSubImage3D` volume uploaded with error 0.
