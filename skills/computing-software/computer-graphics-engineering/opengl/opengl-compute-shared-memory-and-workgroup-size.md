---
id: computing-software.computer-graphics-engineering.opengl.opengl-compute-shared-memory-and-workgroup-size
name: opengl-compute-shared-memory-and-workgroup-size
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-compute, gl-shared-variables, local-size, barrier, groupmemorybarrier]
level: advanced
status: docs-checked
description: "Use shared variables and barrier() in OpenGL compute shaders correctly, choose local_size for the hardware, and respect shared-memory limits."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_compute_shader.txt", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_compute_variable_group_size.txt", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared memory and work-group sizing in GL compute

## Work-group size
```glsl
layout(local_size_x = 8, local_size_y = 8, local_size_z = 1) in;   // 64 invocations
```
- Make the group a multiple of the target GPU's SIMD width (warp or wavefront size, which
  differs between vendors and generations); 64 invocations is a reasonable starting point to
  tune with timer queries.
- 2D image kernels: 8x8 or 16x16 so neighbouring invocations touch neighbouring texels.
- Limits: `GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS`, `GL_MAX_COMPUTE_WORK_GROUP_SIZE` (indexed per
  axis; GLSL guarantees at least 1024 x 1024 x 64) and `GL_MAX_COMPUTE_SHARED_MEMORY_SIZE` (at
  least 32768 bytes per ARB_compute_shader).
- `layout(local_size_x_id = 0)` is SPIR-V only; in GLSL source inject the size with a `#define`
  at compile time, or use `ARB_compute_variable_group_size` (`local_size_variable`).

## Shared variables and barriers
```glsl
shared vec4 tile[16 + 2*R][16 + 2*R];          // tile + apron for a radius-R filter
void main() {
    ivec2 g = ivec2(gl_GlobalInvocationID.xy), l = ivec2(gl_LocalInvocationID.xy);
    // cooperative load: each invocation loads one or more texels incl. apron
    for (int y = l.y; y < 16 + 2*R; y += 16)
      for (int x = l.x; x < 16 + 2*R; x += 16)
        tile[y][x] = imageLoad(src, ivec2(gl_WorkGroupID.xy) * 16 + ivec2(x, y) - R);
    barrier();                                  // all writes to shared visible + all invocations arrived
    vec4 sum = vec4(0);
    for (int i = -R; i <= R; ++i) sum += tile[l.y + R][l.x + R + i];
    imageStore(dst, g, sum / float(2*R + 1));
}
```
Data written to `shared` variables is visible to other invocations of the same work group, but
the order of reads and writes between invocations is undefined without synchronisation: use
`barrier()` to order them. For buffer or image writes that other invocations in the group must
see, add `memoryBarrierBuffer()` / `memoryBarrierImage()` (or `groupMemoryBarrier()`) before
`barrier()`.

## Rules that bite
- In compute shaders `barrier()` may appear in control flow only if all controlling expressions
  are dynamically uniform, so never inside `if (gl_LocalInvocationIndex < N)`; otherwise some
  invocations may never reach it.
- No synchronisation exists **between** work groups inside a dispatch. Multi-pass algorithms need
  separate dispatches with `glMemoryBarrier` between them.
- Total `shared` storage in a program is capped by `GL_MAX_COMPUTE_SHARED_MEMORY_SIZE`; larger
  tiles also leave less shared memory for other groups, so measure tile sizes.

## Verify
- [ ] Output matches a CPU reference on non-multiple-of-16 image sizes (bounds checks on edges).
- [ ] GPU timer query shows the shared-memory version beats the naive per-texel fetch version.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: GLSL 4.60 built-in minimums gl_MaxComputeWorkGroupSize {1024, 1024, 64} and gl_MaxComputeWorkGroupCount {65535, 65535, 65535}; MAX_COMPUTE_SHARED_MEMORY_SIZE minimum 32768 (ARB_compute_shader); local_size_x_id is SPIR-V only; shared-variable visibility within a work group and ordering only through barrier(); barrier() must be in dynamically uniform control flow in compute shaders; local_size_variable (ARB_compute_variable_group_size). Removed the unconfirmed SIMD-width table, invocation minimum, occupancy and bank-conflict claims.
Method: documentation only; no commands were run.
