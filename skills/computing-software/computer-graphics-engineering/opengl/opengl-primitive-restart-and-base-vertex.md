---
id: computing-software.computer-graphics-engineering.opengl.opengl-primitive-restart-and-base-vertex
name: opengl-primitive-restart-and-base-vertex
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-vertex-specification, primitive-restart, base-vertex, index-buffers, gldrawelementsbasevertex]
level: practitioner
status: docs-checked
description: "Use index buffers well in OpenGL: 16 vs 32-bit indices, primitive restart for strips, glDrawElementsBaseVertex to share one buffer across meshes."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPrimitiveRestartIndex.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawElementsBaseVertex.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glEnable.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBindBuffer.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index buffers: primitive restart and base vertex

**Goal:** draw indexed geometry with the smallest index type, many strips in one call, and many
meshes from one shared vertex/index buffer.

## 1. Index type
Use `GL_UNSIGNED_SHORT` when a mesh has < 65536 vertices (half the bandwidth); otherwise
`GL_UNSIGNED_INT`. With base vertex (below) a big shared VBO still allows 16-bit indices
per mesh because indices are relative to each mesh's `baseVertex`.

## 2. Primitive restart
One draw of many triangle strips or line strips separated by a sentinel index:
```c
glEnable(GL_PRIMITIVE_RESTART_FIXED_INDEX);   // GL 4.3 / ES 3.0: sentinel = max value of type
// 0xFFFF for GL_UNSIGNED_SHORT, 0xFFFFFFFF for GL_UNSIGNED_INT
```
Legacy GL 3.1: `glEnable(GL_PRIMITIVE_RESTART); glPrimitiveRestartIndex(0xFFFF);` (the index is
your choice). The fixed-index form's sentinel is always the maximum value of the index type.
Strips vs lists: measure indexed triangle lists in vertex-cache-optimised order (meshoptimizer)
against restarted strips; restart is mainly useful for line strips and terrain.

## 3. Base vertex
```c
glDrawElementsBaseVertex(GL_TRIANGLES, mesh.indexCount, GL_UNSIGNED_INT,
                         (void*)(mesh.firstIndex * sizeof(GLuint)), mesh.baseVertex);
```
`baseVertex` is added to every fetched index before vertex fetch. Lets you append meshes into
one VBO/IBO without rewriting their indices; the step before multi-draw indirect
(see computing-software.computer-graphics-engineering.opengl.opengl-multidraw-indirect).

## Gotchas
- The `indices` argument is a **byte offset** (cast to a pointer) into the buffer bound to
  `GL_ELEMENT_ARRAY_BUFFER`.

## Verify
- [ ] RenderDoc mesh view shows strips separated correctly (no long connecting slivers).
- [ ] Two meshes in one VBO render with correct geometry using only base vertex offsets.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: GL_PRIMITIVE_RESTART and glPrimitiveRestartIndex GL 3.1, GL_PRIMITIVE_RESTART_FIXED_INDEX GL 4.3 and ES 3.0, fixed index equals 2^n - 1 for the index type (glEnable refpage, gl.xml); glDrawElementsBaseVertex adds basevertex to each element and indices is a byte offset into the GL_ELEMENT_ARRAY_BUFFER (refpages). Removed the unconfirmed WebGL2, Vulkan, restart-versus-base-vertex ordering and VAO-binding claims.
Method: documentation only; no commands were run.
