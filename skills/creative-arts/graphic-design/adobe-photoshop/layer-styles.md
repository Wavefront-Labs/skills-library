---
id: creative-arts.graphic-design.adobe-photoshop.layer-styles
name: layer-styles
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, layer-styles, drop-shadow-layer-style, stroke-style, inner-shadow, bevel-and-emboss, global-light, scale-effects, styles-panel, copy-layer-style]
level: practitioner
status: draft
description: "Apply and manage Photoshop layer styles: realistic drop shadows, strokes, overlays, global light, scaling effects, copying and saving styles."
sources:
  - https://helpx.adobe.com/photoshop/using/layer-effects-styles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer styles

**Goal:** editable, consistent effects that scale with the design and do not look like 2005.

## Apply
Double-click the layer (not the name) to open Layer Style, or fx button at the bottom of the
Layers panel. Effects: Bevel & Emboss, Stroke, Inner Shadow, Inner Glow, Satin, Color/Gradient/
Pattern Overlay, Outer Glow, **Drop Shadow**. Stroke, overlays, inner/drop shadow can be added
multiple times (+ button).

## Settings that matter
- **Drop shadow realism:** Multiply, a dark colour sampled from the background (not pure black),
  low opacity (20-40%), distance and size proportional to how far the object "floats". Two
  shadows (a tight contact one + a soft wide one) look more natural than one.
- **Use Global Light:** links the angle across all layers; untick when an object needs its own light.
- **Stroke:** Position Outside for text outlines; Inside for crisp edges on shapes; Fill Type
  can be gradient.
- **Color Overlay** recolours an icon or logo without editing pixels.

## Managing styles
- Copy/paste: right-click layer > Copy Layer Style / Paste Layer Style; Alt/Option+drag the fx
  icon to another layer to copy.
- **Scale effects:** Layer > Layer Style > Scale Effects - essential after resizing a document
  (Image Size has "Scale Styles" in its gear menu; keep it on).
- Save to the Styles panel (New Style) to reuse across files or share via CC Libraries.
- **Create Layers** (right-click fx > Create Layers) splits effects into real pixel layers
  for hand editing or for apps that do not read styles - one-way; keep a copy.
- Hide all effects: click the eye next to "Effects".

## Gotchas
- Styles on a layer apply at document resolution; a 2 px stroke designed at 1x becomes thin
  when exported at 2x unless the doc was built at 2x or effects scale.
- Style on a **group** affects the group as a whole (shadow of the combined shape) - often what you want.
- Bevel/emboss and satin date a design quickly; use deliberately.
- Opacity vs Fill: see blend modes skill (Fill 0% keeps the style).

## Verify
- [ ] Shadows match the scene light direction and colour.
- [ ] After any resize, effects scaled proportionally.
- [ ] Reused styles saved in a library, not rebuilt by eye.
