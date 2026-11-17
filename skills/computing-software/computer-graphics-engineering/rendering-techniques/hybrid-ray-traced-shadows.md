---
id: computing-software.computer-graphics-engineering.rendering-techniques.hybrid-ray-traced-shadows
name: hybrid-ray-traced-shadows
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, shadows, hybrid-shadows, ray-traced-shadows, ray-query, dxr, shadow-denoising, area-light-shadows]
level: advanced
status: docs-checked
description: "Inline ray queries for shadow rays in DXR, and how to feed the NVIDIA NRD SIGMA and AMD FidelityFX shadow denoisers, including the ray-flag trap with hit distance."
sources:
  - https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md
  - https://github.com/NVIDIA-RTX/NRD
  - https://gpuopen.com/fidelityfx-denoiser/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-traced and hybrid shadows

## 1. Shadow ray with an inline ray query (DXR 1.1)
```hlsl
RayQuery<RAY_FLAG_NONE> q;
RayDesc r; r.Origin = worldPos + N * bias; r.Direction = L; r.TMin = 0.0; r.TMax = distToLight;
q.TraceRayInline(sceneTLAS, RAY_FLAG_NONE, 0xFF, r);
while (q.Proceed()) {
    if (q.CandidateType() == CANDIDATE_NON_OPAQUE_TRIANGLE) {
        // evaluate alpha for q.CandidateInstanceIndex(), q.CandidatePrimitiveIndex(), q.CandidateTriangleBarycentrics()
        // if opaque: q.CommitNonOpaqueTriangleHit();
    }
}
float vis = (q.CommittedStatus() == COMMITTED_NOTHING) ? 1.0 : 0.0;
```
- `RayQuery<RAY_FLAGS>` takes compile-time ray flags; `TraceRayInline` takes a dynamic ray flags argument and the two are OR'd. The `Proceed()` loop is where traversal runs; `CandidateType()` reports what needs shader work (non-opaque triangle or procedural primitive), and `CommitNonOpaqueTriangleHit()` commits a non-opaque candidate you decided is opaque.
- `RAY_FLAG_SKIP_CLOSEST_HIT_SHADER` is not allowed for `RayQuery::TraceRayInline()` or in the `RayQuery` template parameter (it makes no sense there), so do not copy the flag combination used in the spec's `TraceRay()` example.
- A `RayQuery` object has an opaque, implementation-specific size and may cost relatively high register storage per live object, which can limit shader occupancy. Keep few live queries.
- `RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH` stops traversal at any hit (not necessarily the closest). It suits binary visibility but see the denoiser warning below.

## 2. Denoising soft shadows
- **NVIDIA NRD SIGMA**: per-light, shadow-only denoiser for shadows from an infinite light (sun, moon) or a local light (omni, spot); `SIGMA_SHADOW_TRANSLUCENCY` handles translucent shadows. It needs the distance to the occluder. Cast the visibility ray from the point of interest toward the light (not from the light), "hit" means an occluder is hit, and do not use `ACCEPT_FIRST_HIT_AND_END_SEARCH` to optimise tracing: it can return wrong, very long hit distances from random distant occluders.
- NRD advises blue noise for SIGMA to minimise shimmering and flicker, best with a pattern limited to 4-8 animated frames or a static one. For several lights apply SIGMA per light; setting `maxStabilizedFrameNum` to 0 disables temporal history, giving light-count-independent memory and no per-light history buffers. Use the SIGMA front-end pack and back-end unpack functions from NRD's HLSL headers.
- **AMD FidelityFX Shadow Denoiser**: spatio-temporal denoiser for a shadow mask made by tracing jittered rays toward a single light source; it includes a tile classifier that skips areas without spatial variance and analyses the local neighbourhood to counter ghosting. Supports DirectX 12 and Vulkan.
- AMD's FidelityFX Hybrid Shadows sample demonstrates combining ray-traced shadows with rasterised shadow maps; read it for a concrete hybrid scheme rather than relying on rules of thumb.

## Checked
Confirmed on 2026-11-08 against the DirectX raytracing functional spec (RayQuery, TraceRayInline, CandidateType, CommittedStatus, ray flag restrictions), the NVIDIA NRD README (SIGMA description and usage notes) and the AMD GPUOpen FidelityFX Denoiser page. Removed because none of the readable pages state them: the Control blog post (404), penumbra and cone-angle figures, ray-count budgets, near-RT/far-map classification rules, self-intersection offset advice, BLAS refit and motion-vector notes. Corrected: the old example combined `RAY_FLAG_SKIP_CLOSEST_HIT_SHADER` with a RayQuery, which the spec disallows.
Method: docs-only read of cited pages, 2026-11-08
