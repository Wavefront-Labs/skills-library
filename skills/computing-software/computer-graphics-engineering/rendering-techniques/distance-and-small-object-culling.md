---
id: computing-software.computer-graphics-engineering.rendering-techniques.distance-and-small-object-culling
name: distance-and-small-object-culling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, distance-culling, small-object-culling, screen-size-culling, lod, performance]
level: intro
status: draft
description: "Cull by distance and projected size: per-object max draw distances, screen-size thresholds from bounding spheres, per-layer cull distances, and fading to avoid pops."
sources: ["https://docs.unity3d.com/ScriptReference/Camera-layerCullDistances.html", "https://docs.unrealengine.com/5.3/en-US/cull-distance-volumes-in-unreal-engine/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distance and small-object culling

## 1. Distance culling
Objects beyond a max distance are skipped. Set per object type: small props 50-100 m, medium
objects 200-500 m, landmarks unlimited.
- Unity: `Camera.layerCullDistances` (per layer, with `layerCullSpherical`), LOD Group culled level.
- Unreal: per-actor Max/Desired Draw Distance, Cull Distance Volumes mapping object size to
  distance.

## 2. Screen-size culling
Cull when the projected size is below a few pixels. Projected radius (perspective):
```cpp
float projectedRadiusPx(float r, float dist, float fovY, float screenH) {
    return (r / (dist * tanf(fovY * 0.5f))) * (screenH * 0.5f);
}
bool cull = projectedRadiusPx(sphere.r, dist, fovY, screenH) < minPixels;   // e.g. 2 px
```
Scales automatically with resolution and FOV (zoomed scopes show more detail).

## 3. Fading
Popping at the cull distance is distracting. Options:
- Dithered/hashed alpha fade over the last 10% of distance (works with TAA).
- Scale-down fade for foliage/grass.
- Hide the boundary in fog.

## 4. Shadows and other passes
Shadow casters can use a shorter cull distance than the main view (distant small casters contribute
little); reflection probes/captures can cull more aggressively.

## Gotchas
- Distance from camera position vs to the object's bounds: measure to the bounding sphere's surface
  so large objects don't vanish when the camera is near their edge.
- FOV changes (zoom) should scale distance thresholds; screen-size culling handles it.

## Verify
- [ ] Cull distance debug view per object category; no landmark disappears.
- [ ] Draw count reduction measured; pops not noticeable in playtest.
