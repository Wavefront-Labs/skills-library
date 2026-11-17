---
id: creative-arts.design-for-form-and-experience.figma.vector-networks-and-boolean-operations
name: vector-networks-and-boolean-operations
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [vector-networks, boolean-operations, figma-vector, pen-tool, union-subtract-intersect, flatten, outline-stroke, figma]
level: practitioner
status: draft
description: "Draw and combine vectors in Figma: vector networks with the pen and bend tools, boolean union, subtract, intersect and exclude, flatten, outline stroke and path hygiene."
sources:
  - "Figma Help Center - Vector networks and the pen tool (help.figma.com/hc/en-us/articles/360040450133)"
  - "Figma Help Center - Boolean operations (help.figma.com/hc/en-us/articles/360039957634)"
  - "Figma Help Center - Edit vector shapes: flatten, outline stroke, offset path (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector networks and boolean operations

## Vector networks
Figma uses **vector networks**: points can connect to any number of other points (not a single path), so branching shapes and strokes meeting at a node need no overlapping paths.
- **Pen tool (P):** click for corners, click-drag for curves; **Enter** to edit, **Esc** to finish; **Shift** constrains angles; click an existing point to continue a path. **Bend tool** (from the pen tool menu): drag a corner point to turn it into a curve; double-click a point to toggle corner and smooth.
- **Edit mode (Enter on a vector):** select points, **Delete** removes the selected point or segment (**Backspace** the segment), drag handles; **Ctrl/Cmd+Alt+drag** to break handles; **Shift+click** multi-select.
- **Corner radius** per point; **stroke** properties (cap, join, dash, align inside/outside); **Pencil tool (Shift+P)** with **Simplify** to reduce points.

## Boolean operations
Select two or more shapes, **Union, Subtract, Intersect, Exclude** (Layer > Boolean groups, or the toolbar). Boolean groups stay **editable** (individual shapes keep position and properties; order and operation can change).
- **Union** merges outlines; **Subtract** removes the top shapes from the bottom shape; **Intersect** keeps overlapping area; **Exclude** keeps non-overlapping.
- **Flatten (Ctrl/Cmd+E)** turns a boolean group or multiple layers into one vector (not editable as a boolean any more); do it for export or performance.
- **Outline stroke (Ctrl/Cmd+Shift+O)** converts a stroke to a filled shape (for icons and scaling uniformly); **Offset path** expands or contracts.

## Practices for icons and logos
- Build from simple shapes with booleans on a **pixel grid**; use **union** for solid forms, **subtract** for holes.
- Use **stroke** while designing, **outline stroke and flatten** for final export when strokes must not scale (`creative-arts.design-for-form-and-experience.design-systems.optimising-and-delivering-svg-icon-libraries`).
- Reduce nodes (clean paths); **fill rule** (non-zero vs even-odd) set in the fill options to avoid holes vanishing.
- Keep a copy of the editable boolean group before flattening.

## Gotchas
- Boolean groups with auto layout parents can shift; place booleans in their own frame.
- Text must be **outlined** (Create outlines, Ctrl+Shift+O) to include in booleans.

## Verify
- [ ] Shapes cleanly combine with minimum nodes; editable originals kept.
- [ ] Final icons flattened and aligned on the grid; fill rule correct.
