---
id: creative-arts.design-for-form-and-experience.design-systems.designing-an-icon-grid-and-style-guide
name: designing-an-icon-grid-and-style-guide
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [icon-grid, keylines, icon-style-guide, iconography, icon-design, icon-system, pixel-fitting]
level: practitioner
status: draft
description: "Design an icon set: grid with keylines and padding, stroke and corner rules, optical balance, sizes, metaphor guidance and a style guide that keeps new icons consistent."
sources:
  - "Material Design - System icons: grid and keyline shapes (m2.material.io/design/iconography/system-icons.html)"
  - "Apple - SF Symbols design guidance (developer.apple.com/design/human-interface-guidelines/sf-symbols)"
  - "IBM Carbon Design System - Iconography (carbondesignsystem.com/elements/icons/design)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Icon grid, keylines and style guide

**Goal:** a family of icons that look drawn by one hand and read at small sizes.

## Grid
- Base canvas **24x24** (also 16, 20, 32 optical variants); **live area** 20x20 with **2 px padding**.
- **Keylines** for balanced shapes: circle 20 diameter, square 18x18, portrait rectangle 16x20, landscape 20x16; fit the main shape to the closest keyline so icons have equal visual weight.
- Pixel-fit strokes: horizontal and vertical edges on the pixel grid for crispness at 1x.

## Style rules (write them down)
- **Stroke weight** 1.5 or 2 px (outlined) uniformly; minimum gap between strokes 2 px.
- **Corner radius** 2 px for rounded joins (or sharp), terminals round or square, consistent.
- **Angles** in 45-degree increments; avoid 1-px details and tiny counters.
- **Filled vs outline** variants: filled for selected state; do not mix styles within a set.
- **Metaphors:** one concept per icon; prefer established symbols (magnifier, trash, gear); avoid text in icons and culture-specific gestures; **icon plus label** where meaning is uncertain.
- **Optical sizing:** thicker details at small sizes, finer at large; provide sizes where needed.
- **Colour:** single colour via `currentColor`; multicolour only for illustrations.

## Process
1. Audit existing icons, set the style, draw 10-20 core icons on the grid template.
2. Review in a **sample sheet** at 16/24/48 px and 1x/2x; squint test for consistent weight.
3. Document: grid diagram, do/don't examples, naming (`arrow-left`, `file-plus`), contribution checklist.

## Verify
- [ ] Every icon sits on the grid and keylines; stroke and radius uniform.
- [ ] Sheet review at small sizes shows consistent visual weight.
- [ ] Naming and contribution rules published.
