---
id: computing-software.computer-graphics-engineering.rendering-techniques.reflection-probes-and-parallax-correction
name: reflection-probes-and-parallax-correction
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, reflection-probes, parallax-correction, box-projection, cubemap-blending]
level: advanced
status: draft
description: "Place and use local reflection probes: capture, prefilter, box/sphere parallax correction, blending between probes and normalising by diffuse lighting."
sources: ["https://seblagarde.wordpress.com/2012/09/29/image-based-lighting-approaches-and-parallax-corrected-cubemap/", "https://docs.unity3d.com/Manual/class-ReflectionProbe.html", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reflection probes and parallax correction

## 1. Capture
Render a cubemap at the probe position (scene without the probe's own dynamic objects), in HDR,
then prefilter to a GGX mip chain (same as IBL split-sum). Bake at build time; realtime probes
only for a few hero locations, updated one face per frame.

## 2. Box projection (parallax correction)
An infinite cubemap reflects as if the room were at infinity; for rooms, intersect the
reflection ray with the probe's proxy box:
```glsl
vec3 R = reflect(-V, N);
vec3 tMax = (boxMax - P) / R, tMin = (boxMin - P) / R;
vec3 t = max(tMax, tMin);
float d = min(min(t.x, t.y), t.z);
vec3 hit = P + R * d;
vec3 Rc = hit - probePos;                        // corrected lookup direction
vec3 spec = textureLod(probe, Rc, roughness * maxMip).rgb;
```
Works for P inside the box. Fade correction toward plain R at high roughness (correction is
wrong for wide lobes). Sphere proxies for outdoor/irregular spaces.

## 3. Blending
- Each probe has an influence volume plus fade distance; sort by priority/size and blend up to
  2-4 probes per pixel (clustered lists in forward+/deferred).
- Fall back to the sky/global probe outside all volumes.

## 4. Normalisation
Baked probes capture lighting at one point; dark corners reflect a bright probe. Scale
specular by `diffuseAtPixel / diffuseAtProbe` (irradiance from SH or lightmaps), clamped.

## Gotchas
- Probes containing bright lights leak through walls: keep influence volumes inside rooms.
- Moving objects do not appear in baked probes; SSR on top handles near-field reflections.
- Mismatched exposure between bake and runtime makes probes too bright or too dark.

## Verify
- [ ] Floor reflections line up with walls when moving through a room.
