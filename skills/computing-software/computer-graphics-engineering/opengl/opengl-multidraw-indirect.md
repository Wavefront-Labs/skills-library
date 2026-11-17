---
id: computing-software.computer-graphics-engineering.opengl.opengl-multidraw-indirect
name: opengl-multidraw-indirect
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vertex-specification, gl-drawing, multidraw-indirect, gl-draw-indirect, gldrawelementsindirectcommand, gl-drawid, shader-draw-parameters, gpu-driven-rendering, azdo]
level: advanced
status: docs-checked
description: "Submit thousands of meshes in one call with glMultiDrawElementsIndirect: shared vertex/index buffers, command layout, gl_DrawID lookup and GPU-written indirect counts."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMultiDrawElementsIndirect.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_multi_draw_indirect.txt", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_indirect_parameters.txt", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_draw_parameters.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL multi-draw indirect

**Goal:** draw every mesh that shares a vertex format and program with a single
`glMultiDrawElementsIndirect`, with per-draw data fetched by `gl_DrawID` — the core of
"approaching zero driver overhead" GL rendering (GL 4.3+, draw parameters 4.6).

## 1. One big vertex and index buffer
Pack all meshes into one VBO + one IBO (a suballocator or simple append). Record per mesh
`firstIndex`, `indexCount`, `baseVertex`.

## 2. Command buffer
```c
typedef struct {
    GLuint count;          // index count
    GLuint instanceCount;  // 0 = culled
    GLuint firstIndex;
    GLint  baseVertex;
    GLuint baseInstance;   // free slot: use as object index
} DrawElementsIndirectCommand;     // 20 bytes, tightly packed

glNamedBufferStorage(indirectBuf, n * sizeof(Cmd), cmds, GL_DYNAMIC_STORAGE_BIT);
glBindBuffer(GL_DRAW_INDIRECT_BUFFER, indirectBuf);
glBindVertexArray(vao);   // VAO references the shared VBO/IBO
glMultiDrawElementsIndirect(GL_TRIANGLES, GL_UNSIGNED_INT, (void*)0, n, 0 /*stride: packed*/);
```

## 3. Per-draw data in the shader
GL 4.6 / `ARB_shader_draw_parameters`:
```glsl
#version 460
layout(std430, binding = 0) readonly buffer Objects { mat4 model[]; uint material[]; };
void main() {
    uint obj = gl_BaseInstance + gl_InstanceID;    // or gl_DrawID for one instance per draw
    gl_Position = viewProj * model[obj] * vec4(aPos, 1);
}
```
Without draw parameters: put `baseInstance` to work via an instanced attribute with divisor 1
that holds the object index — works on GL 4.2+ hardware.

## 4. GPU-driven variant
A compute shader culls objects and writes commands (setting `instanceCount = 0` or
compacting) plus a count. Then:
```c
glMemoryBarrier(GL_COMMAND_BARRIER_BIT);
glBindBuffer(GL_PARAMETER_BUFFER, countBuf);                   // GL 4.6 / ARB_indirect_parameters
glMultiDrawElementsIndirectCount(GL_TRIANGLES, GL_UNSIGNED_INT, 0, 0, maxDraws, 0);
```

## Gotchas
- Textures must be reachable per draw: use texture arrays indexed by material, or bindless
  handles in an SSBO. Binding textures between draws defeats the point.
- `gl_DrawID` is dynamically uniform, so it may select a sampler; an arbitrary per-vertex value
  may not (unless an extension such as `NV_gpu_shader5` relaxes the rule).
- Forgetting `GL_COMMAND_BARRIER_BIT` after compute writes means the draw may read stale commands.
- Benchmark against a loop of plain draws on your target hardware.

## Verify
- [ ] RenderDoc shows one MDI event expanding into N sub-draws with correct meshes.
- [ ] CPU frame time for the scene is flat as object count grows (driver overhead gone).
- [ ] Culled objects have `instanceCount == 0` and do not appear.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: DrawElementsIndirectCommand layout of five uints/ints and stride 0 meaning tightly packed (glMultiDrawElementsIndirect refpage); baseInstance defined for GL 4.2 and later (glDrawElementsIndirect refpage); glMultiDrawElementsIndirect GL 4.3, glMultiDrawElementsIndirectCount and GL_PARAMETER_BUFFER GL 4.6 (gl.xml); the Count signature (mode, type, indirect, drawcount, maxdrawcount, stride) in ARB_indirect_parameters; gl_DrawID and gl_BaseInstance semantics, gl_DrawID dynamically uniform. Removed the unconfirmed driver-emulation claim.
Method: documentation only; no commands were run.
