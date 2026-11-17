---
id: computing-software.computer-graphics-engineering.opengl.opengl-glsl-atomics-and-memory-qualifiers
name: opengl-glsl-atomics-and-memory-qualifiers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-compute, glsl-atomics, coherent-qualifier, imageatomic, memory-model]
level: advanced
status: docs-checked
description: "Use GLSL buffer/image atomics and memory qualifiers (coherent, volatile, restrict, readonly) correctly for cross-invocation communication in OpenGL."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL/extensions/NV/NV_shader_atomic_float.txt", "https://registry.khronos.org/OpenGL/extensions/NV/NV_shader_atomic_int64.txt", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GLSL atomics and memory qualifiers

## Atomic functions
| On | Functions |
|---|---|
| SSBO/shared `uint`/`int` | `atomicAdd, atomicMin, atomicMax, atomicAnd, atomicOr, atomicXor, atomicExchange, atomicCompSwap` |
| Images (`r32ui`, `r32i`, `r32f` exchange only) | `imageAtomicAdd`, `imageAtomicMax`, `imageAtomicCompSwap`, ... |
| Floats | not in GLSL 4.60 (`int`/`uint` only); `atomicAdd` on `float` comes from `GL_NV_shader_atomic_float` |
| 64-bit | not in GLSL 4.60; `GL_NV_shader_atomic_int64` adds 64-bit atomics |
All return the **previous** value.

## Memory qualifiers
| Qualifier | Meaning |
|---|---|
| `coherent` | values written are reflected in subsequent coherent reads by other invocations; without it the implementation may cache reads and writes |
| `volatile` | memory is treated as if it can change at any time: every read re-fetches it |
| `restrict` | promise no aliasing with other bound resources: lets the compiler reorder/cache |
| `readonly` / `writeonly` | access restriction |

```glsl
layout(std430, binding = 0) coherent buffer Heads { uint head[]; };
layout(r32ui, binding = 0) uniform coherent uimage2D uHeadPtr;
layout(std430, binding = 1) restrict readonly buffer Input { vec4 data[]; };
```

## Ordering inside a shader
Atomics are atomic but not ordering fences. To publish data then a flag:
```glsl
nodes[idx] = node;              // payload write
memoryBarrierBuffer();          // order payload before the flag (within this invocation's view)
atomicExchange(ready[idx], 1u);
```
Readers in other invocations must also see the payload: mark the buffer `coherent`.

## Patterns
- **Per-pixel linked list (OIT):** `uint old = imageAtomicExchange(uHeadPtr, px, newNode);`
  then `nodes[newNode].next = old;`.
- **Min depth per tile:** `atomicMin(tileMinDepth[t], floatBitsToUint(depth))` works for
  positive floats because their bit patterns sort like integers.
- **Packed max with payload:** pack `(depthBits << 32 | id)` into 64-bit and `atomicMax` where
  int64 atomics exist; otherwise two-pass.

## Gotchas
- Qualifiers apply to image variables, buffer variables and shader storage blocks only; they are an error on other
  declarations.
- Host-side visibility still needs `glMemoryBarrier` between passes; qualifiers only cover
  shader-to-shader visibility within the rules above.

## Verify
- [ ] Results deterministic across runs (or bounded, for order-dependent appends); no hangs under stress tests.

## Checked

Date: 2026-10-26. Documentation: GLSL 4.60 spec (section on atomic memory functions, image atomics and memory qualifiers), NV_shader_atomic_float and NV_shader_atomic_int64 extension texts, OpenGL 4.6 core spec. Confirmed: `atomicAdd/Min/Max/And/Or/Xor/Exchange/CompSwap` on `int`/`uint` buffer or shared variables; image atomics need `r32i`/`r32ui` (and `r32f` for `imageAtomicExchange` only); atomics return the original value; meanings of `coherent`, `volatile`, `restrict`; `memoryBarrierBuffer()` exists; float and int64 atomics are extension features. Removed: `EXT_shader_atomic_float` (not in the GL registry), `volatile implies coherent`, spinlock/forward-progress and subgroup-aggregation remarks (no documentation read).

Method: documentation only; no commands were run.
