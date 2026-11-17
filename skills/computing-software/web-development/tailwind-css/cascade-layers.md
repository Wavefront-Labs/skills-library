---
id: computing-software.web-development.tailwind-css.cascade-layers
name: cascade-layers
category: computing-software
field: web-development
product: tailwind-css
tags: [css-cascade, specificity, cascade-layers, css-layer, layer-order, third-party-css, css-reset, tailwind-v4]
level: practitioner
status: verified
description: "Ordering CSS with @layer so resets, libraries, components and utilities win predictably regardless of specificity, including unlayered and !important rules."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@layer
  - https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_layers
  - https://www.w3.org/TR/css-cascade-5/#layering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cascade layers (@layer)

**Goal:** end specificity wars: which stylesheet wins is decided by layer order you declare, not by selector weight or load order.

## 1. Declare the order once, first
```css
@layer reset, vendor, base, components, utilities;

@layer reset { *, *::before, *::after { box-sizing: border-box; } }
@layer components { .card .title { font-size: 1.25rem; } }     /* specificity 0,2,0 */
@layer utilities  { .text-sm { font-size: .875rem; } }           /* 0,1,0 but later layer -> wins */
```
Between layers, **later layer wins regardless of specificity**. Within a layer the normal specificity/order rules apply.

## 2. Importing third-party CSS into a layer
```css
@import url('vendor/datepicker.css') layer(vendor);
```
Now a library's `#picker .day.selected` (high specificity) can be overridden by a simple class in `components`. With bundlers, `@import … layer()` must be preserved by your CSS pipeline (Lightning CSS/PostCSS handle it).

## 3. Unlayered styles win
Styles not in any layer beat **all** layered styles (they form an implicit last layer). Legacy CSS left unlayered will override your layered system - either put it in a layer or accept it as the top.

## 4. !important reverses the order
Important declarations in **earlier** layers beat important declarations in later layers (and important layered beats important unlayered). Use this for resets that must hold (`@layer reset { [hidden] { display: none !important; } }`).

## 5. Tailwind
Tailwind v4 emits `@layer theme, base, components, utilities;` and real cascade layers. Your custom CSS should go in `@layer components` (or `@utility` for utilities) - unlayered custom CSS will beat utilities and confuse you. Tailwind v3 used `@layer` as a build-time directive, not native layers.

## 6. Debugging
DevTools Styles pane groups rules by layer and shows the layer order; a rule with higher specificity crossed out by a simpler one usually means layer order.

## Verify
- [ ] Layer order statement appears before any layered rules (first `@layer` mention defines order).
- [ ] A utility class overrides a component rule with higher specificity.
- [ ] Vendor CSS overridable without `!important`.
