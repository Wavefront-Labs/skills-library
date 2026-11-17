---
id: computing-software.computer-graphics-engineering.rendering-techniques.inverted-hull-outlines
name: inverted-hull-outlines
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, inverted-hull, silhouette-edges, outline-rendering, backface-extrusion, smoothed-normals, screen-space-outline-width, toon-outlines]
level: practitioner
status: draft
description: "Draw stylised silhouette outlines with the inverted-hull technique: back-face extrusion along smoothed normals, constant screen-space width, vertex-colour width control."
sources: ["https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 15.2", "https://bgolus.medium.com/the-quest-for-very-wide-outlines-ba82ed442cd9"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inverted-hull outlines

**Goal:** clean, controllable ink lines around characters and props — the standard for
toon-style games (RTR4 §15.2.3 "shell" methods).

## 1. Technique
Render the mesh a second time: **front faces culled**, vertices pushed outward along the
normal, filled with the outline colour. Only the extruded back faces peeking around the
silhouette are visible.
```glsl
// outline pass vertex shader (clip-space extrusion for constant pixel width)
vec4 clip = viewProj * model * vec4(pos, 1.0);
vec3 nView = normalize(mat3(view * model) * outlineNormal);
vec2 offset = normalize((proj * vec4(nView, 0.0)).xy);
clip.xy += offset * (outlineWidthPx * 2.0 / screenSize) * clip.w * widthScale;  // widthScale from vertex colour
gl_Position = clip;
```
State: `cullMode = FRONT`, depth test on, depth write on; draw after or before the main
pass (before + depth test hides interior parts correctly).

## 2. Smoothed normals (essential)
Hard edges (split normals) make the hull crack open at corners → gaps in the line. Bake a
**smoothed normal** (average of normals at each position) into a spare attribute (tangent,
vertex colour or UV channel) and extrude along that, while shading still uses the real
normals.

## 3. Width control
- Constant screen-space width (above) vs world-space width (`pos + n * w`, lines thin out at
  distance — sometimes desired). Clamp both extremes.
- Per-vertex width in vertex colour: thin lines at fingertips, thicker at silhouettes,
  zero where lines should vanish (Guilty Gear Xrd).
- Scale with distance/FOV so close-ups don't get thick blobs.

## 4. Complementing screen-space edges
Inverted hulls draw **silhouettes** only. Interior creases, material borders and
intersections need: edge detection post-process (depth/normal/ID discontinuities), authored
lines in textures (Motomura lines), or geometry-shader feature edges.

## Gotchas
- Thin geometry (cloth, hair cards, planes) has no volume → hull draws over the front; disable
  outlines or use a screen-space method there.
- Z-fighting between outline and object at grazing angles: small depth offset toward the
  camera for the main pass or push the hull slightly back in view space.
- Doubles draw calls/vertex cost for outlined objects; batch outline passes.

## Verify
- [ ] No gaps at hard edges (smoothed normals baked).
- [ ] Line width constant in pixels across distances within clamp limits.
- [ ] Planar/thin objects excluded or handled by screen-space edges.
