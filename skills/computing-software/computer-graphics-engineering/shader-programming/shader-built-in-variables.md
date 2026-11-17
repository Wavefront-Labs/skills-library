---
id: computing-software.computer-graphics-engineering.shader-programming.shader-built-in-variables
name: shader-built-in-variables
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, gl-fragcoord, gl-vertexindex, gl-instanceindex, sv-position, glsl, hlsl, built-in-variables]
level: practitioner
status: docs-checked
description: "Use shader built-ins correctly: gl_FragCoord/SV_Position conventions, gl_VertexIndex vs gl_VertexID, gl_InstanceIndex base offsets, front-facing, sample and invocation IDs."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#interfaces-builtin-variables", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_8.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader built-in variables

## 1. Fragment position
| API | Name | Origin | Pixel centre |
|---|---|---|---|
| GL | `gl_FragCoord` | bottom-left (default) | `.5` (e.g. 0.5, 0.5) |
| Vulkan GLSL | `gl_FragCoord` (SPIR-V `FragCoord`) | upper-left (assumed and required) | `.5` |
| D3D | `SV_Position` in PS | pixel location (x,y) in screen space | |
| WGSL | `@builtin(position)` | framebuffer grid with top-left at (0,0) | |

- `.z` is window-space depth; `.w` is `1/w` (GLSL: window-relative `(x, y, z, 1/w)`).
- Screen UV: `uv = gl_FragCoord.xy / resolution` gives centres at half-texel offsets, correct for
  `texelFetch(ivec2(gl_FragCoord.xy))`.
- GL code ported to Vulkan flips vertically; fix with a negative viewport height
  (a negative `VkViewport` height is allowed) rather than editing every shader.
- GL defaults to a lower-left origin with centres at half-pixel coordinates; redeclaring
  `layout(origin_upper_left, pixel_center_integer) in vec4 gl_FragCoord;` changes that (the pixel centre becomes (0.0, 0.0)).

## 2. Vertex and instance IDs
| GL | Vulkan GLSL | HLSL | Includes base? |
|---|---|---|---|
| `gl_VertexID` | `gl_VertexIndex` | `SV_VertexID` | GL: `glDrawElements` forms with a `basevertex` add it to the buffer index; Vulkan: **yes** (non-indexed: starts at `firstVertex`; indexed: index plus `vertexOffset`); HLSL: DXC maps `SV_VertexID` to `VertexIndex` (see its docs for the base-vertex option) |
| `gl_InstanceID` | `gl_InstanceIndex` | `SV_InstanceID` | Vulkan: **yes** (starts at `firstInstance`); GL: instance number of the instanced draw (`gl_BaseInstance` is separate); HLSL: DXC maps `SV_InstanceID` to `InstanceIndex`, or `InstanceIndex - BaseInstance` with `-fvk-support-nonzero-base-instance` |
| `gl_BaseVertex`, `gl_BaseInstance`, `gl_DrawID` | same | HLSL SM 6.8: `SV_StartVertexLocation`, `SV_StartInstanceLocation`; DXC maps them to `BaseVertex`/`BaseInstance` (needs `SPV_KHR_shader_draw_parameters`) | |

Getting this wrong is the classic bug when porting instanced/indirect rendering: per-instance data
indexed with `gl_InstanceIndex` in Vulkan already includes `firstInstance`; adding it again doubles it.
In D3D12, pass the base via a root constant or use `SV_StartInstanceLocation` (SM 6.8, reports `StartInstanceLocation`).

Fullscreen triangle without a vertex buffer:
```glsl
vec2 uv = vec2((gl_VertexIndex << 1) & 2, gl_VertexIndex & 2);
gl_Position = vec4(uv * 2.0 - 1.0, 0.0, 1.0);
```

## 3. Other common built-ins
- `gl_FrontFacing` / `SV_IsFrontFace`: depends on winding and the viewport flip; check after
  porting.
- `gl_SampleID`, `gl_SamplePosition` / `SV_SampleIndex`: any static use makes the whole fragment shader run per sample
  (cost x MSAA count).
- Writing `gl_Layer` from a vertex shader needs the `shaderOutputLayer` feature.
- `gl_ViewIndex` for multiview.
- Compute: `gl_GlobalInvocationID`, `gl_LocalInvocationIndex` / `SV_DispatchThreadID`,
  `SV_GroupIndex`.

## Gotchas
- `gl_VertexIndex`/`gl_InstanceIndex` exist only when targeting Vulkan; `gl_VertexID`/`gl_InstanceID` only when not.

## Verify
- [ ] Debug-visualise `gl_FragCoord.xy / res` and `gl_InstanceIndex` colour per instance after any port.

## Checked

Checked 2026-10-26 against GLSL 4.60 specification (OpenGL Registry), Vulkan-Docs interfaces/features/vertexpostproc chapters (main, 2026-10-23), DXC SPIR-V docs, DirectX-Specs HLSL Shader Model 6.8, WGSL spec. Confirmed: gl_FragCoord origin and pixel-centre rules and the Vulkan upper-left requirement; `(x, y, z, 1/w)`; gl_VertexIndex/gl_InstanceIndex semantics (firstVertex, vertexOffset, firstInstance) and that gl_VertexID/gl_InstanceID are absent when targeting Vulkan; gl_VertexID with basevertex (OpenGL reference page); gl_SampleID/gl_SamplePosition per-sample evaluation; `shaderOutputLayer`; DXC mappings for SV_VertexID/SV_InstanceID/SV_StartVertexLocation/SV_StartInstanceLocation; negative viewport height. Removed as unconfirmed: D3D half-pixel/D3D9 remark, gl_PrimitiveID, gl_PointSize and gl_SampleMaskIn remarks, driver-compatibility remark on origin_upper_left.

Method: documentation only; no commands were run.
