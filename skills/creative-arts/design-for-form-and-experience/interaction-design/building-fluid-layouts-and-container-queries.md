---
id: creative-arts.design-for-form-and-experience.interaction-design.building-fluid-layouts-and-container-queries
name: building-fluid-layouts-and-container-queries
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [container-queries, fluid-layout, css-grid-layout, clamp-sizing, intrinsic-layout, responsive-components]
level: practitioner
status: draft
description: "Build fluid layouts with CSS grid, flexible units, clamp and container queries so components adapt to their container, not only the viewport."
sources:
  - "W3C CSS Containment Module Level 3, container queries (w3.org/TR/css-contain-3)"
  - "MDN Web Docs (developer.mozilla.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fluid layouts and container queries

Fluid layouts adjust continuously rather than jump at breakpoints (see `...interaction-design.choosing-responsive-breakpoints`).

## Fluid techniques
- **Relative units:** percentages, `fr` in grid, `rem` and `ch` for text measure.
- **CSS grid with auto-fit:** `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));` makes a card grid reflow without media queries.
- **Flexible type and space with `clamp()`:** `font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);` (see `...design-systems.setting-fluid-typography-with-clamp`).
- **Intrinsic sizing:** `min()`, `max()`, `aspect-ratio`, `max-width: 100%` on media.
- **Gap and padding** that scale with the container.

## Container queries
Component styles respond to the width of their container, not the viewport, so one card works in a sidebar and in a main column.
```css
.card-wrap { container-type: inline-size; container-name: card; }
@container card (min-width: 30rem) { .card { display: grid; grid-template-columns: 8rem 1fr; } }
```
Supported in current evergreen browsers; check support tables for your audience. Container query length units (cqw, cqi) also exist. A container cannot be sized by its own query content, so avoid cycles.

## Design practice
Design components with the width ranges in which they switch layout; document these in the component spec (see `...design-systems.specifying-component-anatomy`). Figma auto layout wrap, min and max (see `...figma.auto-layout-wrap-min-max-and-grid`) approximates this in design.

## Verify
- [ ] Components render correctly at the narrowest and widest container they appear in.
- [ ] No fixed pixel widths on content containers.
- [ ] Container query styles have a sensible fallback.
