---
id: computing-software.computer-graphics-engineering.opengl.opengl-gpu-buffer-copies-and-clears
name: opengl-gpu-buffer-copies-and-clears
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, glcopybuffersubdata, glclearbufferdata, gpu-copy]
level: practitioner
status: docs-checked
description: "Copy and clear OpenGL buffers on the GPU with glCopyNamedBufferSubData and glClearNamedBufferSubData instead of CPU round trips."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glCopyBufferSubData.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glClearBufferSubData.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBufferStorage.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU-side buffer copies and clears

## Copy (GL 3.1, DSA form GL 4.5)
```c
glCopyNamedBufferSubData(src, dst, srcOffset, dstOffset, size);
// pre-DSA: bind to GL_COPY_READ_BUFFER / GL_COPY_WRITE_BUFFER, then glCopyBufferSubData
```
Uses:
- staging -> device-local: fill a persistent-mapped staging buffer, then copy into an immutable
  buffer created without `GL_DYNAMIC_STORAGE_BIT` or `GL_MAP_*` flags; server-side copies and
  clears are always allowed on such a buffer (glBufferStorage refpage).
- compacting / reordering GPU-generated data, growing a buffer (allocate bigger, copy old content).
- Overlapping ranges in the *same* buffer are an error (`GL_INVALID_VALUE`); copy through a temp.

## Clear (GL 4.3 / ARB_clear_buffer_object)
```c
GLuint zero = 0;
glClearNamedBufferData(counterBuf, GL_R32UI, GL_RED_INTEGER, GL_UNSIGNED_INT, &zero);
float fill[4] = {0,0,0,1};
glClearNamedBufferSubData(buf, GL_RGBA32F, offset, size, GL_RGBA, GL_FLOAT, fill);
```
The internal format describes how the pattern is replicated; `offset` and `size` must be
multiples of the format's element size. Passing `data = NULL` fills with zeros.

Typical uses: resetting atomic counters and indirect-draw counts each frame, clearing
histogram bins, clearing linked-list heads for OIT.

## Synchronisation
- Copies and clears are ordinary GL commands, ordered with draws in the same context. If a
  compute shader *wrote* the source via SSBO/image store, issue
  `glMemoryBarrier(GL_BUFFER_UPDATE_BARRIER_BIT)` before the copy.
- Consuming the copied data as an indirect buffer after a shader write needs
  `GL_COMMAND_BARRIER_BIT`; as vertex data, `GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT`.

## Gotchas
- Prefer `glCopyBufferSubData` to a `glGetBufferSubData` + `glBufferSubData` round trip, which
  moves the data through client memory.
- Clearing a range that is mapped is `GL_INVALID_OPERATION`, unless it was mapped with
  `GL_MAP_PERSISTENT_BIT`.

## Verify
- [ ] No `glGetBufferSubData` in the per-frame path (search the codebase / apitrace dump).
- [ ] Counter buffers read back as zero at the start of each frame in a debug build.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glCopyBufferSubData overlap rule and GL_INVALID_VALUE; glCopyNamedBufferSubData GL 4.5 and glCopyBufferSubData GL 3.1, glClearBufferSubData GL 4.3 (gl.xml); clear offset and size must be multiples of the format element size and NULL data fills with zeros; clearing a mapped range is GL_INVALID_OPERATION unless persistently mapped; server-side copies and clears work without GL_DYNAMIC_STORAGE_BIT (glBufferStorage); GL_BUFFER_UPDATE_BARRIER_BIT covers glCopyBufferSubData reads of shader writes and GL_COMMAND_BARRIER_BIT covers Draw*Indirect (glMemoryBarrier). Removed the unconfirmed VRAM-placement and PCIe claims.
Method: documentation only; no commands were run.
