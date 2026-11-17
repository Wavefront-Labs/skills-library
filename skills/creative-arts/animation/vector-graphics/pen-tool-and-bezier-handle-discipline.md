---
id: creative-arts.animation.vector-graphics.pen-tool-and-bezier-handle-discipline
name: pen-tool-and-bezier-handle-discipline
category: creative-arts
field: animation
product: vector-graphics
tags: [pen-tool, bezier, vector-drawing, anchor-points, handles, paths, illustrator, inkscape]
level: practitioner
status: draft
description: "Draw clean vector curves with the pen tool: anchor placement at extrema, handle length and angle, smooth versus corner nodes, minimal nodes and fixing lumpy paths."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
  - https://inkscape.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pen tool and bezier handle discipline

Clean curves animate, deform, scale and trace better than lumpy ones. The same rules apply in Adobe Animate and Illustrator (Pen tool) and Inkscape (Bezier tool and Node tool).

## The rules
1. **Few nodes.** Use as few anchor points as the shape needs. A simple arc is two nodes, not eight. Extra nodes cause lumps and cost you in rigging and tweening.
2. **Place nodes at extrema.** Put anchors at the top, bottom, left and right turning points of a curve, not mid-slope. Then use the handles to shape the curve between them.
3. **Handles lie along the tangent.** At an extremum, handles should be horizontal or vertical. A smooth node's two handles form a straight line through the anchor.
4. **Handle length is about a third** of the distance to the next anchor as a starting point. Very short handles make flat corners; very long handles overshoot into loops.
5. **Smooth versus corner:** use smooth nodes (collinear handles) for continuous curves and corner/cusp nodes (independent handles) only for real sharp points.
6. **Draw forward**, click-drag at each anchor in the direction the curve is going, rather than placing then fixing.
7. Close shapes deliberately so fills have no gaps; make sure the end node snaps onto the start node.

## Per-app notes
- **Illustrator/Animate**: Pen tool click-drag to create smooth points; use the Convert Anchor Point tool or the Alt/Option modifier to change a node's type. Animate also offers the Subselection tool for node and handle editing.
- **Inkscape**: Bezier tool (B) to draw; Node tool (N) to edit. In the Node tool, Shift+C makes a node cusp, Shift+S smooth, Shift+A auto-smooth. Check shortcuts in your version's keyboard reference.

## Fixing a lumpy curve
- Delete nodes between extrema and re-pull handles.
- Use the app's Simplify command only as a first pass; it can leave extra nodes and distort the shape, so inspect afterwards.

## Verify
- [ ] Curves have anchors only at extrema and corners.
- [ ] Handles at extrema are horizontal/vertical.
- [ ] No overshoot loops or kinks at 400% zoom.
