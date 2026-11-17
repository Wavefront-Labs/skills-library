---
id: creative-arts.animation.blender.sculpt-trim-tools
name: sculpt-trim-tools
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, sculpt-trim-tools, trim-box, trim-lasso, trim-line, line-project, box-trim, hard-surface-sculpt]
level: practitioner
status: docs-checked
description: "Cut and add shapes in Blender sculpt mode with Box, Lasso, Line and Polyline Trim (difference, union, join; solver; depth modes), and use Line Project to flatten silhouettes."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/trim_tools.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/line_project.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/gesture_tools.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sculpt-trim-tools

Goal: boolean-like cuts and additions directly while sculpting (slicing off a plane, cutting holes, adding blocky forms), then remesh and carry on.

## Trim tools (Toolbar)

**Box Trim**, **Lasso Trim**, **Line Trim**, **Polyline Trim**: each performs a Boolean operation from the area of the matching gesture. New geometry gets a new Face Set; when removing, the new interior faces along the cut get a new face set. Line Trim supports only Difference, not adding geometry.

Tool settings:
- **Solver**: *Exact* (best results, handles overlapping geometry, slowest), *Float* (simple and fast, no overlap support), *Manifold* (usually fastest, manifold meshes only, plus Difference with a plane).
- **Trim Mode**: *Difference* removes geometry and fills the holes, *Union* adds geometry joined with the existing mesh, *Join* adds it as separate geometry without a Boolean.
- **Shape Orientation**: *View* or *Surface* (surface normal).
- **Extrude Mode**: *Fixed* (orthogonal, 90 degree depth) or *Project* (follows the view perspective for a taper).
- **Use Cursor for Depth**: uses the cursor location and radius for the shape's size and position; otherwise the shape spans the object's full depth from the camera.
- Hold Space while dragging to move the gesture area. Line gestures also have Flip (F), Snap (Ctrl) and Limit to Segment.

The manual advises against Difference or Union with the Exact solver on meshes above about 100k vertices because the Boolean can take a long time; use Line Project or the Fair Positions mode of Edit Face Set instead.

## Line Project

Flattens geometry along a plane defined by the camera view and a drawn line; the affected side is shaded. Orient the viewport for depth, hold LMB and move to set the line, adjust with controls, release to confirm. **Flip** (F) changes the side, **Snap** (Ctrl) constrains to 15 degree steps, **Ctrl-Space** repositions the line, **Limit to Segment** stops at the drawn length. Useful for flattening silhouettes such as ears or armour edges.

## Workflow

1. Block the form, then Box Trim Difference for large planes.
2. Voxel remesh to clean the boolean topology (Remesh panel, Voxel Remesh or Ctrl-R).
3. Smooth or Scrape the edges, or keep them sharp for hard-surface work.

## Verify

The mesh stays closed after the cut (voxel remesh succeeds without holes) and the cut looks planar viewed edge-on.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tools/trim_tools and line_project and introduction/gesture_tools: tool names, Line Trim difference-only, solver list (Exact, Float, Manifold; there is no Fast solver), Trim Mode, Shape Orientation, Extrude Mode, Use Cursor for Depth, 100k vertex advice, new face set assignment, Line Project controls (15 degree snap, Ctrl-Space). Removed the 4.2 version gates, Alt draw-from-centre, Front Faces Only and Multires limitation claims.
Method: documentation only; no commands were run.
