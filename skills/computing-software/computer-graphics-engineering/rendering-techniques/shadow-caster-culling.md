---
id: computing-software.computer-graphics-engineering.rendering-techniques.shadow-caster-culling
name: shadow-caster-culling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, shadows, shadow-caster-culling, frustum-culling, cascaded-shadow-maps, shadow-performance]
level: practitioner
status: draft
description: "Cull shadow casters efficiently: light-frustum culling, extruding receivers toward the light, cascade-wise caster sets, small-caster rejection and caching static casters."
sources: ["https://learn.microsoft.com/en-us/windows/win32/dxtecharts/common-techniques-to-improve-shadow-depth-maps", "https://docs.unity3d.com/Manual/shadow-performance.html", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shadow caster culling

Shadow passes often draw more geometry than the main view. Culling them well is one of the
biggest CPU and GPU wins.

## 1. Light frustum culling
For each shadow view (cascade, spot frustum, cube face), test casters' bounds against that view's
frustum. For directional cascades the light frustum is an orthographic box around the cascade's
slice of the camera frustum.

## 2. Include off-screen casters correctly
A caster outside the camera view can still shadow visible receivers. Extend the cascade box toward
the light (near plane pulled back) or clamp caster depth ("pancaking": render with depth clamp so
casters in front of the near plane collapse onto it).

## 3. Receiver-based culling (tighter)
Only casters that can shadow **visible receivers** matter:
- Build the convex hull of the camera frustum slice + light direction (sweep the slice toward the
  light) and cull against that volume instead of the full box.
- Advanced: cull casters whose extruded shadow volume (bounding box swept along the light
  direction to the receivers' max depth) doesn't intersect visible receivers' bounds.

## 4. Per-cascade sets
- An object entirely inside cascade 0 need not be drawn in cascade 1 if cascade 1 is only sampled
  outside cascade 0's region (and blending bands are handled).
- Small casters in distant cascades contribute nothing: reject if projected size < 1-2 shadow
  texels (`radius / cascadeTexelWorldSize < threshold`).
- Disable shadow casting on tiny props, decals, particles, and interior objects of closed meshes.

## 5. Static caching
Static casters can be rendered once into a cached map for slowly changing cascades/lights; only
dynamic casters are drawn each frame on top (see shadow atlas caching).

## 6. GPU-driven
Run caster culling in compute per shadow view (same as main-view GPU culling), with Hi-Z built from
the shadow map of the previous frame for occlusion between casters.

## Gotchas
- Over-aggressive culling causes shadows to pop when casters leave the camera view; test by
  orbiting tall objects at the screen edge.
- LOD selection for shadows can use a lower LOD than the main view (cheaper), but large swaps cause
  visible shadow-shape changes.

## Verify
- [ ] Draw count per shadow view logged; reduced without missing shadows.
- [ ] Off-screen tall objects still cast into view.
