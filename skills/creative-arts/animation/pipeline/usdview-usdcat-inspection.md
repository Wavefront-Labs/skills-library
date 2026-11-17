---
id: creative-arts.animation.pipeline.usdview-usdcat-inspection
name: usdview-usdcat-inspection
category: creative-arts
field: animation
product: pipeline
tags: [usdview, usd, openusd, usdcat, usdchecker, usdtree, usdresolve, debugging-usd, flatten, composition-debugging]
level: advanced
status: draft
description: "Inspect and debug USD with usdview, usdcat, usdtree, usdchecker and usdresolve: composition panels, flattening, converting usdc/usda, and validating assets."
sources:
  - https://openusd.org/release/toolset.html
  - https://openusd.org/release/tut_usdview_plugin.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inspecting USD: usdview, usdcat and friends

**Goal:** answer "why does this prim look like that, and which file says so" in minutes. The OpenUSD
toolset ships command-line tools for exactly this.

## Tools

```bash
usdview sh010.usda                       # interactive viewer + inspector
usdcat asset.usdc                        # print binary as text (usda)
usdcat asset.usdc -o asset.usda          # convert; -o x.usdc converts back
usdcat --flatten sh010.usda -o flat.usda # bake composition into one layer (debug, delivery)
usdtree sh010.usda                       # prim hierarchy outline
usdchecker asset.usda                    # validation (and --arkit for AR rules)
usdresolve @/assets/chair/chair.usda@    # what the asset resolver returns for a path
usdedit layer.usdc                       # open a layer as text in $EDITOR, save back
usddiff a.usda b.usda                    # diff two layers
```

## usdview workflow

- Prim browser, select a prim; **Meta Data** tab shows variant sets/selections; **Layer Stack** tab lists
  layers contributing opinions; **Composition** tab shows arcs. Right-click property - "Value from layer"
  to find the authoring layer.
- Interpreter (Window - Interpreter) gives a Python shell with `usdviewApi.stage`, `usdviewApi.prim`.
- Toggle payloads (load/unload), set the time code, change the camera to the shot camera.
- Turn on Display - Display Purpose (proxy/render/guide) to see what renders vs what is a proxy.

## Common diagnoses

| Symptom | Check |
|---|---|
| prim missing | unresolved reference: `usdresolve` the path; check composition errors in the log |
| wrong value | Value from layer: a stronger layer has an override |
| animation at wrong speed | `timeCodesPerSecond` mismatch between layers |
| huge load time | payloads not used; check with usdtree and file sizes |

## Gotchas

- Flattened files lose composition (variants are baked to the selection); use for debugging or delivery, not
  as working files.
- usdview uses Storm (OpenGL) rendering: material looks differ from production renderers; judge structure,
  not shading.

## Verify

For a known override, usdview's "Value from layer" names the right file; usdchecker passes on published assets.
