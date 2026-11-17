---
id: creative-arts.graphic-design.adobe-photoshop.smart-filters-with-masks
name: smart-filters-with-masks
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, smart-filters, smart-filter-mask, filter-blending-options, non-destructive, smart-objects]
level: practitioner
status: draft
description: "Apply filters non-destructively as smart filters: converting to smart objects, filter masks, per-filter blending options, stacking order and performance."
sources:
  - https://helpx.adobe.com/photoshop/using/applying-smart-filters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart filters with masks and blending

**Goal:** every filter stays re-editable, maskable and removable.

## Setup
- Filter > **Convert for Smart Filters** (converts the layer to a smart object). Any filter then
  applied lists under the layer as a smart filter.
- Most filters work; Camera Raw Filter, Liquify, Blur Gallery and Lens Blur are supported in
  current versions. Filters unavailable for smart objects are greyed.

## Editing
- Double-click the filter name to change settings.
- Double-click the sliders icon to the right = **Blending Options** for that filter (mode and
  opacity), e.g. a High Pass filter set to Overlay, or Gaussian Blur at 40% Screen for glow.
- Eye icon toggles a single filter; the "Smart Filters" eye toggles all.

## Filter mask
- One mask shared by all smart filters on the layer (the white thumbnail). Paint black to hide
  the effects locally; gradient for falloff. Mask properties: density and feather.
- Need different masks per filter? Nest: convert the smart object with filter 1 to a new
  smart object, apply filter 2 with its own mask.

## Order
- Filters apply bottom to top. Drag to reorder - e.g. noise after blur, not before.

## Gotchas
- Heavy filters on large smart objects slow redraw; set preview off on hidden layers or rasterise copies late.
- Smart filters on a linked smart object are stored in the parent PSD, not the linked file.

## Verify
- [ ] Each filter can be reopened and toggled.
- [ ] Mask limits the effect only where intended.
