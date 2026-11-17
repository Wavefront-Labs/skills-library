---
id: computing-software.computer-graphics-engineering.rendering-techniques.light-volumes-and-attenuation-windowing
name: light-volumes-and-attenuation-windowing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, light-attenuation, light-volumes, deferred-shading, stencil-light-volumes, spot-cone-bounds, light-culling]
level: practitioner
status: draft
description: "Bound light influence for culling: finite range windowing, light volume meshes in deferred shading, stencil-optimised volumes, and tight cone bounds for spot lights."
sources: ["https://www.realtimerendering.com/", "https://bartwronski.com/2017/04/13/cull-that-cone/", "https://docs.unrealengine.com/5.3/en-US/physically-based-rendering-in-unreal-engine/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Light volumes and attenuation windowing

## 1. Finite range
Physically, light never reaches zero. For culling, each light gets a radius where its contribution
is windowed smoothly to 0:
```glsl
float window = pow(clamp(1.0 - pow(d / range, 4.0), 0.0, 1.0), 2.0);
float atten = window / max(d * d, 0.01 * 0.01);
```
Choose `range` from intensity: radius where `I / d^2` drops below a threshold (e.g. 1% of exposure
middle grey) - `range = sqrt(I / threshold)`. Too small = visible cut-off; too large = wasted
shading.

## 2. Deferred light volumes
Render geometry covering each light's influence, shading only covered pixels:
- Point: low-poly sphere (icosphere with radius scaled so the mesh circumscribes the sphere).
- Spot: cone mesh.
- Directional/ambient: fullscreen triangle.
Draw back faces with depth test `GREATER_EQUAL` (shading pixels whose geometry is inside/in front
of the volume's back) so it works when the camera is inside the volume.

## 3. Stencil optimisation
Two-pass: (1) mark pixels where scene depth is inside the volume using stencil (front faces
increment, back faces decrement with depth test, colour writes off), (2) shade with stencil test.
Removes shading of pixels in front of or behind the volume. Often slower than a single back-face pass
on modern GPUs because of the extra pass; measure. Tiled/clustered light lists replace this for
many lights.

## 4. Tight bounds for culling
- Point: bounding sphere.
- Spot: a sphere around the cone is loose for narrow cones. Use the cone itself for tile/cluster
  tests (Wronski "Cull that cone"):
```glsl
bool sphereVsCone(vec3 sc, float sr, vec3 apex, vec3 dir, float range, float angle) {
    vec3 v = sc - apex;
    float v2 = dot(v, v), v1 = dot(v, dir);
    float d = cos(angle) * sqrt(v2 - v1 * v1) - v1 * sin(angle);
    return !(d > sr || v1 > sr + range || v1 < -sr);
}
```
- Narrow spot bounding sphere: centre at `apex + dir * range / (2 cos^2(angle))` when angle < 45
  degrees, radius equal to that distance.

## Gotchas
- Volume mesh slightly smaller than the true radius clips light at edges; scale the mesh to
  circumscribe.
- Camera near plane inside the volume with front-face rendering loses the light; use back faces.

## Verify
- [ ] Light visualisation overlay: volumes cover exactly the lit area; no clipping rings.
- [ ] Light count per tile/cluster drops with cone tests vs spheres.
