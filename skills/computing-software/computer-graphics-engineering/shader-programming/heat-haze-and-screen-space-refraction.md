---
id: computing-software.computer-graphics-engineering.shader-programming.heat-haze-and-screen-space-refraction
name: heat-haze-and-screen-space-refraction
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shading-effects, heat-haze, screen-space-refraction, distortion, grab-pass, scene-color, post-processing]
level: practitioner
status: draft
description: "Implement heat haze and screen-space refraction: distortion pass from scene colour copy, normal-driven UV offsets, depth-masking to stop foreground leaking, and cost control."
sources: ["https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/universalrp-asset.html", "https://docs.unrealengine.com/5.3/en-US/refraction-using-pixel-normal-offset-in-unreal-engine/", "https://developer.nvidia.com/gpugems/gpugems2/part-ii-shading-lighting-and-shadows/chapter-19-generic-refraction-simulation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screen-space refraction and heat haze

## 1. Mechanism
1. Render opaques.
2. Copy the colour buffer (Unity "Opaque Texture", UE "Scene Color", Godot `hint_screen_texture`).
3. Draw distortion objects (heat haze cards, glass, water) sampling the copy at offset UVs.

```glsl
vec2 screenUV = gl_FragCoord.xy / resolution;
vec2 n = texture(distortNormal, uv * 2.0 + vec2(0, time * 0.5)).xy * 2.0 - 1.0;
vec2 offset = n * strength * fade;            // strength in UV units, ~0.005-0.02
vec3 col = texture(sceneColor, screenUV + offset).rgb;
```

## 2. Fix foreground leaking
Objects in front of the distorter must not be pulled into it. Check the depth at the offset UV:
```glsl
float sceneZ = linearDepth(texture(depthTex, screenUV + offset).r);
if (sceneZ < fragLinearZ) offset = vec2(0.0);   // sample would come from in front; cancel
```
Or scale offset by `saturate((sceneZ - fragZ) / falloff)` for a smooth version.

## 3. Strength scaling
- Divide offset by view depth so distant haze distorts less (`offset /= max(viewZ, 1.0)` scaled).
- Fade at screen edges to avoid sampling outside (clamp UVs or fade strength near borders).
- Heat haze: fade by distance from the heat source and with a soft particle depth fade.

## 4. Glass-like refraction
Use the surface normal in view space: `offset = normalView.xy * ior_strength * thickness`. This is
an approximation (no real ray bending). Chromatic dispersion: sample R, G, B at slightly different
offsets (3 fetches).

## Gotchas
- The colour copy excludes other transparents drawn after it; refraction through two glass panes
  shows only opaques. Accept or add a second copy.
- Copying full-res HDR colour every frame costs bandwidth; use a half-res copy for haze (blurry
  anyway), or render distortion vectors into a buffer and apply once in post.
- On tilers the copy forces a render pass break; batch all distortion objects into one pass.

## Verify
- [ ] Foreground objects never appear inside distorted regions.
- [ ] No sampling artefacts at screen edges.
