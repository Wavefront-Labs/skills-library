---
id: creative-arts.graphic-design.adobe-illustrator.shape-builder-tool
name: shape-builder-tool
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, shape-builder, shape-builder-tool, merge-shapes, delete-regions, gap-detection, geometric-construction, logo-construction]
level: practitioner
status: draft
description: "Build complex shapes in Illustrator by merging and deleting regions with Shape Builder: drag to merge, Alt to delete, gap detection, and when Pathfinder is better."
sources:
  - https://helpx.adobe.com/illustrator/using/building-new-shapes-using-shape.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shape Builder tool

**Goal:** turn overlapping circles, rectangles and lines into clean final shapes (logos, icons,
geometric illustrations) intuitively.

## Basic use
1. Draw the construction shapes overlapping: circles, rectangles, lines (lines split shapes too).
2. **Select all** the shapes involved (Shape Builder only works on the selection).
3. Shape Builder (**Shift+M**). Hovering highlights regions (mesh pattern).
   - **Click-drag across regions** to merge them into one shape.
   - **Alt/Option+click or drag** to delete regions (or edges).
   - Shift+drag draws a marquee to merge many regions at once.
4. The result is real paths; construction shapes not touched remain as separate pieces - delete leftovers.

## Options (double-click the tool)
- **Gap Detection:** treats small gaps between paths as closed (Small/Medium/Large or custom) - useful
  for line-art illustrations that do not quite close.
- **Consider Open Filled Path as Closed.**
- **In Merge Mode, Clicking Stroke Splits the Path.**
- **Pick Color From:** Color Swatches (cursor swatch, arrow keys cycle swatches) or Artwork; merged
  region takes the colour of the first region dragged from.
- **Highlight:** Fill / Stroke editable highlighting.

## Shape Builder vs Pathfinder
- Shape Builder: interactive, region-by-region, best for construction and logos.
- Pathfinder (Unite, Minus Front, Intersect, Exclude, Divide): precise one-click operations on whole
  shapes; Alt/Option+click makes compound shapes that stay editable (see pathfinder skill).
- Live alternative: **Live Paint** (colouring regions without merging, see live paint skill).

## Logo construction workflow
Build the mark from geometry (circles on a grid), Shape Builder to merge/delete, then check curves
(the junctions between arcs can produce tiny kinks - inspect in Outline mode, Ctrl/Cmd+Y), and
apply optical corrections afterwards (see optical refinement skill).

## Gotchas
- Unselected shapes are ignored; selected but unwanted shapes get split - select only what you need.
- Strokes are treated as edges, not as their visible width - outline strokes first if you want
  the stroke's shape.
- Many tiny regions (slivers) appear where shapes almost meet; zoom in and merge or delete them.

## Verify
- [ ] Outline mode shows clean single paths with no slivers or overlapping duplicates.
- [ ] Final shapes have the intended fills; construction leftovers removed.
