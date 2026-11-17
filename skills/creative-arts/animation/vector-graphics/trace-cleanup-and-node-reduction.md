---
id: creative-arts.animation.vector-graphics.trace-cleanup-and-node-reduction
name: trace-cleanup-and-node-reduction
category: creative-arts
field: animation
product: vector-graphics
tags: [trace-cleanup, node-reduction, simplify, vectorization, path-optimisation, anchor-points, svg]
level: practitioner
status: draft
description: "Clean up traced vector art: remove specks, reduce nodes, merge colours, smooth curves with Simplify safely, and validate the result for rigging or export."
sources:
  - https://inkscape.org/
  - https://potrace.sourceforge.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Post-trace node reduction and cleanup

Automatic tracing creates many nodes and tiny specks. Clean it before it enters an animation rig or production export.

## Steps
1. **Despeckle**: delete tiny stray shapes (dust, stray pixels). Many tracers have a speck-size parameter (for Potrace, `turdsize`); set it before tracing if you can (`potrace-vectorisation.md`).
2. **Merge**: unite adjacent shapes of the same colour (`boolean-path-operations.md`), delete hidden shapes beneath others.
3. **Simplify**: Inkscape Path > Simplify (Ctrl+L); Illustrator Object > Path > Simplify. They reduce nodes by fitting curves within a tolerance. Do this in small steps and compare; heavy simplification rounds off corners and shifts lines.
4. **Fix corners**: Re-add sharp corners lost to smoothing (`pen-tool-and-bezier-handle-discipline.md`).
5. **Align** edges that should touch so no hairline gap remains; overlap slightly beneath the top shape instead.
6. **Name and group** by region, such as `skin`, `hair`, `outline`, for rigging.
7. **Optimise for export** (`vector-asset-optimisation-for-animation.md`): reduce decimal precision, remove metadata.

## Checks
- Count nodes before and after; aim for a large reduction with no visible change.
- Overlay the cleaned result on the source and flip between the two.
- Test a deformation or a scale-up to 300%.

## Gotchas
- Simplify can change shape; never run it on the only copy.
- Over-aggressive node removal makes ugly curves; remove nodes manually at extrema instead.

## Verify
- [ ] Node count reduced, visible shape unchanged at 400%.
- [ ] No stray specks or hairline gaps.
- [ ] Layers or groups named for rigging.
