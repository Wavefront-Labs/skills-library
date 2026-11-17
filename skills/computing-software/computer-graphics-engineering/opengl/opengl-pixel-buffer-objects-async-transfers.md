---
id: computing-software.computer-graphics-engineering.opengl.opengl-pixel-buffer-objects-async-transfers
name: opengl-pixel-buffer-objects-async-transfers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-textures, pixel-buffer-objects, async-readback, async-texture-upload]
level: advanced
status: docs-checked
description: "Use OpenGL pixel buffer objects for asynchronous texture uploads and non-blocking glReadPixels readback with fences and multi-buffering."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glReadPixels.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pixel buffer objects (PBOs)

When a buffer is bound to `GL_PIXEL_UNPACK_BUFFER` / `GL_PIXEL_PACK_BUFFER`, the pointer
argument of texture upload / readback calls becomes a **byte offset into that buffer**, and the
transfer can proceed asynchronously.

## Async readback (screenshots, video capture, GPU->CPU data)
```c
const int N = 3;                    // frames of latency you accept
GLuint pbo[N]; GLsync fence[N] = {};
glCreateBuffers(N, pbo);
for (int i = 0; i < N; ++i) glNamedBufferStorage(pbo[i], w*h*4, NULL, GL_MAP_READ_BIT | GL_CLIENT_STORAGE_BIT);

// frame f
int i = f % N;
glBindBuffer(GL_PIXEL_PACK_BUFFER, pbo[i]);
glReadPixels(0, 0, w, h, GL_BGRA, GL_UNSIGNED_BYTE, (void*)0);   // queued, returns immediately
fence[i] = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
glBindBuffer(GL_PIXEL_PACK_BUFFER, 0);

int j = (f + 1) % N;                // oldest
if (fence[j] && glClientWaitSync(fence[j], GL_SYNC_FLUSH_COMMANDS_BIT, 0) != GL_TIMEOUT_EXPIRED) {
    void* p = glMapNamedBufferRange(pbo[j], 0, w*h*4, GL_MAP_READ_BIT);
    consume(p); glUnmapNamedBuffer(pbo[j]);
    glDeleteSync(fence[j]); fence[j] = 0;
}
```
Reading into client memory (`glReadPixels` with no pack buffer bound) must wait until the pixels have been
produced, so it synchronises the CPU with the GPU. The flush flag on the poll above matters: a fence that was
never flushed may not signal.

## Async upload (video frames, streaming textures)
```c
glBindBuffer(GL_PIXEL_UNPACK_BUFFER, upPbo[i]);
void* dst = glMapNamedBufferRange(upPbo[i], 0, bytes, GL_MAP_WRITE_BIT | GL_MAP_INVALIDATE_BUFFER_BIT);
decode_frame_into(dst); glUnmapNamedBuffer(upPbo[i]);
glTextureSubImage2D(tex, 0, 0, 0, w, h, GL_BGRA, GL_UNSIGNED_BYTE, (void*)0);  // source is the bound unpack buffer
glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0);
```
Use 2-3 upload PBOs round-robin, or one persistent-mapped ring buffer with fences.

## Gotchas
- Leaving a PBO bound makes *every* later `glTexSubImage` treat its pointer as an offset
  into that buffer. Always unbind (bind 0) after use.
- Choose the format and type the implementation prefers (`glGetInternalformativ` with `GL_READ_PIXELS_FORMAT`
  or `GL_TEXTURE_IMAGE_FORMAT`, and the matching `..._TYPE` queries); a conversion may defeat the async benefit.
- `GL_PACK_ALIGNMENT` / `GL_UNPACK_ALIGNMENT` still apply to PBO transfers.
- Rows come back bottom-up; flip when saving images.

## Verify
- [ ] No synchronous readback shows up in a CPU profile of the capture frame.
- [ ] CPU frame time no longer spikes on capture frames (measure with and without PBO path).

## Checked

Date: 2026-10-26. Documentation: gl4 reference page for glReadPixels and OpenGL 4.6 core spec (5 May 2022, sync object and internalformat query sections). Confirmed: a bound `GL_PIXEL_PACK_BUFFER` turns the data pointer into an offset and errors apply when the store is mapped or too small; `GL_CLIENT_STORAGE_BIT`, `GL_MAP_INVALIDATE_BUFFER_BIT`; `glClientWaitSync` with `GL_SYNC_FLUSH_COMMANDS_BIT` (an unflushed fence can make a wait hang); `GL_READ_PIXELS_FORMAT` and `GL_TEXTURE_IMAGE_FORMAT` queries; `GL_PACK_ALIGNMENT`/`GL_UNPACK_ALIGNMENT` apply. Fixed: the fence poll now passes the flush flag. Removed: the BGRA-on-Windows claim, the KHR_debug message text and the full-pipeline-flush wording (no documentation read).

Method: documentation only; no commands were run.
