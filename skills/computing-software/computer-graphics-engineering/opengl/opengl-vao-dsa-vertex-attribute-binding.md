---
id: computing-software.computer-graphics-engineering.opengl.opengl-vao-dsa-vertex-attribute-binding
name: opengl-vao-dsa-vertex-attribute-binding
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vertex-specification, gl-drawing, vao, vertex-attrib-binding, dsa, direct-state-access, glvertexarrayattribformat, interleaved-vertices, normalized-attributes]
level: practitioner
status: docs-checked
description: "Describe vertex input in OpenGL 4.5 with DSA vertex array objects: separate attribute format and buffer binding, interleaved vs split streams, integer and normalised attributes."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glVertexAttribFormat.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL VAOs with DSA and separate attribute binding

**Goal:** vertex layouts declared once, independent of which buffer feeds them, using the
`ARB_vertex_attrib_binding` model with GL 4.5 DSA entry points (spec ch. 10).

## 1. Format vs binding
- **Attribute format** (location, components, type, relative offset) — the shape.
- **Binding point** (buffer, base offset, stride, divisor) — where the bytes come from.
One VAO per vertex *format*; switch meshes by rebinding buffers only.

```c
struct Vtx { float pos[3]; int16_t nrm[4]; uint16_t uv[2]; };   // 20 bytes
GLuint vao; glCreateVertexArrays(1, &vao);
// format
glEnableVertexArrayAttrib(vao, 0);
glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, offsetof(Vtx,pos));
glEnableVertexArrayAttrib(vao, 1);
glVertexArrayAttribFormat(vao, 1, 4, GL_SHORT, GL_TRUE, offsetof(Vtx,nrm));        // snorm -> [-1,1]
glEnableVertexArrayAttrib(vao, 2);
glVertexArrayAttribFormat(vao, 2, 2, GL_UNSIGNED_SHORT, GL_TRUE, offsetof(Vtx,uv)); // unorm
// attributes -> binding 0
for (int a = 0; a < 3; ++a) glVertexArrayAttribBinding(vao, a, 0);
// per mesh:
glVertexArrayVertexBuffer(vao, 0, mesh.vbo, 0, sizeof(Vtx));
glVertexArrayElementBuffer(vao, mesh.ibo);
glBindVertexArray(vao);
```

## 2. Integer and double attributes
- `glVertexArrayAttribIFormat` for `ivec`/`uvec` inputs (bone indices, material ids).
  Using the float version with an `int` input yields garbage — a classic skinning bug.
- `glVertexArrayAttribLFormat` for `double` inputs.

## 3. Interleaved vs split streams
- Interleaved (one binding) keeps each vertex's attributes together.
- Split position into its own binding for **depth/shadow passes**: they read only
  positions, so they fetch less data.
```c
glVertexArrayAttribBinding(vao, 0, 0);   // position stream
glVertexArrayAttribBinding(vao, 1, 1);   // everything else
```

## 4. Attribute-less and vertex pulling
Fullscreen triangles: bind an empty VAO and use `gl_VertexID`. Fully vertex-pulled renderers read SSBOs in the
shader and can do the same. The core profile has no default VAO: vertex-array commands generate
`GL_INVALID_OPERATION` while none is bound, so create one.

## Gotchas
- `glVertexArrayElementBuffer` stores the index buffer **in the VAO**; with legacy
  bind-to-edit, binding `GL_ELEMENT_ARRAY_BUFFER` while a different VAO is bound silently
  modifies that VAO.
- Shader `layout(location = N)` must match; query mismatches with
  `glGetProgramResourceLocation(prog, GL_PROGRAM_INPUT, "aNormal")`.
- Disabled attributes read the "current value" (default `0,0,0,1`) — a missing
  `glEnableVertexArrayAttrib` gives black/flat meshes, not an error.

## Verify
- [ ] A frame debugger's mesh viewer shows correct positions/normals/UVs for VS input.
- [ ] Switching meshes changes only `glVertexArrayVertexBuffer`/`ElementBuffer`, no format calls.
- [ ] Depth-only pass reads a position-only stream.

## Checked

Date: 2026-10-26. Documentation: gl4 reference page for glVertexAttribFormat (version table: the glVertexArray* DSA functions are 4.5) and OpenGL 4.6 core spec (5 May 2022, chapter 10). Confirmed: attribute format and binding are separate (`glVertexArrayAttribFormat`, `glVertexArrayAttribBinding`, `glVertexArrayVertexBuffer`); `IFormat` and `LFormat` for integer and double inputs; the element array buffer binding is VAO state; generic attributes have the initial value (0, 0, 0, 1); vertex-array commands give `GL_INVALID_OPERATION` with no VAO bound; `glGetProgramResourceLocation` with `GL_PROGRAM_INPUT`. Removed: GL 4.3 tag, bandwidth-halving and cache claims, RenderDoc reference.

Method: documentation only; no commands were run.
