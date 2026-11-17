---
id: creative-arts.graphic-design.typography.fluid-responsive-type-with-clamp
name: fluid-responsive-type-with-clamp
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, web-typography, screen-typography, fluid-typography, clamp, responsive-type, viewport-units, type-scale, accessibility, zoom, utopia]
level: practitioner
status: draft
description: "Set fluid responsive type with CSS clamp(): calculate the slope between min and max viewport sizes, scale ratios fluidly, and keep zoom working for accessibility."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
  - https://utopia.fyi/type/calculator/
  - https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fluid responsive type with clamp()

**Goal:** type sizes that grow smoothly from a small phone to a large desktop with no breakpoint jumps,
while still respecting browser zoom and user font-size settings.

## The formula
`font-size: clamp(MIN, PREFERRED, MAX);` where PREFERRED = `intercept + slope * 100vw`.
- slope = (maxSize - minSize) / (maxViewport - minViewport)
- intercept = minSize - slope * minViewport
- Example: 18 px at 360 px viewport to 22 px at 1280 px viewport:
  slope = 4 / 920 = 0.004348 -> 0.4348vw; intercept = 18 - 0.004348*360 = 16.43 px = 1.027rem.
  `font-size: clamp(1.125rem, 1.027rem + 0.4348vw, 1.375rem);`
- Always mix a **rem** term with the vw term: pure `vw` ignores browser zoom and user font settings
  (fails WCAG 1.4.4 Resize Text).

## Fluid scales
- Use a smaller ratio on mobile (1.2, minor third) and larger on desktop (1.333, perfect fourth), so
  headings grow more than body text. The **Utopia** calculator generates the full set as CSS custom
  properties (`--step-0`, `--step-1`...).
- Keep body text change modest (16-20 px range); let display sizes do the dramatic scaling.

## Line height and measure
- Line height can be unitless and slightly lower for large sizes: `line-height: calc(1em + 0.5rem)`
  gives a tighter ratio as size grows.
- Limit measure with `max-inline-size: 65ch` instead of relying on font size to control line length.

## Container queries
- For components, use container query units (`cqi`) instead of `vw` so type scales with the component's
  width: `font-size: clamp(1rem, 0.8rem + 2cqi, 1.5rem);` inside `container-type: inline-size`.

## Gotchas
- Max sizes too large make headlines break into many lines on big screens; cap with clamp's MAX.
- Testing only at breakpoints misses awkward middle sizes; drag the window across the whole range.
- Zoom to 200% and check text still scales (WCAG 1.4.4).

## Verify
- [ ] Each step hits its min at the min viewport and its max at the max viewport.
- [ ] 200% browser zoom enlarges text; no clipping or overlap.
