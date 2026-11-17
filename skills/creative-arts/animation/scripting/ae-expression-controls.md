---
id: creative-arts.animation.scripting.ae-expression-controls
name: ae-expression-controls
category: creative-arts
field: animation
product: scripting
tags: [expression-controls, ae-expressions, expressions, after-effects, slider-control, checkbox-control, layer-control, dropdown-menu-control, control-layer, rigging]
level: practitioner
status: draft
description: "Rig After Effects comps with Expression Controls: sliders, checkboxes, colour, point, layer and dropdown controls on a control null, linked by pick-whip."
sources:
  - https://helpx.adobe.com/after-effects/using/expression-controls.html
  - https://ae-expressions.docsforadobe.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Expression controls

**Goal:** one control layer with clearly labelled knobs that drive many properties, so animators and
template users adjust a whole design without touching expressions.

## Controls (Effect - Expression Controls)

| Control | Value | Typical use |
|---|---|---|
| Slider Control | number | amplitude, delay, count |
| Angle Control | degrees | direction |
| Checkbox Control | 0/1 | toggle elements, switch modes |
| Color Control | RGBA | palette colours |
| Point / 3D Point Control | [x,y] / [x,y,z] | targets, offsets |
| Layer Control | a layer | choose which layer to follow |
| Dropdown Menu Control | index 1..n | style variants (AE 17.0+) |

## Pattern: CTRL null

1. Layer - New - Null Object, name it `CTRL`, set as guide layer (not rendered).
2. Add controls and rename them (Enter on the effect name): `Shake Amount`, `Accent Colour`, `Show Logo`.
3. Pick-whip target properties to the controls, or write expressions:
```javascript
// Opacity
thisComp.layer("CTRL").effect("Show Logo")("Checkbox") * 100
// Position wiggle with slider-driven amount
wiggle(2, thisComp.layer("CTRL").effect("Shake Amount")("Slider"))
// Dropdown driving colour
var i = thisComp.layer("CTRL").effect("Style")("Menu").value;
[ [1,0.3,0.2,1], [0.2,0.5,1,1], [1,1,1,1] ][i-1]
```
4. Expose the CTRL controls in Essential Graphics for mogrts
   (`creative-arts.animation.motion-graphics.mogrt-essential-properties`).

## Clamp and map

Sliders are unbounded by default; set Slider Range (right-click - Edit Value) and clamp in expressions:
`clamp(effect("Count")("Slider"), 1, 20)`.

## Gotchas

- Renaming a control after writing expressions: AE updates expressions that reference by name in most
  cases, but scripts and external references break; name before linking.
- Checkbox returns 0/1, not true/false, in most contexts; multiply or compare explicitly.
- Colour controls return 0-1 floats, not 0-255.

## Verify

Change each control through its range: every linked property responds, nothing breaks at the range
ends, and the CTRL layer does not render (guide layer).
