---
id: creative-arts.animation.pipeline.usd-variant-sets
name: usd-variant-sets
category: creative-arts
field: animation
product: pipeline
tags: [variant-sets, usd, openusd, variants, modelingvariant, shadingvariant, lod-variants, costume-variants, asset-variants-usd]
level: advanced
status: draft
description: "Author and select USD variant sets for animation assets: costume/shading/LOD variants, nesting, default selections, and choosing variants per shot."
sources:
  - https://openusd.org/release/glossary.html#usdglossary-variantset
  - https://openusd.org/release/tut_authoring_variants.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USD variant sets

**Goal:** one asset with switchable versions (outfits, damage states, colour schemes, LODs), chosen per shot
by setting a selection, not by publishing separate assets.

## Author

```python
from pxr import Usd, UsdGeom
stage = Usd.Stage.Open("hero.usda")
prim = stage.GetDefaultPrim()
vset = prim.GetVariantSets().AddVariantSet("costume")
for name in ["casual", "winter", "pajamas"]:
    vset.AddVariant(name)
    vset.SetVariantSelection(name)
    with vset.GetVariantEditContext():
        # opinions authored here live inside the variant
        stage.OverridePrim(prim.GetPath().AppendPath("geo/outfit")).GetReferences().AddReference(f"./outfits/{name}.usdc")
vset.SetVariantSelection("casual")   # default
stage.GetRootLayer().Save()
```

Conventional set names: `modelingVariant`, `shadingVariant`, `lodVariant`, plus show-specific (`costume`,
`damage`).

## Select in a shot

In the shot's layout or animation layer:
```usda
over "hero_01" ( variants = { string costume = "winter" } ) { }
```
Selections are opinions too: the strongest selection wins (lighting can override a shading variant if needed).

## Nesting

Variants can contain other variant sets (e.g. costume variant contains a shading variant set). Keep nesting
shallow; deep nesting is hard to debug.

## Gotchas

- Only opinions authored inside the variant edit context belong to the variant; authoring outside puts them
  on all variants.
- Selecting a variant name that does not exist silently yields nothing from that set; validate names.
- Variants are composition, not instancing: heavy variants behind a payload keep load times down.

## Verify

`usdview`, select the prim, Meta Data tab shows variant sets; switching selection changes the viewport; a
shot layer selection appears in the composition panel for that prim.
