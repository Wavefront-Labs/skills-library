---
id: creative-arts.animation.pipeline.usd-composition-arcs
name: usd-composition-arcs
category: creative-arts
field: animation
product: pipeline
tags: [composition-arcs, usd, openusd, references, payloads, inherits, specializes, livrps, asset-structure]
level: advanced
status: draft
description: "Use USD composition arcs for animation assets: references vs payloads, inherits for class-wide edits, LIVRPS strength order, and a standard asset file layout."
sources:
  - https://openusd.org/release/glossary.html#usdglossary-compositionarcs
  - https://openusd.org/release/glossary.html#livrps-strength-ordering
  - https://openusd.org/release/tut_referencing_layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USD composition arcs

**Goal:** assets authored once and reused hundreds of times, loadable on demand, overridable per shot,
with class-wide fixes possible.

## The arcs (LIVRPS strength order, strongest first)

| Arc | Use |
|---|---|
| **L**ocal opinions | edits in the current layer stack |
| **I**nherits | class-based edits: change `/_class_tree` and every inheriting tree updates |
| **V**ariant sets | switchable alternatives (`creative-arts.animation.pipeline.usd-variant-sets`) |
| **R**eferences | bring an asset into a scene namespace |
| **P**ayloads | references that can be unloaded (deferred loading of heavy geometry) |
| **S**pecializes | weakest fallback-style base (material libraries) |

## Typical asset file

```usda
#usda 1.0
( defaultPrim = "chair" )
def Xform "chair" ( kind = "component"
    payload = @./chair_payload.usdc@ )    # heavy geo behind a payload
{
}
```
Layout references it per instance:
```usda
def "chair_01" ( prepend references = @/assets/chair/chair.usda@ ) { double3 xformOp:translate = (120, 0, 40) uniform token[] xformOpOrder = ["xformOp:translate"] }
```
With `defaultPrim` set, the reference does not need a prim path.

## Payloads in practice

Open big sets with payloads unloaded (`Usd.Stage.Open(path, Usd.Stage.LoadNone)`), then load only what you
need. Animators load characters and the set's proxy; lighting loads everything at render.

## Instancing

Mark repeated references `instanceable = true` so USD shares their prototypes: big memory and load-time wins
for crowds of props.

## Gotchas

- References are resolved relative to the layer that authors them; use the studio's asset resolver or anchored
  paths consistently.
- Local opinions always win over referenced content; a stray override in a shot layer hides later asset fixes.
  Audit with usdview's composition inspector.
- Kind metadata (`component`, `assembly`, `group`) matters for selection and model hierarchy tools; set it.

## Verify

In usdview, toggle a payload unload/load; edit a class prim and see all inheriting instances update; the
composition panel shows the expected arc for a selected prim.
