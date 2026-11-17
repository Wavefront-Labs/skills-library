---
id: creative-arts.graphic-design.brand-identity.brand-iconography
name: brand-iconography
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, identity-system, brand-iconography, icon-set, icon-design, icon-style, pictograms, visual-identity, svg-icons]
level: practitioner
status: draft
description: "Create a brand icon style that matches the identity: stroke, corner and terminal rules derived from the logo and type, size variants, colour usage and a delivery library."
sources:
  - https://m3.material.io/styles/icons/designing-icons
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brand iconography

**Goal:** icons that look like they belong to the brand (not a generic free set), consistent across web,
app, print and signage.

## Derive the style from the identity
- Stroke weight matched to the primary typeface's stem at icon size (a 2 px stroke on 24 px for a regular
  sans; heavier for bold brands).
- Corners and terminals: rounded if the logo and type are rounded; square if they are sharp.
- Angles: reuse the logo's characteristic angle for diagonals.
- Fill vs outline: decide one primary style; a filled variant for active states or small sizes.
- Perspective: flat front views for UI; brand illustrations can be more expressive but separate from icons.

## Build the system
- Grid and keylines (see icon-grid-and-keylines skill): 24 px live area 20 px, plus 16 and 32/48 px variants
  redrawn for small and large use, not just scaled.
- Metaphor list: agree one meaning per icon across products (one "settings" icon, not three).
- Colour: single colour by default (inherits text colour in UI via `currentColor`); brand-colour duotone for
  marketing only, with rules.

## Expand from a library or draw custom
- Starting from an open set (Material Symbols, Phosphor, Lucide) and adapting stroke and corners is faster;
  check the licence allows modification and redistribution.
- Fully custom icons for large brands; plan 50-150 icons in the first release.

## Deliver
- SVGs optimised (SVGO), outlined strokes or stroke-preserving per developer needs, consistent naming
  (`icon-arrow-right-24.svg`), Figma components with variants, icon font only if required.

## Gotchas
- Mixing icon sets in one product is instantly visible; replace all or none.
- Icons need text labels for accessibility and clarity in most UIs.
- Small sizes on print signage need heavier strokes (see wayfinding pictograms).

## Verify
- [ ] Icons side by side at 24 px show equal optical weight and consistent corners.
- [ ] Library delivered in SVG and Figma with names and a usage page.
