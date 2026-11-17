---
id: creative-arts.animation.pipeline.usd-layer-stacking
name: usd-layer-stacking
category: creative-arts
field: animation
product: pipeline
tags: [usd-layers, usd, openusd, sublayers, layer-stack, department-layers, opinion-strength, shot-assembly, usda]
level: advanced
status: draft
description: "Structure animation shots as USD layer stacks: one sublayer per department, opinion strength order, edit targets, and keeping layers independent and re-publishable."
sources:
  - https://openusd.org/release/glossary.html#usdglossary-layerstack
  - https://openusd.org/release/glossary.html#livrps-strength-ordering
  - https://openusd.org/release/tut_referencing_layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USD layer stacking per department

**Goal:** layout, animation, FX and lighting each write their own file for a shot, and the shot is the
composition of those files, so departments work in parallel and re-publish without overwriting each other.

## Shot structure

```
sh010.usda                      # shot root: sublayers only, strongest first
  subLayers = [
    @./sh010_lighting.usda@,    # strongest
    @./sh010_fx.usda@,
    @./sh010_anim.usda@,
    @./sh010_layout.usda@,      # weakest: set dressing, cameras, asset references
  ]
```
```usda
#usda 1.0
(
    subLayers = [@./sh010_lighting.usda@, @./sh010_fx.usda@, @./sh010_anim.usda@, @./sh010_layout.usda@]
    startTimeCode = 1001
    endTimeCode = 1120
    timeCodesPerSecond = 24
    framesPerSecond = 24
    upAxis = "Y"
    metersPerUnit = 0.01
)
```

Earlier entries in `subLayers` are **stronger**: lighting's opinion on a light or a material override wins
over layout's. Order departments by who should win conflicts (usually downstream departments stronger).

## Department layers

- Layout: references assets (`creative-arts.animation.pipeline.usd-composition-arcs`), places them, camera.
- Animation: time-sampled transforms/point caches on the referenced prims (`over` prims, not `def`).
- FX: new prims (sims, particles) and overrides.
- Lighting: lights, render settings, material overrides.
Each department writes only `over`s/new prims in its own layer; never edits other layers.

## Python

```python
from pxr import Usd, Sdf
stage = Usd.Stage.Open("sh010.usda")
anim = Sdf.Layer.FindOrOpen("sh010_anim.usda")
stage.SetEditTarget(Usd.EditTarget(anim))      # writes go to the anim layer
xf = stage.GetPrimAtPath("/World/chars/hero")
# ... author time samples ...
anim.Save()
```

## Gotchas

- Time metadata (`timeCodesPerSecond`, start/end) must agree across layers, or animation plays at the wrong
  speed when composed.
- A department accidentally using `def` instead of `over` for an existing prim can replace its type/specifier.
- Version department layers by publishing new files and updating the shot root (or using a resolver), not by
  editing published files in place.

## Verify

`usdview sh010.usda`, select a prim, Layer Stack/Composition panel shows which layer each opinion comes from;
muting a department layer removes only its contributions.
