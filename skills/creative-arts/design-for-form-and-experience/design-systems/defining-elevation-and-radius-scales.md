---
id: creative-arts.design-for-form-and-experience.design-systems.defining-elevation-and-radius-scales
name: defining-elevation-and-radius-scales
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [elevation, shadow-scale, border-radius-scale, corner-radius, shadows, shape-tokens, design-tokens]
level: practitioner
status: draft
description: "Define elevation and shadow scales and a corner-radius scale as tokens: layered ambient and key shadows, semantic levels, radius steps by component size, nested radius maths."
sources:
  - "Material Design 3 - Elevation and Shape (m3.material.io/styles/elevation, m3.material.io/styles/shape)"
  - "Josh Comeau - Designing Beautiful Shadows in CSS (joshwcomeau.com/css/designing-shadows)"
  - "Fluent 2 - Shadow and Corner radius tokens (fluent2.microsoft.design/shapes)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Elevation, shadow and corner-radius scales

## Elevation levels
- **5-6 semantic levels:** 0 flat, 1 raised (card), 2 sticky (header, dropdown), 3 overlay (popover, menu), 4 modal, 5 toast/tooltip. Name by role (`elevation.card`), not pixel values.
- **Shadow recipe:** layered shadows, each with a **key** (directional, sharper) and **ambient** (soft) component; greater elevation = larger offset-y and blur, lower opacity: e.g. level 1 `0 1px 2px rgb(0 0 0 / .12), 0 1px 3px rgb(0 0 0 / .08)`; level 3 `0 8px 16px rgb(0 0 0 / .14), 0 2px 4px rgb(0 0 0 / .08)`.
- Use a consistent light source (top); shadow colour a darker tint of the background hue rather than pure black for natural look.
- **Dark themes:** shadows vanish; raise by lighter surface tint (Material 3 tonal elevation); also use borders (`creative-arts.design-for-form-and-experience.interaction-design.designing-dark-mode-ui`).
- Pair elevation with **z-index tokens** (base, sticky, dropdown, modal, toast) to prevent stacking wars.
- Do not use shadows as the only separator (WCAG non-text contrast if boundary defines a control).

## Radius scale
- 5-6 steps: 0, 2 or 4 (inputs, small), 8 (cards, buttons), 12 or 16 (sheets), 24-28 (large containers), 9999 (pills, avatars). Material 3: none, extra-small 4, small 8, medium 12, large 16, extra-large 28, full.
- **Nested radius rule:** inner radius = outer radius - padding (so concentric corners look even).
- Consistency by component family (all inputs same radius); brand personality dial (sharp vs friendly).
- Use `border-radius` tokens bound in Figma (variables) and CSS (`--radius-md`); clip content with `overflow: hidden` when children touch corners.

## Verify
- [ ] Shadow tokens are layered, named by role, and paired with z-index tokens.
- [ ] Radius steps applied by component size; nested radii computed.
- [ ] Dark theme elevation handled with surfaces or borders.
