---
id: computing-software.computer-graphics-engineering.directx.d3d12-amplification-shader-meshlet-culling
name: d3d12-amplification-shader-meshlet-culling
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-advanced, amplification-culling, meshlet-cone-culling, dispatchmesh]
level: sme
status: docs-checked
description: "Cull meshlets in D3D12 amplification shaders: frustum, normal-cone and Hi-Z tests per meshlet, wave-compacted payloads and DispatchMesh sizing."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/MeshShader.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/directx-12-programming-guide", "https://github.com/zeux/meshoptimizer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Meshlet culling in amplification shaders

The amplification shader (AS) runs one thread per candidate meshlet, tests visibility, and
launches mesh shader groups only for survivors via `DispatchMesh`.

## Per-meshlet bounds (offline)
`meshopt_computeMeshletBounds` gives a bounding sphere and a normal cone (axis, cutoff, apex) per
meshlet. Store `{float4 sphere; float4 coneAxisCutoff; float4 coneApex;}` in a structured buffer.

## Amplification shader
```hlsl
struct Payload { uint meshletIndices[32]; };
groupshared Payload s_payload;

bool IsVisible(MeshletBounds b, float4x4 world, float scale) {
    float3 c = mul(float4(b.sphere.xyz, 1), world).xyz; float r = b.sphere.w * scale;
    [unroll] for (int i = 0; i < 6; ++i)                       // frustum planes in world space
        if (dot(float4(c, 1), Frustum.planes[i]) < -r) return false;
    float3 axis = normalize(mul(float4(b.coneAxis, 0), world).xyz);
    float3 apex = mul(float4(b.coneApex, 1), world).xyz;
    if (dot(normalize(apex - CameraPos), axis) >= b.coneCutoff) return false;   // all triangles backfacing
    return true;
}

[numthreads(32, 1, 1)]
void ASMain(uint gtid : SV_GroupThreadID, uint dtid : SV_DispatchThreadID) {
    bool visible = dtid < MeshletCount && IsVisible(Bounds[dtid], World, Scale);
    if (visible) {
        uint slot = WavePrefixCountBits(visible);              // compact survivors
        s_payload.meshletIndices[slot] = dtid;
    }
    uint count = WaveActiveCountBits(visible);
    DispatchMesh(count, 1, 1, s_payload);                      // exactly once per group, uniform
}
```
`WavePrefixCountBits` and `WaveActiveCountBits` count within one wave, so this compaction is only correct when the wave size
is at least the 32-thread group size; otherwise compact through groupshared with `InterlockedAdd`.

## Hi-Z occlusion (two-phase)
Project the sphere to screen, pick the Hi-Z mip covering its rect, compare nearest depth with the
pyramid (built from last frame's depth reprojected or this frame's first-phase depth). Meshlets
rejected in phase 1 are retested after rendering phase-1 survivors (avoids false culling).

## Sizing
- Amplification shader payload must not exceed 16k bytes, and it counts against groupshared memory (limits 28k for mesh
  shaders and 32k for amplification shaders per the spec).
- `DispatchMesh` thread group counts must satisfy `x*y*z <= 2^22`.
- `[numthreads]` is mandatory with `X*Y*Z <= 128` for both stages.
- Choose meshlet size by profiling on your target GPUs.

## Gotchas
- `DispatchMesh` can only be called once per amplification shader, and must be reached by the whole group with uniform arguments.
- Cone culling requires a conservative cutoff (meshopt computes it); per-instance non-uniform
  scale invalidates cones: disable cone test for those instances.

## Verify
- [ ] Pipeline statistics (`D3D12_QUERY_DATA_PIPELINE_STATISTICS1` AS/MS invocations) drop sharply when facing away/occluded; identical image vs. no culling.

## Checked

Checked 2026-10-26 against the DirectX-Specs Mesh Shader spec (repository current to 2026-10-22). Confirmed: DispatchMesh intrinsic launches mesh groups with a payload, payload limit 16k, groupshared limits 28k/32k, 2^22 group-count limit, numthreads X*Y*Z <= 128, DispatchMesh callable once per shader. Removed: vendor meshlet-size guidance (64/124 per NVIDIA, AMD preferences) that the spec does not state. meshopt_computeMeshletBounds and the cone test dot(normalize(cone_apex - camera_position), cone_axis) >= cone_cutoff match the meshoptimizer README (zeux/meshoptimizer, repository current to 2026-10-14).
Method: documentation only; no commands were run.
