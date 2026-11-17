---
id: creative-arts.graphic-design.adobe-illustrator.gradients-linear-radial-freeform
name: gradients-linear-radial-freeform
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, gradient-tool, freeform-gradient, linear-gradient, radial-gradient, gradient-on-stroke, gradient-annotator, gradient-banding]
level: practitioner
status: draft
description: "Make Illustrator gradients: linear and radial with the annotator, gradients on strokes, freeform points and lines, swatch-based stops and print-safe practice."
sources:
  - https://helpx.adobe.com/illustrator/using/gradients.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gradients: linear, radial and freeform

**Goal:** smooth, controllable gradients that stay editable and print cleanly.

## Linear and radial (Window > Gradient, Ctrl/Cmd+F9)
- Type: Linear or Radial; click a stop to set its colour (double-click opens swatches/colour picker),
  drag stops and midpoint diamonds; drag a swatch onto the slider to add a stop; drag a stop off to remove.
- Stop **opacity** and **location** fields for precision; Angle; aspect ratio for elliptical radials.
- **Gradient tool (G):** drag on the object to set direction and length; the on-object **annotator**
  lets you move stops directly. Shift constrains to 45 degree steps.
- Apply one gradient across several objects: select them all, drag with the Gradient tool across.
- Save as a swatch (drag the gradient thumbnail into Swatches).

## Gradients on strokes
Select the stroke, apply gradient, choose: **within stroke**, **along stroke** (follows the path, great
for neon tubes or ribbons) or **across stroke**.

## Freeform gradients
Type: Freeform. **Points** mode: click inside the shape to add colour points, drag to move, set each
point's colour and spread. **Lines** mode: click to draw a path of colour points - colour follows the
line. Natural, painterly shading for illustrations, mesh-like results without mesh complexity.

## Consistency and colour
- Use **global swatches** for stop colours so brand gradients update with the palette.
- Avoid interpolating complementary colours directly (muddy middle); add an intermediate stop.

## Print and export
- Long subtle gradients can band in print; set Document Raster Effects to 300 ppi; add slight noise
  only in raster contexts. Avoid tiny colour differences over long distances.
- Spot-to-white gradients separate as tints of one plate (good). Spot-to-spot gradients need checking in Separations Preview.
- SVG supports linear/radial; **freeform gradients export as raster** (embedded images) in SVG - avoid freeform for web icons.

## Gotchas
- Gradient angle is relative to the object when "Edit Gradient" is used on rotated objects; check after transforms.
- Gradient mesh (see that skill) is a different, heavier tool for photorealistic shading.

## Verify
- [ ] Stops use swatches; no muddy midtones.
- [ ] Separations and SVG output behave as expected for the target medium.
