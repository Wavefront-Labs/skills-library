---
id: computing-software.computer-graphics-engineering.rendering-techniques.sorting-transparent-objects
name: sorting-transparent-objects
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, transparent-sorting, alpha-blending, render-queue, back-to-front, sort-keys]
level: practitioner
status: draft
description: "Sort transparent geometry correctly: back-to-front by view depth, choosing sort keys, per-object vs per-triangle sorting, intersecting objects, and render queues/priorities."
sources: ["https://www.khronos.org/opengl/wiki/Transparency_Sorting", "https://docs.unity3d.com/Manual/SL-SubShaderTags.html", "https://realtimecollisiondetection.net/blog/?p=86"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sorting transparent objects

## 1. Why
Alpha blending `src * a + dst * (1 - a)` is order-dependent: surfaces must be drawn back-to-front
(after all opaques, with depth test on and depth write off).

## 2. Sort key
- Distance along the camera forward axis `dot(objCenter - camPos, camForward)` is better than
  Euclidean distance (more stable for wide FOVs and objects side by side).
- Pack into a 64-bit key: `[layer/queue 8 bits][depth 24 bits inverted][material 32 bits]` and
  radix sort (Ericson's "Order your graphics draw calls around").
- Artist overrides: render queue / sorting priority (Unity `Queue=Transparent+1`, UE Translucency
  Sort Priority) for cases the heuristic gets wrong (windows inside cars).

## 3. Granularity
- Per object: cheap, wrong when objects interpenetrate or are large (a long glass corridor).
- Per triangle (within a mesh): sort indices on CPU or compute each frame for complex transparent
  meshes (hair cards, foliage); expensive.
- Two-pass for convex-ish single meshes: draw back faces first (cull front), then front faces
  (cull back); fixes self-sorting for closed convex shapes.
- Depth prepass for transparent objects (write depth in a first pass, then draw colour with EQUAL):
  shows only the nearest layer of each object (no inner surfaces); good for "ghost" effects.

## 4. When sorting is not enough
Interpenetrating or cyclically overlapping surfaces can't be sorted per object. Use OIT (weighted
blended, per-pixel lists, moment-based), or alpha-to-coverage/hashed alpha for foliage and hair.

## 5. Particles
Sort particles per emitter back-to-front (GPU bitonic/radix sort for large counts); additive particles
need no sorting (commutative), so prefer additive for sparks and glows.

## Gotchas
- Sorting by object centre fails for large objects: water planes vs boats; give water a fixed queue.
- Depth write on for transparents hides objects behind them that are drawn later.
- Mixed premultiplied and straight alpha blending modes give dark fringes regardless of order.

## Verify
- [ ] Camera orbit test around overlapping transparent objects: no popping order swaps.
- [ ] Additive effects unaffected by order.
