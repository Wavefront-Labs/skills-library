---
id: creative-arts.animation.motion-graphics.ae-precompose-and-nesting
name: ae-precompose-and-nesting
category: creative-arts
field: animation
product: motion-graphics
tags: [precompose, pre-compose, nested-compositions, after-effects, collapse-transformations, composition-structure]
level: practitioner
status: draft
description: "Precompose in After Effects: when to nest, the two Pre-compose options, collapse transformations, rendering-order effects, resolution traps and tidy comp trees."
sources:
  - https://helpx.adobe.com/after-effects/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Precomposing and nesting (After Effects)

**Pre-compose** (Layer > Pre-compose, Ctrl/Cmd+Shift+C) moves selected layers into a new composition, which then appears as one layer in the original comp.

## When to precompose
- To apply an effect, mask or matte to a **group** of layers as one image.
- To **reuse** an animation several times (and retime each copy independently).
- To **organise** a crowded timeline: character parts, background, titles.
- To control **render order** (for example, apply an effect after another layer's masks and effects: effects in the outer comp see the inner comp's finished pixels).
- To work with track mattes or time remapping on a group (`ae-track-mattes.md`).

## The dialog options
- **Leave all attributes in [comp]**: only one layer is allowed. The layer keeps its effects, masks and transformations in the original comp and the new comp holds just the source.
- **Move all attributes into the new composition**: layers keep their properties inside the new comp; the new nested layer starts with default transform. This is the usual choice for multiple layers.
- **Open New Composition** shows the new comp as soon as it is created.
- A new comp takes the dimensions of the current comp, and its duration is based on the selected layers.

## Collapse Transformations switch
- Without it, the nested comp is rasterised at its comp size, then transformed in the outer comp. Scaling up can look soft, and effects in the nested comp ignore the outer camera.
- With **Collapse Transformations / Continuously Rasterize** on (the same switch applies to vector layers and to nested comps), the inner layers are transformed directly with the outer comp's settings, retaining sharpness and 3D relationships. It also changes render order: blending modes inside may behave differently.

## Traps
- Precomposed comps have their own **frame size**; if you scale a precomp 200%, make it larger rather than scaling up.
- Track mattes inside a precomp and 3D layers: layers inside a flat precomp do not intersect with outer 3D layers, unless transformations are collapsed.
- Renaming precomps and keeping them in a Project panel folder avoids a pile of "Pre-comp 1".
- Heavy nesting slows previews; render and replace large precomps when needed.

## Verify
- [ ] Names are descriptive; folders organise the nested comps.
- [ ] Collapse state is deliberate; edges stay sharp at final scale.
