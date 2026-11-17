---
id: creative-arts.design-for-form-and-experience.interaction-design.choosing-responsive-breakpoints
name: choosing-responsive-breakpoints
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [breakpoints, responsive-breakpoints, media-queries, content-based-breakpoints, responsive-design, css-breakpoints]
level: practitioner
status: draft
description: "Choose responsive breakpoints from the content, not devices: find where layout breaks, use a small set, name them as tokens and test in-between widths."
sources:
  - "Ethan Marcotte, Responsive Web Design (A Book Apart, 2011)"
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Choosing breakpoints

A breakpoint is a viewport width where the layout changes. Devices vary continuously, so choose points where the design needs to change.

## Method
1. **Start at the smallest supported width** with a single-column layout (see `...interaction-design.prioritising-content-mobile-first`).
2. **Widen the viewport slowly** and note where the layout breaks: lines too long (see `...interaction-design.setting-line-length-for-readable-ui-text`), gaps too big, items cramped. Add a breakpoint there.
3. **Keep to a few,** typically three to five, and align across components so the page changes together.
4. **Check analytics** to confirm real viewport sizes, including tablets in both orientations and small laptops.
5. **Name them as tokens** (small, medium, large) and document the pixel values in the design system; use `min-width` media queries (mobile-first), with em or rem units so zoom and font-size settings work.
6. **Use fluid layout between breakpoints** (grids, `clamp()`, container queries; see `...interaction-design.building-fluid-layouts-and-container-queries`) so intermediate widths work.
7. **Test** at many widths and with browser zoom at 200 percent and text spacing changes.

## Values
Many frameworks publish default widths (for example Material Design window size classes of compact, medium and expanded: below 600 dp, 600-839 dp, 840 dp and above). Treat them as a starting point and check your content.

## Verify
- [ ] Each breakpoint has a reason you can state.
- [ ] No horizontal scrolling at 320 CSS px width.
- [ ] Layout is acceptable at every width in between.
