---
id: computing-software.computer-graphics-engineering.directx.dxr-any-hit-and-alpha-tested-geometry
name: dxr-any-hit-and-alpha-tested-geometry
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, any-hit-shader, alpha-tested-rt, ignorehit]
level: advanced
status: docs-checked
description: "Handle alpha-tested foliage in DXR: any-hit shaders with IgnoreHit, opaque geometry flags, texture LOD in hit shaders, inline RayQuery candidates and opacity micromaps."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_9.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Any-hit shaders and alpha-tested geometry

## Mark geometry correctly
- Opaque geometry: `D3D12_RAYTRACING_GEOMETRY_FLAG_OPAQUE` in the BLAS geometry desc. Any-hit shaders are not invoked for
  opaque geometry. Mark as much geometry opaque as you can.
- Alpha-tested geometry: no OPAQUE flag, and a hit group with an any-hit shader.
- `D3D12_RAYTRACING_GEOMETRY_FLAG_NO_DUPLICATE_ANYHIT_INVOCATION` if your any-hit has side effects (counting); otherwise leave it off.

## Any-hit shader
```hlsl
[shader("anyhit")]
void AlphaTestAnyHit(inout ShadowPayload p, BuiltInTriangleIntersectionAttributes a) {
    MaterialData m = Materials[InstanceID()];
    float2 uv = InterpolateUV(PrimitiveIndex(), a.barycentrics);
    float alpha = Textures[m.alphaTex].SampleLevel(PointOrLinear, uv, 0).a;   // explicit LOD: raytracing shaders have no 2x2 derivatives
    if (alpha < m.alphaCutoff) IgnoreHit();       // continue traversal as if no hit
    // else accept: falls through (or AcceptHitAndEndSearch() for shadow rays)
}
```
For shadow rays use `AcceptHitAndEndSearch()` after a passing alpha test: any opaque hit is enough.

## Texture LOD in hit shaders
Raytracing shaders have no 2x2-invocation derivatives, so use `SampleLevel` or `SampleGrad` with a LOD or gradients
you compute yourself (for example from hit distance and UV density).

## Inline ray tracing (RayQuery)
```hlsl
RayQuery<RAY_FLAG_NONE> q;
q.TraceRayInline(scene, RAY_FLAG_NONE, 0xFF, ray);
while (q.Proceed()) {
    if (q.CandidateType() == CANDIDATE_NON_OPAQUE_TRIANGLE && AlphaPasses(q.CandidateInstanceID(),
            q.CandidatePrimitiveIndex(), q.CandidateTriangleBarycentrics()))
        q.CommitNonOpaqueTriangleHit();
}
bool hit = q.CommittedStatus() == COMMITTED_TRIANGLE_HIT;
```

## Opacity micromaps
Opacity micromaps (DXR Tier 1.2, Shader Model 6.9, enabled with `RAYTRACING_PIPELINE_FLAG_ALLOW_OPACITY_MICROMAPS`)
classify micro-triangles as opaque or transparent (or unknown) so traversal can resolve hits as miss or hit
without invoking an any-hit shader. See the dedicated SER/OMM skill.

## Gotchas
- Any-hit may be invoked in any order, and more than once for the same triangle unless `NO_DUPLICATE_ANYHIT_INVOCATION` is set; never assume closest-first.
- Two-sided foliage: also set instance `TRIANGLE_CULL_DISABLE`.

## Verify
- [ ] Shadows of leaves show holes matching alpha; opaque BLASes are marked opaque so any-hit is not invoked for them.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: GEOMETRY_FLAG_OPAQUE and NO_DUPLICATE_ANYHIT_INVOCATION semantics, IgnoreHit and AcceptHitAndEndSearch exist, RayQuery CANDIDATE_NON_OPAQUE_TRIANGLE / CommitNonOpaqueTriangleHit / COMMITTED_TRIANGLE_HIT, instance flag TRIANGLE_CULL_DISABLE, no 2x2 derivatives in raytracing shaders, OMM requires Tier 1.2 and SM 6.9 with RAYTRACING_PIPELINE_FLAG_ALLOW_OPACITY_MICROMAPS. Removed: the RTG2 ray-cone paper citation, VK_EXT name, and GPU-generation speed claim.
Method: documentation only; no commands were run.
