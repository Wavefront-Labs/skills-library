---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl2-readpixels-fences-async-readback
name: webgl2-readpixels-fences-async-readback
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgl2, webgl-api, webgl-readpixels, fencesync, pixel-pack-buffer, async-readback]
level: advanced
status: verified
description: "Read GPU results back in WebGL2 without stalling: readPixels into PIXEL_PACK_BUFFER, fenceSync and clientWaitSync polling, getBufferSubData, and format rules."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/readPixels", "https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext/fenceSync", "https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices#use_non-blocking_async_data_readback"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# readPixels, fences and async readback in WebGL2

Synchronous `gl.readPixels` into a typed array waits for the GPU to finish all queued work (Chromium logged 'GPU stall due to ReadPixels' for it). Use a pixel pack buffer and a fence.

## 1. Async pattern (MDN best practice)
```js
function readPixelsAsync(gl, x, y, w, h, format, type, dest) {
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.PIXEL_PACK_BUFFER, buf);
  gl.bufferData(gl.PIXEL_PACK_BUFFER, dest.byteLength, gl.STREAM_READ);
  gl.readPixels(x, y, w, h, format, type, 0);         // offset into PBO: returns immediately
  gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
  const sync = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
  gl.flush();
  return new Promise((resolve, reject) => (function poll() {
    const r = gl.clientWaitSync(sync, 0, 0);
    if (r === gl.WAIT_FAILED) return reject(new Error('wait failed'));
    if (r === gl.TIMEOUT_EXPIRED) return setTimeout(poll, 1);
    gl.deleteSync(sync);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, buf);
    gl.getBufferSubData(gl.PIXEL_PACK_BUFFER, 0, dest);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null); gl.deleteBuffer(buf);
    resolve(dest);
  })());
}
```
Reuse PBOs in a small ring instead of creating one per read.

## 2. Format rules
Always-supported combinations: `RGBA/UNSIGNED_BYTE` for normalised targets, `RGBA_INTEGER/UNSIGNED_INT`
(or INT) for integer targets, `RGBA/FLOAT` for float targets with EXT_color_buffer_float.
The implementation-chosen extra pair is `gl.getParameter(gl.IMPLEMENTATION_COLOR_READ_FORMAT/TYPE)` (RGBA and UNSIGNED_BYTE on the default framebuffer here). Reading an RGBA32UI target with plain `RGBA/UNSIGNED_BYTE` raised INVALID_OPERATION, while `RGBA_INTEGER/UNSIGNED_INT` returned [5,6,7,8] and an RGBA32F target returned [0.25,0.5,1.5,2] with `RGBA/FLOAT`.
Read from a specific attachment with `gl.readBuffer(gl.COLOR_ATTACHMENTi)`.

## 3. Uses
GPU picking (read 1x1 pixel under cursor, a frame late is fine), screenshots (`canvas.toBlob` called right after rendering in the same task returned the rendered red pixel even with `preserveDrawingBuffer: false`; use `true` if you capture later), GPGPU results, occlusion statistics.

## Gotchas
- Default framebuffer reads after the frame was presented return cleared data unless `preserveDrawingBuffer` is true (after two animation frames the pixel read (0,0,0,0) instead of green, and (0,255,0,255) with `preserveDrawingBuffer: true`); read in the same task as rendering.
- Rows come bottom-up from the framebuffer origin (a 1x2 texture uploaded as 10 then 20 read back 10 first); flip when making images.
- Chromium (Edge here) logs 'GPU stall due to ReadPixels' for synchronous reads; the warning is the hint to go async.

## Verify
- [ ] Performance panel shows no long GPU-wait task on the readback frame.
- [ ] Picking result arrives within 1-2 frames and matches the clicked object.

## Checked
- headless Edge WebGL2 on ANGLE/SwiftShader and, where noted, ANGLE/D3D11 (AMD RX 6900 XT): the skill's `readPixelsAsync` function ran unchanged: it resolved [255,128,0,255] (same as the synchronous read) in 6.1 ms (4.1 ms on D3D11) with GL error 0, using `fenceSync`, `clientWaitSync` polling and `getBufferSubData` from a PIXEL_PACK_BUFFER; the readback and presentation cases above; `readBuffer(COLOR_ATTACHMENT1)` read blue and attachment 0 read red; MDN readPixels, fenceSync and WebGL best practices pages return 200. `canvas.toBlob` right after a render returned (255,0,0,255) at the centre without `preserveDrawingBuffer`.
