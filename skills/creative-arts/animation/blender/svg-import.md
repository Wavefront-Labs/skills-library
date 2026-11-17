---
id: creative-arts.animation.blender.svg-import
name: svg-import
category: creative-arts
field: animation
product: blender
tags: [blender, svg-import, svg-to-curve, pdf-import, grease-pencil, import-export, logos, curves]
level: practitioner
status: docs-checked
description: "Bring vector art into Blender: SVG as Curves (scale, fill, layers as collections), SVG/PDF to Grease Pencil, cleaning imports, and turning logos into extruded 3D."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/svg_curve.html
  - https://docs.blender.org/manual/en/latest/files/import_export/grease_pencil_svg.html
  - https://docs.blender.org/manual/en/latest/files/import_export/grease_pencil_pdf.html
  - https://docs.blender.org/manual/en/latest/modeling/curves/properties/geometry.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# svg-import

Goal: a logo or illustration from Illustrator/Inkscape becomes clean Blender curves or Grease Pencil strokes ready to extrude or animate.

## SVG as curves (File > Import > Scalable Vector Graphics (.svg))

- The importer reads SVG path geometry as one or more curve objects (each path typically becomes a spline). The manual states that gradients, fills, strokes, text objects, images and filters are ignored.
- Curves are created in the XY plane and scaled according to the SVG document units; extra scaling or orientation fixes may be needed (select all, set the origin, scale and apply).

## SVG/PDF to Grease Pencil

- File > Import > SVG as Grease Pencil: *Resolution*, *Scale*, *Scene Unit*, *Center on Bounds*.
- Export: File > Export > Grease Pencil as SVG, and Export Grease Pencil as PDF (PDF is export only; both exporters work only in Object Mode).

## Clean-up for 3D

1. Join the curves (`Ctrl J`).
2. Object Data > Geometry: *Offset*, *Extrude* (turns the curve into a ribbon) and *Bevel* (depth and resolution).
3. Check the result from above; for closed shapes with holes keep the inner paths in the same object (practice).
4. Convert to mesh (`Object > Convert > Mesh`) for booleans or export, then clean up as needed.

## Gotchas

- Text, strokes, fills, gradients and filters are ignored by the curve importer (manual), so convert text and strokes to outlined paths in the source app before export.
- Self-intersecting paths may fill unexpectedly (practice); fix them in the vector app.

## Verify

View from top (Numpad 7): shapes match the source; after extrude, the shape looks correct from every side.

## Checked

Blender 5.2 manual (files/import_export: svg_curve, grease_pencil_svg, grease_pencil_pdf; modeling/curves/properties/geometry), read 2026-10-27.
- File > Import > SVG as Curves: path geometry only; gradients, fills, strokes, text, images and filters ignored; curves created in the XY plane and scaled by document units. SVG as Grease Pencil options (Resolution, Scale, Scene Unit, Center on Bounds); Grease Pencil export to SVG and PDF (PDF export only, Object Mode only). Curve Offset, Extrude and Bevel settings.
- Corrected: the old skill described fills, materials, a per-file collection and a 90-dpi scale for the curve importer, none of which the 5.2 manual supports; and claimed PDF import for Grease Pencil, which does not exist in the manual.

Method: documentation only; no commands were run.
