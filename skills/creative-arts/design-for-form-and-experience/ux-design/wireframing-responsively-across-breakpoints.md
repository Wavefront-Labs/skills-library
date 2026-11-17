---
id: creative-arts.design-for-form-and-experience.ux-design.wireframing-responsively-across-breakpoints
name: wireframing-responsively-across-breakpoints
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [responsive-wireframes, responsive-wireframing, breakpoint-wireframes, layout-across-breakpoints, wireframing]
level: practitioner
status: draft
description: "Wireframe responsive layouts across breakpoints: start with content priority, define layout patterns and behaviour at each width, and annotate what changes."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
  - "Luke Wroblewski, Mobile First (A Book Apart, 2011)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Responsive wireframes

Responsive wireframes show how the same content adapts across screen widths. Start from the content priority guide (see `...ux-design.writing-a-content-priority-guide`).

## Steps
1. **Choose breakpoints** from content and your device analytics rather than a device list; wireframe commonly at least a small phone, a tablet and a desktop width (see `...interaction-design.choosing-breakpoints`).
2. **Begin with the narrowest layout** in one column; then widen.
3. **At each breakpoint define** column count, how blocks reflow (stack, side by side, collapse into tabs or accordions), navigation pattern (bottom bar, hamburger, full menu), the size of touch targets and images, and what is hidden or deferred.
4. **Use real content lengths** and a grid (see `...interaction-design.building-column-grids-and-gutters`); test long titles and translations.
5. **Annotate behaviours** that wireframes cannot show: sticky elements, how images crop, how tables adapt (see `...interaction-design.designing-data-tables`).
6. **Include in-between states:** check the layout in between breakpoints, not just at the three widths.
7. **Prototype** a clickable version to test reflow in a browser or in Figma with resizing (see `...figma.figma-constraints-and-layout-grids`).

## Gotchas
- Scaling a desktop layout down and hiding content.
- Wireframing only three widths and ignoring those between.

## Verify
- [ ] The reading order is the same in the DOM and visually.
- [ ] No horizontal page scroll at the narrowest width.
- [ ] Each breakpoint has annotation for behaviour that changes.
