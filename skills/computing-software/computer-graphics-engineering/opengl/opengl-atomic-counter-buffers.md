---
id: computing-software.computer-graphics-engineering.opengl.opengl-atomic-counter-buffers
name: opengl-atomic-counter-buffers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-buffer-objects, atomic-counter-buffer, atomic-uint, glsl-atomics]
level: practitioner
status: docs-checked
description: "Use GLSL atomic_uint counters backed by atomic counter buffers for append buffers and statistics, and know when SSBO atomics are better."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_atomic_counters.txt", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_atomic_counter_ops.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glMemoryBarrier.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGet.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomic counter buffers

`atomic_uint` is a 32-bit unsigned counter with increment/decrement only, stored in a buffer
bound to `GL_ATOMIC_COUNTER_BUFFER`. GLSL 4.60 also provides `atomicCounterAdd`, `atomicCounterSubtract`, `atomicCounterMin`,
`atomicCounterMax`, `atomicCounterAnd`, `atomicCounterOr`, `atomicCounterXor`,
`atomicCounterExchange` and `atomicCounterCompSwap`.

## Shader
```glsl
layout(binding = 0, offset = 0) uniform atomic_uint fragCount;
layout(binding = 0, offset = 4) uniform atomic_uint overflow;
layout(std430, binding = 1) writeonly buffer Out { vec4 items[]; };
void main() {
    uint i = atomicCounterIncrement(fragCount);   // returns value BEFORE increment
    if (i < items.length()) items[i] = vec4(gl_FragCoord.xy, 0, 1);
    else atomicCounterIncrement(overflow);
}
```

## Host
```c
GLuint acb; glCreateBuffers(1, &acb);
glNamedBufferStorage(acb, 8, NULL, GL_DYNAMIC_STORAGE_BIT);
GLuint zeros[2] = {0, 0};
glNamedBufferSubData(acb, 0, 8, zeros);          // reset every frame (or glClearNamedBufferData)
glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, acb);
draw();
glMemoryBarrier(GL_ATOMIC_COUNTER_BARRIER_BIT);   // before later shader atomic counter accesses
```
`GL_ATOMIC_COUNTER_BARRIER_BIT` covers later atomic counter accesses only. To read the counter
through another path use the bit for that consumer: `GL_BUFFER_UPDATE_BARRIER_BIT` for
`glCopyBufferSubData`, `glGetBufferSubData` and mapped reads, `GL_COMMAND_BARRIER_BIT` for data
sourced by `Draw*Indirect`.

## Atomic counters vs SSBO atomics
- Atomic counters need GL 4.2 and exist only in OpenGL GLSL: atomic counter types are not
  available when targeting Vulkan. Measure them against SSBO atomics on your target GPUs.
- SSBO `atomicAdd(buf.count, 1u)` is portable to the Vulkan dialect of GLSL, so prefer it for
  code you may port.

## Gotchas
- Limits are per stage: check `GL_MAX_FRAGMENT_ATOMIC_COUNTERS` and
  `GL_MAX_COMBINED_ATOMIC_COUNTERS` (stage versions such as `GL_MAX_VERTEX_ATOMIC_COUNTERS`
  exist too).
- `offset` must be a multiple of 4 (compile-time error otherwise), and two counters on the same
  binding may not share an offset. A counter without an explicit offset takes the binding's
  next offset, which advances by 4 per counter.
- A fragment-shader counter counts shader executions, not visible pixels: overdraw increments
  it more than once per pixel.

## Verify
- [ ] Read back the counter after a frame; overflow counter stays 0 at the expected scene load.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: the atomicCounter* built-ins in the GLSL 4.60 function list (Add, Subtract, Min, Max, And, Or, Xor, Exchange, CompSwap, Increment returning the prior value); atomic counters are not available when targeting Vulkan; offset must be a multiple of 4 and two counters may not share binding and offset; GL_ATOMIC_COUNTER_BARRIER_BIT, GL_BUFFER_UPDATE_BARRIER_BIT and GL_COMMAND_BARRIER_BIT semantics (glMemoryBarrier); limit names (glGet); GL 4.2 gate (gl.xml). Removed unconfirmed vendor, hardware and subgroup claims.
Method: documentation only; no commands were run.
