---
id: computing-software.computer-graphics-engineering.opengl.opengl-uniform-buffers-std140
name: opengl-uniform-buffers-std140
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, uniform-buffer-objects, ubo, std140, uniform-blocks, binding-points, glbindbufferrange, layout-binding]
level: practitioner
status: docs-checked
description: "Share uniforms across OpenGL programs with uniform buffer objects: std140 padding rules, explicit binding points, per-draw ranges and matching C structs."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL uniform buffers and std140

**Goal:** camera/light/material constants live in buffers shared by every program, laid
out so the C++ struct and the GLSL block agree byte for byte.

## 1. Declare the block with explicit binding
```glsl
layout(std140, binding = 0) uniform Camera {
    mat4 view;          // offset 0
    mat4 proj;          // 64
    vec3 eyePos;        // 128 (vec3 aligned to 16)
    float time;         // 140 - packs into vec3's tail
    vec4 frustum[6];    // 144
};
```
`binding = N` removes the need for `glGetUniformBlockIndex` +
`glUniformBlockBinding` per program.

## 2. std140 rules that bite
| GLSL type | base alignment | size |
|---|---|---|
| float/int/bool | 4 | 4 |
| vec2 | 8 | 8 |
| vec3 / vec4 | 16 | 12 / 16 |
| array element (any scalar/vector) | **16** | rounded to 16 |
| mat4 | 16 (as 4 vec4 columns) | 64 |
| mat3 | 16 (3 vec4 columns) | **48** |
| struct | 16 | rounded up to 16 |
- `float arr[8]` takes **128 bytes**, not 32 — use `vec4 arr[2]` and index `arr[i/4][i%4]`.
- Avoid `vec3` members and `mat3`; use vec4/mat4 or put a float after a vec3 deliberately.
- Mirror in C++ with `alignas(16)` and `static_assert(offsetof(Camera, frustum) == 144)`.

## 3. Create, bind, update
```c
glCreateBuffers(1, &ubo);
glNamedBufferStorage(ubo, sizeof(Camera), NULL, GL_DYNAMIC_STORAGE_BIT);
glBindBufferBase(GL_UNIFORM_BUFFER, 0, ubo);
glNamedBufferSubData(ubo, 0, sizeof cam, &cam);         // once per frame
```
Per-object data in one big UBO: `glBindBufferRange(GL_UNIFORM_BUFFER, 1, ubo, i*stride, size)`
with `stride` rounded up to `GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT` (query it; the 4.6 spec caps the value at 256).
For streaming every frame combine with a persistent-mapped ring.

## 4. Limits
- `GL_MAX_UNIFORM_BLOCK_SIZE` is guaranteed only 16 KiB (16384 bytes). Larger or
  variable-length data → SSBO (std430).
- `GL_MAX_UNIFORM_BUFFER_BINDINGS` is at least 84 in the 4.6 spec (the gl4 reference page still says 36) — plan a fixed binding map
  (0 = frame, 1 = view, 2 = material, 3 = object) shared by all shaders.

## Debugging layout mismatches
Query actual offsets the compiler chose (a block without an instance name lists members by bare name; with an
instance name the resource name is `Block.member`):
```c
GLuint idx = glGetProgramResourceIndex(prog, GL_UNIFORM, "eyePos");   // block has no instance name
GLenum p = GL_OFFSET; GLint off; glGetProgramResourceiv(prog, GL_UNIFORM, idx, 1, &p, 1, NULL, &off);
```
Garbage values in one member and correct values before it = an alignment mismatch at that member.

## Verify
- [ ] `static_assert`s on struct offsets match `glGetProgramResourceiv` offsets.
- [ ] RenderDoc's buffer view of the UBO decodes to sane values with the block layout.
- [ ] All programs share one binding map; no per-program `glUniformBlockBinding` calls remain.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022, sections 7.3.1 and 7.6.2.2, tables 23.x and the change list), GLSL 4.60 spec, gl4 reference page for glGet. Confirmed: std140 rules (array element alignment rounded up to vec4, mat3 as three vec4 columns = 48 bytes, struct alignment rounded to vec4); `GL_MAX_UNIFORM_BLOCK_SIZE` minimum 16384; `MAX_UNIFORM_BUFFER_BINDINGS` minimum raised to 84 (the reference page is stale at 36); `UNIFORM_BUFFER_OFFSET_ALIGNMENT` is a maximum-allowed value of 256; resource naming (`Block.member` only for blocks with an instance name). Fixed: the program-resource query used `Camera.eyePos` for a block declared without an instance name. Removed: GL 4.2 tag, typical 64 KiB and common-256 claims.

Method: documentation only; no commands were run.
