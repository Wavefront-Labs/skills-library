---
id: computing-software.computer-graphics-engineering.opengl.opengl-persistent-mapped-buffer-streaming
name: opengl-persistent-mapped-buffer-streaming
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, opengl-buffers, glbufferstorage, immutable-buffers, persistent-mapping, buffer-streaming, ring-buffer, azdo, glfencesync, buffer-orphaning]
level: advanced
status: docs-checked
description: "Stream per-frame data in OpenGL 4.4+ with immutable glBufferStorage, persistent coherent mapping and a fenced triple-buffered ring instead of glBufferSubData stalls."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_buffer_storage.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferStorage.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glClientWaitSync.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL persistent-mapped buffer streaming

**Goal:** upload per-frame vertex/uniform/instance data with no driver copies and no
implicit sync stalls ("AZDO" style), on GL 4.4+ or `ARB_buffer_storage`.

## 1. Immutable storage
`glBufferStorage`/`glNamedBufferStorage` fixes size and usage flags forever
The data store is immutable: you cannot resize it — recreate instead.
```c
const GLsizeiptr FRAME = 4 << 20, N = 3;                    // 4 MiB per frame, triple buffered
GLbitfield f = GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT | GL_MAP_COHERENT_BIT;
glCreateBuffers(1, &buf);
glNamedBufferStorage(buf, FRAME * N, NULL, f | GL_DYNAMIC_STORAGE_BIT);
uint8_t* base = glMapNamedBufferRange(buf, 0, FRAME * N, f);   // stays mapped for the buffer's lifetime
```
Static data: `glNamedBufferStorage(buf, size, data, 0)` — flags 0 means no client updates or mapping after creation (server-side copies and clears still work).

## 2. Fenced ring
```c
GLsync fence[N] = {0};
void* beginFrame(int i) {
    if (fence[i]) {
        GLenum r = glClientWaitSync(fence[i], GL_SYNC_FLUSH_COMMANDS_BIT, 1000000000);
        if (r == GL_TIMEOUT_EXPIRED || r == GL_WAIT_FAILED) log("ring stall");
        glDeleteSync(fence[i]);
    }
    return base + i * FRAME;            // CPU writes this frame's region
}
void endFrame(int i) { fence[i] = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0); }
```
Bind ranges with `glBindBufferRange(GL_UNIFORM_BUFFER, slot, buf, i*FRAME + off, size)`
(offsets aligned to `GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT`) or pass the offset
as `baseInstance`/vertex offset.

## 3. Coherent vs explicit flush
- `GL_MAP_COHERENT_BIT`: writes become visible automatically at the next GL command.
- Without it: map with `GL_MAP_FLUSH_EXPLICIT_BIT` and call
  `glFlushMappedNamedBufferRange` for each written range before the commands that read it.
  (`GL_CLIENT_MAPPED_BUFFER_BARRIER_BIT` plus a fence is for the opposite direction: the CPU
  reading data the GPU wrote.)

## 4. Pre-4.4 fallback: orphaning
`glBufferData(target, size, NULL, GL_STREAM_DRAW)` before each refill, or
`glMapBufferRange(..., GL_MAP_INVALIDATE_BUFFER_BIT | GL_MAP_UNSYNCHRONIZED_BIT)` with your
own fences.

## Gotchas
- Writing into a region without waiting on its fence = torn/flickering geometry that
  only shows under load.
- Do not **read** through a pointer mapped without `GL_MAP_READ_BIT` (undefined); build data in a
  CPU struct and `memcpy` it in sequentially.
- Size the ring for the worst frame; overflow must either wait or grow by recreating.
- `glClientWaitSync` returns `GL_TIMEOUT_EXPIRED` when the fence is not signalled within the
  timeout; count those returns to see how often you actually block.

## Verify
- [ ] Nsight/RenderDoc shows no `glBufferSubData` driver copies on the hot path.
- [ ] Ring-stall counter stays ~0 at target frame rate.
- [ ] Artificially slowing the GPU (heavy shader) produces stalls, never corruption.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glBufferStorage and GL_MAP_PERSISTENT_BIT GL 4.4 (gl.xml); GL_DYNAMIC_STORAGE_BIT semantics and that server-side copies and clears are always allowed (glBufferStorage refpage); the MAP_COHERENT_BIT visibility rules, including that CLIENT_MAPPED_BUFFER_BARRIER_BIT plus a fence is for GPU writes read by the CPU while client writes need FlushMapped*BufferRange when not coherent (ARB_buffer_storage); glClientWaitSync results and nanosecond timeout. Corrected: the memory-barrier alternative for non-coherent client writes was the wrong direction. Removed the unconfirmed write-combined, 100x and GPU-only claims.
Method: documentation only; no commands were run.
