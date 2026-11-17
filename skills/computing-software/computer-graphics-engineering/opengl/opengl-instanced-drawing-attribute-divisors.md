---
id: computing-software.computer-graphics-engineering.opengl.opengl-instanced-drawing-attribute-divisors
name: opengl-instanced-drawing-attribute-divisors
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-vertex-specification, gl-instancing, attribute-divisor, gldrawelementsinstanced, instancing]
level: practitioner
status: docs-checked
description: "Draw thousands of copies in one call with glDrawElementsInstanced: per-instance attributes via divisors, mat4 attributes, SSBO alternative."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glVertexAttribDivisor.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawElementsInstancedBaseInstance.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instanced drawing with attribute divisors

**Goal:** render N copies of a mesh (grass, rocks, particles) in one draw, each with its own
transform/colour, without N uniform updates.

## 1. Per-instance buffer + divisor (DSA, GL 4.5)
```c
// binding 0: per-vertex mesh, binding 1: per-instance data
glVertexArrayVertexBuffer(vao, 1, instanceVbo, 0, sizeof(Instance));
glVertexArrayBindingDivisor(vao, 1, 1);             // advance once per instance
for (int c = 0; c < 4; ++c) {                       // mat4 = 4 vec4 attribute slots
    glEnableVertexArrayAttrib(vao, 3 + c);
    glVertexArrayAttribFormat(vao, 3 + c, 4, GL_FLOAT, GL_FALSE, offsetof(Instance, model) + 16 * c);
    glVertexArrayAttribBinding(vao, 3 + c, 1);
}
glDrawElementsInstanced(GL_TRIANGLES, indexCount, GL_UNSIGNED_INT, 0, instanceCount);
```
Non-DSA: `glVertexAttribDivisor(loc, 1)` per attribute. Divisor N means the attribute advances
every N instances; 0 means per vertex.

GLSL: `layout(location = 3) in mat4 iModel;` consumes locations 3 to 6.

## 2. Alternative: SSBO indexed by gl_InstanceID
```glsl
layout(std430, binding = 0) readonly buffer Inst { mat4 model[]; };
gl_Position = viewProj * model[gl_InstanceID + gl_BaseInstance] * vec4(aPos, 1);
```
Cleaner for large/variable per-instance structs and for GPU-culled lists. `gl_InstanceID` does
**not** include the base instance (add `gl_BaseInstance` from GL 4.6/`ARB_shader_draw_parameters`).
Divisor attributes do honour `baseInstance` in `glDrawElementsInstancedBaseInstance`.

## 3. Updating instance data
Rewrite per frame with buffer orphaning (`glNamedBufferData` with same size then sub-data) or a
persistent-mapped ring; for static scatter upload once.

## Gotchas
- Normals need the inverse-transpose; with non-uniform scale pass a normal matrix per instance
  or compute `transpose(inverse(mat3(model)))` in the shader (cost per vertex).
- Forgetting the divisor gives every vertex a different instance matrix: exploded geometry.

## Verify
- [ ] RenderDoc mesh viewer shows the instance attribute stepping per instance, not per vertex.
- [ ] Draw call count is 1 per mesh type; CPU time flat as instance count grows.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: divisor 0 advances per vertex and a non-zero divisor once per divisor instances (glVertexAttribDivisor); instanced attribute index is gl_InstanceID / divisor + baseInstance and baseinstance does not change gl_InstanceID (glDrawElementsInstancedBaseInstance); gl_BaseInstance exists in GLSL 4.60; a matrix input uses one location per column (GLSL 4.60); glVertexAttribDivisor GL 3.3, glDrawElementsInstancedBaseInstance GL 4.2, glVertexArrayBindingDivisor GL 4.5 (gl.xml). Removed the unconfirmed small-mesh performance claim.
Method: documentation only; no commands were run.
