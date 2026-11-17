---
id: creative-arts.animation.vector-graphics.boolean-path-operations
name: boolean-path-operations
category: creative-arts
field: animation
product: vector-graphics
tags: [boolean-ops, pathfinder, union, difference, intersection, vector-drawing, shape-building]
level: practitioner
status: docs-checked
description: "Combine vector shapes with boolean operations (union, difference, intersection, exclusion, division) as named in Inkscape's Path menu, plus non-destructive habits."
sources:
  - https://inkscape-manuals.readthedocs.io/en/1.1/boolean-operations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Boolean path operations

Boolean operations build complex shapes from simple ones: circles and rectangles combine into characters, props and icons with clean edges.

## Operations (Inkscape Path menu)
Select two or more objects, then choose the operation from the Path menu. If it fails, the status bar shows why.

| Operation | Result |
|---|---|
| Union | Combined outline of all selected paths |
| Difference | Removes one path's area from another |
| Intersection | Only the area shared by all selected paths |
| Exclusion | Areas covered by an odd number of paths (with two objects, the non-overlapping parts) |
| Division | Cuts the lower path into pieces along the upper path |
| Cut Path | One path for each crossing between the two paths |
| Combine | Keeps all parts and merges them into one object |
| Break Apart | Splits a multi-subpath object into one object per subpath |

Stacking order matters: put the shape you want to cut at the bottom and the cutting shape above it. Other
applications (Illustrator's Pathfinder, Animate's Combine Objects) offer similar commands under different names and
with their own rules; check that application's help rather than assuming the table above.

## Habits
1. **Duplicate first**: keep an original copy of the source shapes on a hidden layer so you can redo a cut.
2. **Order the stack** before a difference.
3. **Clean up** after: stray nodes, tiny slivers and duplicate points are common results. Use Simplify gently or remove nodes manually (`pen-tool-and-bezier-handle-discipline.md`).
4. Check that the result is a single closed path where you need a rig part or fill.

## Verify
- [ ] The result shows no slivers or hairline gaps at high zoom.
- [ ] Source shapes kept for later changes.

## Checked

2026-11-01. Confirmed in the Inkscape manual (Boolean Operations, 1.1 mirror): the Path menu operations and their
meanings listed above, and that stacking order matters. Removed because Adobe help pages were blocked (HTTP 403) and
could not be read: all Illustrator Pathfinder and Animate Combine Objects button lists and shortcuts; also removed the
"non-destructive path effects" advice, which the page does not mention.
Method: documentation only; no commands were run.
