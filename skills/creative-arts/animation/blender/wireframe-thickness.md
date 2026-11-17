---
id: creative-arts.animation.blender.wireframe-thickness
name: wireframe-thickness
category: creative-arts
field: animation
product: blender
tags: [blender, wireframe-thickness, wireframe-boundary, wireframe-modifier, modifiers, holographic, cage-render, even-thickness, replace-original]
level: practitioner
status: docs-checked
description: "Render real wireframe geometry with Blender's Wireframe modifier: thickness, even/relative, boundary, replace original, material offset, crease and vertex-group thickness."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/wireframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# wireframe-thickness

Goal: turn every edge into a solid strut — for technical/holographic renders, lattices, cages, 3D-printable wire sculptures — without hand-modelling struts.

## Fields

The modifier turns a mesh into a wireframe by collecting all edges of its faces and turning them into four-sided polygons, so the mesh needs faces.

- **Thickness**: the depth or size of the wireframe.
- **Offset** (-1 to 1): whether the wireframe is generated inside or outside of the original mesh; zero centres it on the original edges.
- **Boundary**: creates wireframe on mesh island boundaries.
- **Replace Original**: replaces the original mesh with the wireframe; when off, the wireframe is generated on top of the original.
- **Even Thickness**: maintains thickness by adjusting for sharp corners; sometimes improves quality but increases computation time. The manual warns that thickness is an approximation and skinny faces can cause spikes (reduce extreme angles or turn Even off).
- **Relative Thickness**: edge thickness follows edge length; longer edges are thicker.
- **Crease Edges** + *Crease Weight* (0 to 1): intended for use with a following Subdivision Surface modifier, creasing edges at junctions to prevent large curved intersections.
- **Material Offset**: uses the chosen material index for the wireframe, applied as an offset from the first material.
- **Vertex Group** (+ *Factor*, *Invert*): the group weights are multiplied onto the Thickness; vertices not in the group count as weight zero. Factor 0 uses the weights fully, 0.5 makes zero-weight vertices half as thick, 1.0 ignores the weights. Note: a vertex whose final thickness is zero still generates wireframe, creating duplicate geometry.

Stack (practice): `(Triangulate →) Wireframe → Subdivision (optional, with Crease Edges)`. Modifier order changes the result: Wireframe after a Subdivision Surface produces the wire of the subdivided mesh, while before it the wire follows the base cage.

## Recipes

These recipes are practice, not from the manual; tune values by eye.

- **Holographic object**: duplicate the object; on the duplicate use Wireframe (Replace Original, a small Thickness, Material Offset 1) with an emission material; the original gets a transparent or glass shader.
- **Low-poly art lattice**: Decimate, then Wireframe with Replace Original, Even Thickness and Boundary, then a Subdivision Surface level.
- **Printable wire sculpture**: choose a thickness your printer can print and check the result for thin struts (see `creative-arts.animation.blender.mesh-analysis-overlay`).

## Gotchas

- Very thin struts may vanish at render resolution; check at final resolution (practice).
- Dense meshes make heavy wireframes; Decimate first or consider Freestyle/Line Art (`creative-arts.animation.blender.freestyle`) (practice).
- With *Replace Original* off and the same material on both, the wire and surface can fight visually; use a Material Offset or Offset (practice).
- Inconsistent normals can make the Offset direction vary between faces (practice); check with the Face Orientation overlay.

## Verify

- Material Preview shows the wire in the Material Offset slot's material and the surface in slot 1.
- Compare thickness at acute and 90 degree corners with Even Thickness on and off.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/generate/wireframe.rst: every option listed above, the approximation warning, vertex group Factor behaviour and the zero-thickness duplicate-geometry note. Wrong claim fixed: a zero vertex-group weight does not remove the strut (it still generates wireframe). Removed the 0.02 default, ngon, pixel and 500k claims and the numeric recipe values.

Method: documentation only; no commands were run.
