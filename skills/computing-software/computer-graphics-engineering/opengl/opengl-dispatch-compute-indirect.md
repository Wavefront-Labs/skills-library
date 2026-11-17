---
id: computing-software.computer-graphics-engineering.opengl.opengl-dispatch-compute-indirect
name: opengl-dispatch-compute-indirect
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-compute, gldispatchcomputeindirect, gpu-generated-work, dispatch-indirect-buffer]
level: advanced
status: docs-checked
description: "Let the GPU size its own compute work with glDispatchComputeIndirect: building the args buffer in a shader, barriers, and group-count limits."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDispatchComputeIndirect.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_compute_shader.txt", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glDispatchComputeIndirect

Use when the amount of work is produced on the GPU (culled object lists, particle counts,
tile classification) and reading it back to the CPU would stall.

## Args layout
```c
typedef struct { GLuint num_groups_x, num_groups_y, num_groups_z; } DispatchIndirectCommand;
```
Bound to `GL_DISPATCH_INDIRECT_BUFFER`; offset must be a multiple of 4.

## Pattern: append, then size the next pass
```glsl
// pass 1 (cull): append survivors
layout(std430, binding = 0) buffer Count { uint visibleCount; };
layout(std430, binding = 1) writeonly buffer List { uint visible[]; };
...
if (isVisible) visible[atomicAdd(visibleCount, 1)] = id;
```
```glsl
// pass 2 (tiny 1-invocation kernel): write dispatch args
layout(local_size_x = 1) in;
layout(std430, binding = 0) readonly buffer Count { uint visibleCount; };
layout(std430, binding = 2) writeonly buffer Args { uvec3 dispatchArgs; };
void main() { dispatchArgs = uvec3((visibleCount + 63u) / 64u, 1u, 1u); }
```
```c
glDispatchCompute((n + 63) / 64, 1, 1);                     // pass 1
glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT);
glDispatchCompute(1, 1, 1);                                 // pass 2 writes args
glMemoryBarrier(GL_COMMAND_BARRIER_BIT | GL_SHADER_STORAGE_BARRIER_BIT);
glBindBuffer(GL_DISPATCH_INDIRECT_BUFFER, argsBuf);
glDispatchComputeIndirect(0);                               // pass 3 processes exactly visibleCount
```
`GL_COMMAND_BARRIER_BIT` covers command data sourced by `Draw*Indirect` and
`DispatchComputeIndirect` (ARB_compute_shader); forgetting it can leave the dispatch reading
stale counts.

In pass 3, guard with `if (gl_GlobalInvocationID.x >= visibleCount) return;` since the last group
is partially filled.

## Gotchas
- Group counts above `GL_MAX_COMPUTE_WORK_GROUP_COUNT` for their axis are undefined behaviour
  and may terminate the application; no error is generated. GLSL guarantees at least 65535
  per axis. Clamp in the args kernel and loop inside the shader for huge counts.
- `GL_INVALID_OPERATION` if no buffer is bound to `GL_DISPATCH_INDIRECT_BUFFER` or the command
  would read beyond the end of the buffer; `GL_INVALID_VALUE` if the offset is negative or not a
  multiple of four.
- Reset the counter each frame (`glClearNamedBufferSubData`) before pass 1.

## Verify
- [ ] Debug readback (a frame late, via PBO/persistent buffer) of args matches visibleCount.
- [ ] No CPU `glGetBufferSubData` on the per-frame path.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glDispatchComputeIndirect offset rules, error conditions and the undefined-behaviour note for counts above GL_MAX_COMPUTE_WORK_GROUP_COUNT (glDispatchComputeIndirect refpage); GL 4.3 (gl.xml); COMMAND_BARRIER_BIT covers DispatchComputeIndirect (ARB_compute_shader); 65535 per-axis minimum (GLSL 4.60). Removed the unconfirmed zero-group-count claim.
Method: documentation only; no commands were run.
