---
id: computing-software.computer-graphics-engineering.directx.hlsl-semantics-and-system-values
name: hlsl-semantics-and-system-values
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, hlsl-semantics, system-value-semantics, sv-position]
level: practitioner
status: docs-checked
description: "Use HLSL semantics and SV_ system values correctly: stage linkage, SV_Position in pixel shaders, SV_VertexID/InstanceID, SV_Target outputs, interpolation modifiers."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-struct", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_8.md", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL semantics and system values

## User semantics link stages
```hlsl
struct VSIn  { float3 pos : POSITION; float3 nrm : NORMAL; float2 uv : TEXCOORD0; };
struct VSOut {
    float4 pos : SV_Position;             // clip-space in VS, pixel coords in PS
    float3 nrm : NORMAL;
    float2 uv  : TEXCOORD0;
    nointerpolation uint matId : MATERIAL; // flat
};
```
VS output and PS input are matched by semantic name+index (and register packing), not by struct
member order. Input layout `SemanticName/SemanticIndex` must match VS input semantics.
For SPIR-V (DXC `-spirv`), `Location` numbers are assigned sequentially in declaration order by
default (`-fvk-stage-io-order=decl`; `alpha` sorts alphabetically) unless you use
`[[vk::location(n)]]`; keep VS outputs and PS inputs in the same order or annotate.

## Key system values
| Semantic | Stage | Meaning |
|---|---|---|
| `SV_Position` | VS out / PS in | VS: clip-space position; PS: pixel location in screen space |
| `SV_VertexID`, `SV_InstanceID` | VS in | vertex and instance index |
| `SV_StartInstanceLocation`/`SV_StartVertexLocation` | VS in (SM 6.8) | base values from the draw call (`StartInstanceLocation`; `StartVertexLocation` or `BaseVertexLocation`) |
| `SV_Target0..7` | PS out | render target outputs |
| `SV_Depth`, `SV_DepthGreaterEqual`, `SV_DepthLessEqual` | PS out | depth output |
| `SV_IsFrontFace` | PS in | facing |
| `SV_SampleIndex`, `SV_Coverage` | PS | per-sample shading, coverage mask |
| `SV_PrimitiveID` | GS/PS | primitive index |
| `SV_RenderTargetArrayIndex`, `SV_ViewportArrayIndex` | VS/GS out | layered rendering |
| `SV_DispatchThreadID`, `SV_GroupID`, `SV_GroupThreadID`, `SV_GroupIndex` | CS | thread ids |
| `SV_ClipDistance0`, `SV_CullDistance0` | VS out | user clip planes |

## Interpolation modifiers
`linear` (default), `nointerpolation`, `noperspective`, `centroid` (interpolates within the covered
area of the pixel; must be combined with `linear` or `noperspective`), `sample` (SM 4.1+; interpolates
at the sample location and makes the pixel shader run per sample).

## Gotchas
- To read the draw's start instance or vertex in the shader use the SM 6.8 `SV_StartInstanceLocation`
  and `SV_StartVertexLocation` semantics, or pass the base as a root constant on older shader models.

## Verify
- [ ] PSO creation succeeds without "linkage" errors; PIX shader debugging shows expected SV values.

## Checked

2026-10-26. Checked against the Microsoft Learn HLSL semantics list, the struct interpolation-modifier table, the DirectX-Specs
Shader Model 6.8 document (SV_StartVertexLocation, SV_StartInstanceLocation) and docs/SPIR-V.rst (location assignment
order, -fvk-stage-io-order) (win32, DirectX-Specs and DirectXShaderCompiler repositories, commits to 2026-10).
Confirmed: the semantic names listed, centroid/sample modifier behaviour, SM 6.8 start-location semantics, SPIR-V
location order. Removed the unconfirmed claims about SV_InstanceID excluding StartInstanceLocation, early-Z behaviour,
pixel-centre offset, SV_ViewID and unused interpolators.
Method: documentation only; no commands were run.
