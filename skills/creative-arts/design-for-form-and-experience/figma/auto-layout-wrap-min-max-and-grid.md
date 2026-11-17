---
id: creative-arts.design-for-form-and-experience.figma.auto-layout-wrap-min-max-and-grid
name: auto-layout-wrap-min-max-and-grid
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [auto-layout-wrap, auto-layout-grid, min-max-width, absolute-position, figma-auto-layout, responsive-components, figma]
level: practitioner
status: docs-checked
description: "Use advanced Figma auto layout: wrap, min and max sizes, ignore auto layout (absolute position), auto gap and grid auto layout for card galleries and responsive components."
sources:
  - https://help.figma.com/hc/en-us/articles/360040451373-Explore-auto-layout-properties
  - https://help.figma.com/hc/en-us/articles/31289469907863-Use-grid-auto-layout-flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced auto layout: wrap, min/max and grid

## Wrap
- Wrap works on horizontal and vertical flows: children move to a new row or column when they no longer fit.
- Vertical wrap is not masonry: objects stay in auto-layout order and move to the next column only after the current one fills the frame height.
- Wrap with Fill container children plus a min width gives card grids that change column count as the parent resizes. Test by resizing the parent.

## Min and max
- Open the Width or Height dropdown and choose **Add min width**, **Add max width**, **Add min height** or **Add max height**; enter a value or apply a number variable. **Remove min and max** clears them.
- Use for button minimums and readable text column maximums (`creative-arts.design-for-form-and-experience.interaction-design.setting-line-length-for-readable-ui-text`).

## Gap and alignment
- Set the gap to **Auto**, then choose **Between**, **Around** or **Evenly**.
- The alignment box in the right panel sets alignment; B toggles baseline alignment.
- **Ignore auto layout** (formerly absolute position) takes a child out of the flow, for badges and close icons. Select the child and click it in the right sidebar. Such objects can use constraints.

## Grid auto layout
Grid frames hold rows and columns of cells that objects can span. Available on all plans; editing needs can-edit access.
- Track sizes: fixed, **Fill container** (typing "Auto" or "A" sets 1fr), fractional units (`fr`), **Hug contents**, and min/max limits.
- Spanning: set the child to Fill container, then resize on canvas or use the **Column span** and **Row span** fields.
- Gaps: **Gap between rows** and **Gap between columns**; padding is separate.
- Fill container does not apply to top-level auto layout frames.
- Use grid for dashboards and galleries where wrap cannot express two-dimensional alignment.

## Verify
- [ ] Parents have a width (fixed or fill) so wrap and fill behave.
- [ ] Min/max protect readability and button sizes.
- [ ] Ignore-auto-layout elements are intentional.

## Checked
2026-11-01. Confirmed on the Figma Help Center pages Explore auto layout properties and Use the grid auto layout flow: wrap behaviour, min/max menu items, auto gap options, Ignore auto layout rename, grid track sizing, spanning, gaps, plan availability. Removed: example breakpoint widths, pixel examples, stroke include/exclude, canvas stacking, the "hug parent collapses" gotcha and the pattern recipes, which neither page stated.
Method: documentation only; no commands were run.
