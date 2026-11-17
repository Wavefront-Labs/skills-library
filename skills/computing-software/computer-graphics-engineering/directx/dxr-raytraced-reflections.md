---
id: computing-software.computer-graphics-engineering.directx.dxr-raytraced-reflections
name: dxr-raytraced-reflections
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, raytraced-reflections, glossy-reflections, hybrid-reflections]
level: sme
status: docs-checked
description: "Build ray-traced reflections: GGX importance-sampled rays from the G-buffer, hit shading with simplified materials, SSR hybrid, roughness cutoffs and denoising."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://github.com/NVIDIA-RTX/NRD"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-traced reflections

## Pipeline
1. **Classify** pixels: roughness above a cutoff you tune -> use prefiltered probes/IBL only;
   below -> trace. Optionally try SSR first and trace only where SSR fails (off-screen, occluded).
2. **Generate rays**: mirror direction for very smooth surfaces; GGX visible-normal (VNDF)
   importance sampling for glossy, driven by blue noise per pixel per frame.
3. **Trace** with `TraceRay` (shader tables for material variety) or inline RayQuery + a material
   evaluation in compute.
4. **Shade hits** cheaply: albedo/normal from vertex data and material textures at a fixed low mip,
   direct lighting from the sun (with a shadow ray or a shadow map lookup), plus probe-based
   indirect. Misses sample the sky / reflection probe.
5. **Denoise** (temporal + spatial; for example NRD REBLUR or RELAX) using hit distance,
   roughness, normals and motion vectors.
6. **Composite** with split-sum specular (BRDF LUT x reflected radiance).

## Ray generation snippet
```hlsl
float3 V = normalize(CameraPos - P);
float2 u = BlueNoise2D(pixel, frameIndex);
float3 H = SampleGGXVNDF(V, N, roughness * roughness, u);     // alpha = roughness^2
float3 R = reflect(-V, H);
if (dot(R, Ngeom) <= 0) R = reflect(-V, N);                    // below horizon: fall back
RayDesc ray = { OffsetRayOrigin(P, Ngeom), 0.0, R, MaxReflectionDistance };
```

## Performance levers
- Trace at reduced resolution (checkerboard) and reconstruct; budget rays per pixel.
- Shorter `TMax` for rough surfaces; fall back to probes beyond it.
- Simplified hit shaders: no normal maps, no complex layered materials, lower texture mips.
- Ray binning/sorting by direction, or SER (`HitObject` plus `MaybeReorderThread`, Shader Model 6.9) for coherence.

## Gotchas
- Reflection of the first-person weapon/character: exclude via instance masks or render them
  separately; mismatched LODs between raster and BLAS cause visible differences.
- Temporal reprojection of reflections needs the reflected surface's motion (virtual position), not
  the mirror's; use hit distance-based reprojection as in denoiser docs.
- Transparent surfaces need special handling (separate pass or no RT reflections).

## Verify
- [ ] Compare against a path-traced reference at several roughness levels; the pass stays within your frame budget.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: RayDesc usage with TMax, TraceRay and inline RayQuery both available, SER types and MaybeReorderThread in SM 6.9 (DXR spec), NRD provides REBLUR and RELAX (NVIDIA-RTX/NRD README). The sampling, classification and compositing steps are rendering technique guidance rather than API facts and were not checked against a standard. Removed: roughness 0.6, 3 ms budget, FidelityFX denoiser name, 'half resolution, 1 ray per pixel maximum' prescriptions.
Method: documentation only; no commands were run.
