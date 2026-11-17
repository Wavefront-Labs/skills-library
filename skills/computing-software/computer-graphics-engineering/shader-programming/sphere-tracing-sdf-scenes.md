---
id: computing-software.computer-graphics-engineering.shader-programming.sphere-tracing-sdf-scenes
name: sphere-tracing-sdf-scenes
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, raymarching, sdf, sphere-tracing, sdf-normals, sdf-soft-shadows, sdf-ambient-occlusion, shadertoy, signed-distance-functions, raymarch-camera]
level: advanced
status: draft
description: "Render 3D signed-distance scenes by sphere tracing: camera rays, march loop with epsilon and step limits, gradient normals, soft shadows and AO, and keeping SDFs Lipschitz-safe."
sources: ["https://iquilezles.org/articles/distfunctions/", "https://iquilezles.org/articles/normalsSDF/", "https://iquilezles.org/articles/rmshadows/", "https://graphics.stanford.edu/courses/cs348b-20-spring-content/uploads/hart.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sphere tracing SDF scenes

**Goal:** a robust ray marcher for SDF scenes (Shadertoy-style art, procedural effects,
volumetric UI elements, SDF-based collision previews).

## 1. Camera ray
```glsl
vec2 uv = (2.0 * fragCoord - iResolution.xy) / iResolution.y;
vec3 ro = camPos;
vec3 fw = normalize(target - ro), rt = normalize(cross(fw, vec3(0, 1, 0))), up = cross(rt, fw);
vec3 rd = normalize(uv.x * rt + uv.y * up + 1.5 * fw);       // 1.5 = focal length
```

## 2. March loop
```glsl
float map(vec3 p);                         // scene SDF: min of primitives
float march(vec3 ro, vec3 rd) {
    float t = 0.0;
    for (int i = 0; i < 128; ++i) {
        float d = map(ro + rd * t);
        if (abs(d) < 0.0005 * t) return t;  // epsilon grows with distance (pixel-footprint)
        t += d;
        if (t > 100.0) break;
    }
    return -1.0;
}
```
Sphere tracing is safe only if `map` never **overestimates** distance (Lipschitz ≤ 1).
Non-uniform scaling, twists, displacement by noise break it → overstepping artefacts
(holes, banding). Fix by multiplying the step: `t += d * 0.7` or by dividing the SDF by its
Lipschitz bound.

## 3. Normals
Tetrahedral gradient (4 evaluations instead of 6):
```glsl
vec3 calcNormal(vec3 p) {
    const vec2 k = vec2(1, -1); const float h = 0.0005;
    return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
}
```
Prevent the compiler inlining `map` 4 times (huge shaders) with IQ's loop trick when compile
time explodes.

## 4. Soft shadows and AO
```glsl
float softShadow(vec3 ro, vec3 rd, float k) {        // k ~ 8-32: higher = sharper
    float res = 1.0, t = 0.02;
    for (int i = 0; i < 64 && t < 20.0; ++i) {
        float h = map(ro + rd * t);
        res = min(res, k * h / t);
        if (res < 0.001) break;
        t += clamp(h, 0.01, 0.2);
    }
    return clamp(res, 0.0, 1.0);
}
float ao(vec3 p, vec3 n) { float o = 0.0, s = 1.0;
    for (int i = 1; i <= 5; ++i) { float h = 0.03 * float(i); o += (h - map(p + n * h)) * s; s *= 0.7; }
    return clamp(1.0 - 2.0 * o, 0.0, 1.0); }
```
Offset shadow ray origin along the normal to avoid self-shadowing.

## 5. Performance
- Bounding volumes: early-out `map` per object with a cheap sphere/box test.
- Lower `MAX_STEPS` and resolution; render at half-res and upscale for heavy scenes.
- Material IDs: return `vec2(dist, id)` from `map` instead of re-evaluating per material.

## Gotchas
- Dynamic loop counts and branches are fine on desktop, expensive on mobile.
- Precision: far distances with small epsilon never converge → step-limit artefacts
  ("onion rings"); use relative epsilon as above.

## Verify
- [ ] No holes or rings on deformed objects (step scaling sufficient).
- [ ] Normals continuous (no faceting) on curved primitives.
- [ ] Frame time at target resolution within budget with step count logged via debug colour.
