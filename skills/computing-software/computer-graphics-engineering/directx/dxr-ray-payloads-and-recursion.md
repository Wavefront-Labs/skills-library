---
id: computing-software.computer-graphics-engineering.directx.dxr-ray-payloads-and-recursion
name: dxr-ray-payloads-and-recursion
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, ray-payload, recursion-depth, payload-access-qualifiers]
level: advanced
status: docs-checked
description: "Design DXR ray payloads and attributes: size limits, payload access qualifiers (SM 6.6+), MaxTraceRecursionDepth, and iterative loops instead of recursion."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_6.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray payloads and recursion

## Payload
```hlsl
struct [raypayload] PrimaryPayload {
    float3 radiance   : read(caller) : write(closesthit, miss);
    float  hitT       : read(caller) : write(closesthit, miss);
    uint   rngState   : read(closesthit, caller) : write(caller, closesthit);
    uint   depth      : read(closesthit) : write(caller);
};
```
Payload access qualifiers (PAQs) arrived with SM 6.6: they are opt-in with DXC's `-enable-payload-qualifiers` on
SM 6.6 and on by default from SM 6.7 (`-disable-payload-qualifiers` opts out). They tell the compiler which stages
read or write each field, which can reduce register pressure and avoid spilling payload state to memory.
A payload struct must carry the `[raypayload]` attribute. Keep payloads small.

Pipeline config:
```cpp
D3D12_RAYTRACING_SHADER_CONFIG sc = { sizeof(PrimaryPayload) /*MaxPayloadSizeInBytes*/,
                                      sizeof(BuiltInTriangleIntersectionAttributes) /*8 bytes*/ };
D3D12_RAYTRACING_PIPELINE_CONFIG pc = { 1 /*MaxTraceRecursionDepth*/ };
```
`MaxPayloadSizeInBytes` must cover the largest payload across ray types in the pipeline (or use separate pipelines);
the field is ignored for payloads that use PAQs.

## Recursion depth
`MaxTraceRecursionDepth` (0 to 31, ray generation is depth 0) bounds nested `TraceRay` calls from closest-hit/miss;
the spec advises the lowest limit you need. Write path tracers as **loops in the ray generation shader**:
```hlsl
for (uint bounce = 0; bounce < MaxBounces; ++bounce) {
    TraceRay(scene, flags, 0xFF, 0, 2, 0, ray, payload);      // closest hit returns next ray in payload
    if (payload.done) break;
    throughput *= payload.attenuation; ray.Origin = payload.nextOrigin; ray.Direction = payload.nextDir;
}
```
Closest-hit then only evaluates the material and samples a direction; no nested traces except a
shadow ray (depth 2) if done there. A `TraceRay` at the declared maximum depth puts the device into the removed state.

## Attributes
Triangles: `BuiltInTriangleIntersectionAttributes` (barycentrics). Procedural geometry uses custom attributes from
intersection shaders, at most `D3D12_RAYTRACING_MAX_ATTRIBUTE_SIZE_IN_BYTES` (32 bytes).

## Gotchas
- Shadow rays should use a tiny payload (one bool/float) and `RAY_FLAG_SKIP_CLOSEST_HIT_SHADER |
  ACCEPT_FIRST_HIT_AND_END_SEARCH` with a miss shader setting "lit".
- Stack size: query `GetShaderStackSize` per shader and set `SetPipelineStackSize` explicitly for
  extreme cases; the spec describes how to compute the size from the recursion depth.

## Verify
- [ ] No device removal at max bounce count; path tracer output identical between recursive and loop versions.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: PAQ availability (SM 6.6 opt-in via -enable-payload-qualifiers, default from SM 6.7, -disable-payload-qualifiers), [raypayload] attribute and the read(...)/write(...) field syntax, MaxPayloadSizeInBytes ignored with PAQs, recursion depth 0-31 with device removal at the limit, 32-byte attribute limit, GetShaderStackSize and SetPipelineStackSize. Removed: the claim that the default stack size assumes worst-case recursion for loops and profiler-specific register-count checks.
Method: documentation only; no commands were run.
