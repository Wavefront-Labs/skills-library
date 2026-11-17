---
id: computing-software.computer-graphics-engineering.opengl.opengl-mapbufferrange-access-flags
name: opengl-mapbufferrange-access-flags
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, glmapbufferrange, map-unsynchronized, map-flush-explicit, buffer-streaming]
level: advanced
status: docs-checked
description: "Choose glMapBufferRange access flags (INVALIDATE, UNSYNCHRONIZED, FLUSH_EXPLICIT) to stream data without implicit GPU stalls or corrupt draws."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMapBufferRange.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glFlushMappedBufferRange.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glUnmapBuffer.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferStorage.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glMapBufferRange access flags

A plain `glMapBuffer(GL_WRITE_ONLY)` on a buffer the GPU is still using may make the driver
synchronise with pending work (a stall). The range flags tell it what you intend.

| Flag | Meaning | Use when |
|---|---|---|
| `GL_MAP_WRITE_BIT` / `READ_BIT` | Access direction | always one of them |
| `GL_MAP_INVALIDATE_RANGE_BIT` | Old contents of the range may be discarded | overwriting a whole sub-range |
| `GL_MAP_INVALIDATE_BUFFER_BIT` | Whole buffer discardable (orphan) | rewriting everything each frame |
| `GL_MAP_UNSYNCHRONIZED_BIT` | Driver must NOT wait for pending GPU use | ring buffers where you guarantee no overlap |
| `GL_MAP_FLUSH_EXPLICIT_BIT` | You call `glFlushMappedBufferRange` for written bytes | writing a few sparse regions |

## Ring-buffer pattern (classic, pre-4.4)
```c
size_t need = bytes;
if (head + need > cap) {                       // wrap: orphan once, start at 0
    void* p = glMapNamedBufferRange(buf, 0, need,
        GL_MAP_WRITE_BIT | GL_MAP_INVALIDATE_BUFFER_BIT);
    head = 0; memcpy(p, src, need);
} else {
    void* p = glMapNamedBufferRange(buf, head, need,
        GL_MAP_WRITE_BIT | GL_MAP_UNSYNCHRONIZED_BIT | GL_MAP_INVALIDATE_RANGE_BIT);
    memcpy(p, src, need);
}
glUnmapNamedBuffer(buf);
draw_from(buf, head); head += align_up(need, 256);
```
`UNSYNCHRONIZED` is only safe because the region past `head` has not been used since the last
orphan. If you wrap without orphaning, guard each region with a fence (`glFenceSync`) and
`glClientWaitSync` before reuse.

## Flush explicit
```c
char* p = glMapNamedBufferRange(buf, 0, size, GL_MAP_WRITE_BIT | GL_MAP_FLUSH_EXPLICIT_BIT);
write(p + offA, ...); glFlushMappedNamedBufferRange(buf, offA, lenA);   // offsets relative to map start
write(p + offB, ...); glFlushMappedNamedBufferRange(buf, offB, lenB);
glUnmapNamedBuffer(buf);
```

## Gotchas
- `glUnmapBuffer` can return `GL_FALSE`, which leaves the data store contents undefined;
  reinitialise the buffer.
- `GL_MAP_READ_BIT` combined with `GL_MAP_INVALIDATE_RANGE_BIT`, `GL_MAP_INVALIDATE_BUFFER_BIT`
  or `GL_MAP_UNSYNCHRONIZED_BIT` is `GL_INVALID_OPERATION`, as is `GL_MAP_FLUSH_EXPLICIT_BIT`
  without `GL_MAP_WRITE_BIT`.
- Using the pointer for an access you did not request (reading without `GL_MAP_READ_BIT`, writing
  without `GL_MAP_WRITE_BIT`) gives undefined results and may terminate the program. Map for
  write and write only.
- On GL 4.4+ prefer persistent mapping (`glBufferStorage` + `GL_MAP_PERSISTENT_BIT`) and skip
  map/unmap per frame entirely.

## Verify
- [ ] Any KHR_debug performance messages about buffer synchronisation disappear.
- [ ] No flicker or garbage geometry at high frame rates (overlap bug shows as random corruption).

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed (glMapBufferRange, glFlushMappedBufferRange, glUnmapBuffer refpages): meaning of INVALIDATE_RANGE, INVALIDATE_BUFFER, UNSYNCHRONIZED, FLUSH_EXPLICIT and PERSISTENT flags; the GL_INVALID_OPERATION conditions (READ with INVALIDATE or UNSYNCHRONIZED, FLUSH_EXPLICIT without WRITE); flush offsets are relative to the start of the mapped range; glUnmapBuffer returning GL_FALSE leaves contents undefined; glMapBufferRange behaviour for unrequested access; GL_MAP_PERSISTENT_BIT GL 4.4 (gl.xml). Corrected: READ_BIT also conflicts with UNSYNCHRONIZED. Removed unconfirmed stall mechanics, uncached-memory and vendor claims.
Method: documentation only; no commands were run.
