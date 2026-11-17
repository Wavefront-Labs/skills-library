---
id: creative-arts.design-for-form-and-experience.concept-design.tracing-reference-images-with-sketch-picture-in-solidworks
name: tracing-reference-images-with-sketch-picture-in-solidworks
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [sketch-picture, image-tracing, reference-image, solidworks-surfacing, concept-to-cad]
level: practitioner
status: draft
description: "Place, scale and trace a reference image in SOLIDWORKS with Sketch Picture, then draw splines over it without letting the image distort the model."
sources:
  - "SOLIDWORKS Help (help.solidworks.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sketch Picture tracing

Use a side or top view of a concept to drive CAD curves.

## Steps
1. Open a sketch on the plane matching the image view (Front for a side view, and so on).
2. **Tools > Sketch Tools > Sketch Picture**; choose your image. Use an orthographic image (side, front or top) if you want true proportions, not a perspective sketch.
3. In the PropertyManager set **origin**, **size** (keep aspect ratio) and **rotation**, and use **transparency** so geometry shows against the image.
4. **Scale it:** draw a reference line over a known dimension (overall length) and size the picture so it equals the real value; check a second dimension.
5. Trace with **splines** using few control points and check curvature combs; use lines and arcs on straight or round areas.
6. Hide or delete the picture when done, or keep it in a separate reference sketch.

## Gotchas
- Perspective drawings give wrong proportions; build orthographic views first.
- Too many spline points create wavy surfaces.
- Resizing the picture after tracing moves the image but not the curves; scale first.

## Verify
- [ ] A measured reference dimension matches the real number.
- [ ] Splines have few points and smooth curvature combs.
- [ ] The picture is hidden or isolated before surfacing.
