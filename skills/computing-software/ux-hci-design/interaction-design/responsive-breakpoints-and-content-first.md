---
id: computing-software.ux-hci-design.interaction-design.responsive-breakpoints-and-content-first
name: responsive-breakpoints-and-content-first
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [responsive-design, breakpoint-strategy, id-responsive-touch]
level: practitioner
status: draft
description: "Choose breakpoints where content breaks, design mobile-first and use fluid layouts and container queries."
sources:
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responsive approach
- Mobile-first CSS with `min-width` media queries; add breakpoints when content needs it.
- Fluid grids (`clamp()`, `minmax()`, CSS grid auto-fit), flexible images (`max-width:100%`, `srcset`).
- Container queries (`@container`) for components independent of viewport.
- Include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Test at 320 px width and 400% zoom (WCAG reflow).

## Verify
- [ ] No horizontal scroll at 320 CSS px; tap targets remain usable.
