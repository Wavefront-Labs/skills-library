---
id: computing-software.computer-graphics-engineering.shader-programming.height-fog-and-screen-space-fog
name: height-fog-and-screen-space-fog
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, height-fog, exponential-fog, distance-fog, atmospheric-fog, depth-reconstruction]
level: practitioner
status: draft
description: "Add distance and exponential height fog in shaders: analytic integral along the view ray, inscattering colour toward the sun, depth reconstruction, and sky handling."
sources: ["https://iquilezles.org/articles/fog/", "https://docs.unrealengine.com/5.3/en-US/exponential-height-fog-in-unreal-engine/", "https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-13-volumetric-light-scattering-post-process"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screen-space fog and height fog

## 1. Distance fog
```glsl
float fogAmount = 1.0 - exp(-dist * density);      // exponential
vec3 col = mix(sceneCol, fogColor, fogAmount);
```
Linear and exp2 variants exist; exponential follows Beer-Lambert.

## 2. Exponential height fog (analytic)
Density falls with height: `d(y) = a * exp(-b * y)`. Integrating along the ray from camera `ro`
with direction `rd` over distance `t` (Quilez):
```glsl
float heightFog(vec3 ro, vec3 rd, float t, float a, float b) {
    float fog = (a / b) * exp(-ro.y * b) * (1.0 - exp(-t * rd.y * b)) / rd.y;
    return 1.0 - exp(-fog);
}
```
Guard `rd.y` near zero (`abs(rd.y) < 1e-4` -> use the limit `a * exp(-ro.y*b) * t`).

## 3. Sun inscattering
Tint fog toward the sun colour when looking toward it:
```glsl
float sunAmt = pow(max(dot(rd, sunDir), 0.0), 8.0);
vec3 fogCol = mix(fogBlue, sunYellow, sunAmt);
```

## 4. As a post pass
- Reconstruct world position from depth: `worldPos = camPos + viewRay * linearDepth`, with
  `viewRay` interpolated from the fullscreen triangle's frustum corners (scaled so `.z` = 1).
- Apply before transparents (or apply fog per transparent in their shaders, since the post pass
  only sees opaque depth).
- Sky pixels (depth = far): either skip (sky shader has its own horizon fog) or apply with a capped
  distance.

## Gotchas
- Reversed-Z depth: far = 0; linearisation formula changes.
- Fog in the forward shader vs post pass must match exactly or transparents look detached.
- Applying fog after tonemapping makes it look flat; fog in linear HDR before tonemap.

## Verify
- [ ] Fog density decreases with altitude; looking down from a mountain clears.
- [ ] Transparent objects fogged consistently with opaques at the same distance.
