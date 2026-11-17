---
id: computing-software.computer-graphics-engineering.directx.dxr-raytraced-shadows
name: dxr-raytraced-shadows
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, raytraced-shadows, soft-shadows-rt, shadow-denoising]
level: advanced
status: docs-checked
description: "Implement ray-traced shadows: shadow ray setup from G-buffer, origin offsets, soft shadows by sampling light area/cone, 1 spp plus denoising, and cost controls."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/Raytracing.md", "https://github.com/NVIDIA-RTX/NRD"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-traced shadows

## Pass structure (hybrid renderer)
1. G-buffer rasterised as usual (depth, normals).
2. Compute/raygen pass, one thread per pixel (or half resolution): reconstruct world position
   from depth, trace one shadow ray per light (or per sampled light) with inline `RayQuery`.
3. Denoise the noisy visibility.
4. Lighting pass multiplies by visibility.

## Shadow ray
```hlsl
float3 P = ReconstructWorldPos(uv, depth);
float3 N = GBufferNormal(uv);
float3 origin = P + N * (0.001 + 0.0005 * length(P - CameraPos));   // offset against self-hit, scale with distance
float3 L = SampleSunCone(sunDir, sunAngularRadius, BlueNoise(pixel, frame));   // soft shadow
RayDesc r = { origin, 0.0, L, 1e4 };
RayQuery<RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH | RAY_FLAG_SKIP_PROCEDURAL_PRIMITIVES> q;
q.TraceRayInline(Scene, RAY_FLAG_NONE, SHADOW_CASTER_MASK, r);
q.Proceed();                                   // opaque-only: one Proceed resolves
float vis = q.CommittedStatus() == COMMITTED_NOTHING ? 1.0 : 0.0;
```
Point/spot/area lights: sample a point on the light's shape (sphere/disk/rect), `TMax` = distance
minus epsilon, direction normalised.

## Soft shadows
- Directional sun: sample a cone of the sun's angular radius; penumbra width then
  emerges naturally (contact hardening).
- Area lights: uniform or solid-angle sampling on the light shape.
- Few samples per pixel plus a denoiser is the usual real-time approach; NVIDIA NRD's SIGMA is a per-light
  shadow-only denoiser. Feed the denoiser hit distance / penumbra size where it requires them.

## Cost controls
- Skip rays for back-facing pixels (`dot(N, L) <= 0`): they're in shadow by shading anyway.
- Half-resolution tracing + upsample for distant pixels; tile classification to skip fully lit/
  fully shadowed tiles from a cheap shadow-map pre-pass.
- Use instance masks to exclude non-casters, and OPAQUE geometry flags.

## Gotchas
- Self-shadow acne from bad offsets: scale the origin offset with distance, or use a robust offset method
  such as the one in the book Ray Tracing Gems (not checked here).
- Skinned/animated meshes need BLAS refit every frame or shadows lag behind geometry.
- Alpha-tested casters need any-hit or the query loop handling candidates.

## Verify
- [ ] Shadows match a high-sample reference after denoising; no acne at grazing angles or far distances.

## Checked

Checked 2026-10-26 against the DirectX-Specs DXR functional spec (microsoft/DirectX-Specs, d3d/Raytracing.md, repository current to 2026-10-22) and the HLSL Shader Model 6.6 spec. Confirmed: RayQuery TraceRayInline with RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH and RAY_FLAG_SKIP_PROCEDURAL_PRIMITIVES available as ray flags, CommittedStatus returning COMMITTED_NOTHING, instance mask AND rule, NRD SIGMA is a per-light shadow denoiser. Removed: the 0.27 degree figure and the FidelityFX denoiser name. The Ray Tracing Gems offset reference is marked not checked (a book, not on the public docs); the shader offset constants in the snippet are illustrative tuning values, not documented values.
Method: documentation only; no commands were run.
