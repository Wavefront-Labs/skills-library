---
id: computing-software.computer-graphics-engineering.rendering-techniques.screen-space-contact-shadows
name: screen-space-contact-shadows
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, shadows, screen-space-shadows, contact-shadows, ray-marching, depth-buffer, bend-studio]
level: practitioner
status: draft
description: "Add screen-space contact shadows: short depth-buffer ray marches toward the light per pixel, thickness heuristics, step counts, jitter with TAA, and combining with shadow maps."
sources: ["https://www.bendstudio.com/blog/inside-bend-screen-space-shadows/", "https://docs.unrealengine.com/5.3/en-US/contact-shadows-in-unreal-engine/", "https://panoskarabelas.com/posts/screen_space_shadows/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screen-space contact shadows

Shadow maps lack resolution for small-scale contact (feet on ground, wrinkles, grass bases).
Screen-space shadows march a short ray toward the light through the depth buffer.

## 1. Algorithm
```glsl
float contactShadow(vec3 posVS, vec3 lightDirVS, float noise) {
    const int STEPS = 16; const float MAX_DIST = 0.3; const float THICKNESS = 0.05;
    vec3 stepV = lightDirVS * (MAX_DIST / float(STEPS));
    vec3 p = posVS + stepV * noise;                        // jitter start, TAA resolves
    for (int i = 0; i < STEPS; i++) {
        p += stepV;
        vec4 clip = proj * vec4(p, 1.0);
        vec2 uv = clip.xy / clip.w * 0.5 + 0.5;
        if (any(lessThan(uv, vec2(0))) || any(greaterThan(uv, vec2(1)))) break;
        float sceneZ = linearDepth(texture(depthTex, uv).r);
        float delta = -p.z - sceneZ;                       // view space -z forward
        if (delta > 0.0 && delta < THICKNESS) return 0.0; // occluded
    }
    return 1.0;
}
```
- Max distance small (a few cm to ~0.5 m); it's for contact detail only.
- **Thickness** threshold avoids thin-object false shadows behind objects (depth buffer has no
  thickness info).
- Fade near screen edges and with distance from the camera.

## 2. Bend Studio approach (Days Gone)
A compute shader marches in screen space along the light direction projected to screen, sharing
depth samples across a wavefront (line-based traversal), giving long, cheap shadows at full res;
open-sourced in the "Inside Bend: Screen Space Shadows" post.

## 3. Combining
Multiply with the shadow map term for the main directional light (and optionally the brightest local
lights). Apply in the lighting pass or write a separate mask.

## Gotchas
- Only occluders visible on screen cast; off-screen or occluded geometry doesn't.
- Self-shadowing acne on sloped surfaces: start the ray slightly offset along the normal.
- Hair/foliage with alpha are absent from depth (if not written) and won't cast.

## Verify
- [ ] Contact shading at object/ground contact visible in shadowed and lit areas.
- [ ] No dark halos behind thin objects; stable under TAA.
