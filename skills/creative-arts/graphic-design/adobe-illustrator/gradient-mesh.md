---
id: creative-arts.graphic-design.adobe-illustrator.gradient-mesh
name: gradient-mesh
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, gradient-mesh, mesh-tool, mesh-points, create-gradient-mesh, photorealistic-vector, vector-shading]
level: advanced
status: draft
description: "Build photorealistic vector shading with Illustrator gradient mesh: creating meshes, colouring mesh points, simple grids, and when freeform gradients are better."
sources:
  - https://helpx.adobe.com/illustrator/using/meshes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gradient mesh

**Goal:** smooth, multi-directional colour transitions on vector shapes (product renders, fruit,
fabric folds) that scale without loss.

## Create a mesh
- **Mesh tool (U):** click inside a filled shape to add a mesh point; each click adds a row and column line.
- **Object > Create Gradient Mesh:** enter rows/columns and appearance (Flat, To Center, To Edge,
  highlight %) for a regular grid - good starting point for simple forms.
- Start with **few lines** (2-4 each way). Dense meshes are slow and hard to keep smooth.

## Colour the mesh
- Select a mesh point with Direct Selection (A) or the Mesh tool, then click a swatch or use the
  Eyedropper (I) to sample from a reference photo placed underneath.
- Select several points (Shift or lasso) to colour them together.
- Mesh **patches** (areas between four points) can also be coloured by clicking inside with Direct Selection.
- Point **opacity** can be set (Illustrator CS5+): soft shadows and glows that fade into the background.

## Shape the transitions
- Move mesh points and their handles like path points; follow the form's contours (lines should flow
  around the object's curvature, like latitude/longitude on a sphere).
- Alt/Option+click a point with the Mesh tool to delete it.
- Build complex objects from several simple mesh objects (body, highlight, shadow) rather than one huge mesh.

## When not to use mesh
- Simple shading: **freeform gradients** are easier and lighter (see gradients skill).
- Photorealism at fixed size: Photoshop is faster.
- Web/SVG: meshes export as raster images; avoid for SVG.

## Gotchas
- Mesh objects cannot have strokes (the stroke is dropped); keep outlines as separate paths.
- Text and compound paths cannot become meshes directly; Expand / release compound paths first.
- Printing complex meshes is slow on some RIPs; flatten/rasterise at high res for problematic print workflows.

## Verify
- [ ] Mesh lines follow the form; no lumps or kinks in transitions at 400%.
- [ ] Point count minimal for the result; file remains responsive.
