---
id: computing-software.computer-graphics-engineering.opengl.opengl-shader-storage-buffers-std430
name: opengl-shader-storage-buffers-std430
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, ssbo, shader-storage-buffer, std430, unsized-arrays, atomics, glmemorybarrier, compute-shader]
level: practitioner
status: docs-checked
description: "Use OpenGL shader storage buffers for large or writable data: std430 layout, unsized arrays, atomics, and the memory barriers needed between writes and reads."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_storage_buffer_object.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL shader storage buffers and std430

**Goal:** big, variable-length, GPU-writable arrays (instance transforms, particles, light
lists, culling output) accessed from any shader stage, with correct layout and visibility.
GL 4.3+.

## 1. Declare
```glsl
struct Particle { vec4 posLife; vec4 vel; };          // 32 bytes, no padding surprises
layout(std430, binding = 3) buffer Particles {
    uint count;
    uint _pad[3];
    Particle p[];                                       // unsized: must be the LAST member
};
layout(std430, binding = 4) readonly buffer Instances { mat4 model[]; };
```
Array length in shader: `p.length()` (computed from the bound range size).

## 2. std430 vs std140
std430 drops the "round arrays and structs to 16" rule: `float a[8]` is 32 bytes, `vec2`
arrays pack tightly. **vec3 is still aligned to 16** — a `vec3` array has a 16-byte
stride. Keep vec3 out of SSBO structs (use vec4 or separate float arrays).

## 3. Bind
```c
glCreateBuffers(1, &ssbo);
glNamedBufferStorage(ssbo, bytes, init, GL_DYNAMIC_STORAGE_BIT);
glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, ssbo);
// or a sub-range: offset aligned to GL_SHADER_STORAGE_BUFFER_OFFSET_ALIGNMENT
```

## 4. Writes, atomics and barriers
```glsl
uint slot = atomicAdd(count, 1u);
if (slot < p.length()) p[slot] = newParticle;
```
Incoherent memory access: after a dispatch/draw that writes an SSBO, before the next
command reads it:
```c
glDispatchCompute(groups, 1, 1);
glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT);         // next shader reads the SSBO
// if consumed as vertex attributes / indirect args, use the matching bits:
glMemoryBarrier(GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT | GL_COMMAND_BARRIER_BIT);
```
The barrier bit names the **consumer**, not the producer. Inside one dispatch, use
`memoryBarrierBuffer()` + `barrier()` for intra-workgroup ordering.

## Gotchas
- A fragment shader that writes an SSBO executes once per covering fragment, so overdraw
  repeats the write: make writes idempotent or use atomics.
- `readonly`/`writeonly` qualifiers document intent and catch mistakes.
- Query `GL_MAX_SHADER_STORAGE_BLOCK_SIZE`, `GL_MAX_SHADER_STORAGE_BUFFER_BINDINGS` and the
  per-stage `GL_MAX_*_SHADER_STORAGE_BLOCKS` (for example
  `GL_MAX_VERTEX_SHADER_STORAGE_BLOCKS`) instead of assuming limits.
- Keep small, read-only constant data in UBOs and use SSBOs where you need large, unsized or
  writable data.

## Verify
- [ ] C++ struct size/stride `static_assert`ed against the std430 layout.
- [ ] Removing the `glMemoryBarrier` produces visible flicker/garbage (proves it is needed),
      restoring it fixes it.
- [ ] Atomic counters read back (`glGetNamedBufferSubData` in debug) never exceed capacity.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: std430 differs from std140 only in not rounding the base alignment of scalar and vector arrays and structures up to vec4 (ARB_shader_storage_buffer_object); an unsized array must be the last member and length() is evaluated at run time from the buffer size (GLSL 4.60); GL_SHADER_STORAGE_BUFFER_OFFSET_ALIGNMENT, GL_MAX_SHADER_STORAGE_BLOCK_SIZE, per-stage block limits (extension and glGet); GL_SHADER_STORAGE_BARRIER_BIT semantics (glMemoryBarrier). Removed the unconfirmed limit minimums, helper-invocation and read-speed claims.
Method: documentation only; no commands were run.
