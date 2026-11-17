---
id: computing-software.computer-graphics-engineering.opengl.opengl-packed-vertex-formats
name: opengl-packed-vertex-formats
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vertex-specification, packed-vertex-formats, int-2-10-10-10, half-float-vertices, vertex-compression]
level: advanced
status: docs-checked
description: "Shrink OpenGL vertex buffers with normalized, half-float and 2_10_10_10_REV attribute formats, and pick glVertexAttribFormat vs IFormat correctly."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glVertexAttribFormat.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packed vertex attribute formats

A naive vertex (`vec3 pos, vec3 normal, vec4 tangent, vec2 uv` as floats) is 48 bytes. Packing
gets it to 20-24 bytes with little visible loss (check by eye), cutting the bytes fetched per vertex by more than half.

## Format table
| Attribute | Packed format | Call | Bytes |
|---|---|---|---|
| Position (local, quantised) | `GL_UNSIGNED_SHORT` normalized x3 (+pad) | `glVertexArrayAttribFormat(vao, 0, 4, GL_UNSIGNED_SHORT, GL_TRUE, off)` | 8 |
| Position (full float) | `GL_FLOAT` x3 | `..., 3, GL_FLOAT, GL_FALSE, ...` | 12 |
| Normal | `GL_INT_2_10_10_10_REV` normalized | `..., 4, GL_INT_2_10_10_10_REV, GL_TRUE, ...` | 4 |
| Tangent + sign | `GL_INT_2_10_10_10_REV` (w = 2-bit sign) | same | 4 |
| UV | `GL_HALF_FLOAT` x2 | `..., 2, GL_HALF_FLOAT, GL_FALSE, ...` | 4 |
| Colour | `GL_UNSIGNED_BYTE` x4 normalized | `..., 4, GL_UNSIGNED_BYTE, GL_TRUE, ...` | 4 |
| Bone indices | `GL_UNSIGNED_BYTE` x4 integer | `glVertexArrayAttribIFormat(vao, 5, 4, GL_UNSIGNED_BYTE, off)` | 4 |

## Format vs IFormat vs LFormat
- `glVertexAttribFormat` converts to float in the shader (`in vec4`), normalising if asked.
- `glVertexAttribIFormat` keeps integers (`in uvec4 boneIdx`). Using `Format` with `GL_FALSE`
  for indices converts them to floats; pair integer shader inputs with `IFormat`.
- `glVertexAttribLFormat` for `double` inputs only.

## Packing 2_10_10_10 on the CPU
```c
static uint32_t pack_snorm1010102(float x, float y, float z, int w) {
    auto q = [](float v){ int i = (int)lroundf(fminf(fmaxf(v,-1.f),1.f) * 511.f); return (uint32_t)i & 0x3FF; };
    return q(x) | (q(y) << 10) | (q(z) << 20) | ((uint32_t)(w & 0x3) << 30);
}
```
Signed normalised conversion is `max(c / 511, -1)` for the 10-bit fields (spec equation 2.2), so -512 and -511
both map to -1. Re-normalise normals in the shader.

## Quantised positions
Store positions as unorm16 relative to the mesh AABB and fold the dequantisation
(`aabbMin + p * aabbExtent`) into the model matrix: zero shader cost. 16 bits over a 10 m
object gives 0.15 mm steps.

## Gotchas
- `GL_INT_2_10_10_10_REV` requires size 4 (or `GL_BGRA`); size 3 is `GL_INVALID_OPERATION`.
- `GL_HALF_FLOAT` has a 10-bit mantissa: the step is 1/1024 in [1, 2) and 1/8 in [128, 256), so tiled UVs in the
  hundreds need floats.

## Verify
- [ ] Shaded result identical by eye to the float version (flip between them).
- [ ] Vertex stride reported in RenderDoc matches the packed layout.

## Checked

Date: 2026-10-26. Documentation: gl4 reference page for glVertexAttribFormat and OpenGL 4.6 core spec (5 May 2022, section 2.3.5 equations 2.1 and 2.2). Confirmed: `GL_INT_2_10_10_10_REV` and `GL_UNSIGNED_INT_2_10_10_10_REV` need size 4 (or `GL_BGRA`), otherwise `GL_INVALID_OPERATION`; `glVertexArrayAttribFormat/IFormat/LFormat` are 4.5; `LFormat` is for doubles; signed normalised conversion `max(c/(2^(b-1)-1), -1)`; 48-byte versus 20-byte vertex sizes and the 0.15 mm step (10 m / 65535) are computed; half-float steps follow the 10-bit mantissa. Removed: pre-4.2 conversion formula, alignment-performance claim, bandwidth-halving claim.

Method: documentation only; no commands were run.
