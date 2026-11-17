---
id: computing-software.computer-graphics-engineering.shader-programming.lens-flares-and-god-rays
name: lens-flares-and-god-rays
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, lens-flare, god-rays, light-shafts, volumetric-light-scattering, bloom, occlusion-query]
level: practitioner
status: draft
description: "Render lens flares and god rays: sprite-based flares with occlusion queries, screen-space ghost flares from bright pixels, and radial-blur light shafts from an occlusion buffer."
sources: ["https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-13-volumetric-light-scattering-post-process", "https://john-chapman.github.io/2017/11/05/pseudo-lens-flare.html", "https://docs.unrealengine.com/5.3/en-US/lens-flare-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lens flares and god rays

## 1. Sprite flares (sun, lamps)
- Project the light to screen; place flare elements along the line from the light through the
  screen centre at authored offsets (`pos = light + (center - light) * t_i`).
- Visibility: GPU occlusion query of a small quad at the light, or sample the depth buffer in a
  small disc around the light in a compute/vertex shader and average. Smooth over a few frames.
- Fade by visibility and by distance from the screen edge.

## 2. Screen-space ghost flares (Chapman)
From a downsampled, thresholded bright buffer:
```glsl
vec2 uv = 1.0 - texcoord;                         // flip about centre
vec2 ghostVec = (vec2(0.5) - uv) * ghostDispersal;
vec3 result = vec3(0);
for (int i = 0; i < NUM_GHOSTS; i++) {
    vec2 off = fract(uv + ghostVec * float(i));
    float w = pow(1.0 - length(vec2(0.5) - off) / 0.707, 10.0);  // favour centre
    result += texture(bright, off).rgb * w;
}
// halo: sample along normalize(ghostVec) * haloWidth; tint with a radial lens colour LUT
```
Then blur, multiply by a lens dirt texture and a starburst rotated by camera orientation, add to
the HDR image before tonemapping.

## 3. God rays (GPU Gems 3 ch13, Mitchell)
1. Render an occlusion buffer: sky/light bright, all geometry black (half-res is fine).
2. Radial blur toward the light's screen position:
```glsl
vec2 delta = (uv - lightScreenPos) * density / float(NUM_SAMPLES);
float illum = 1.0; vec3 color = texture(occl, uv).rgb;
for (int i = 0; i < NUM_SAMPLES; i++) {
    uv -= delta;
    color += texture(occl, uv).rgb * illum * weight;
    illum *= decay;                        // decay ~0.95-0.98
}
color *= exposure;
```
3. Add to the scene. Fade out when the light is behind the camera or off-screen.

For physically correct shafts with any light direction, use froxel volumetric fog instead.

## Gotchas
- Screen-space methods vanish when the source leaves the screen; fade gracefully.
- Radial blur with few samples bands; jitter the start offset per pixel with blue noise and let TAA
  resolve.
- Flares are an aesthetic choice; keep intensity tied to exposure so they don't bloom out at night.

## Verify
- [ ] Flares fade correctly when the light is occluded by geometry.
- [ ] God rays stable as the camera moves (no banding, no popping at screen edges).
