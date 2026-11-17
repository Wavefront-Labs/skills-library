---
id: creative-arts.animation.vector-graphics.centerline-tracing-for-line-art
name: centerline-tracing-for-line-art
category: creative-arts
field: animation
product: vector-graphics
tags: [centerline-trace, centerline, autotrace, vectorization, line-art, single-stroke, trace-bitmap]
level: practitioner
status: docs-checked
description: "Trace line art to single-stroke centrelines instead of outlines: when to choose it, the Inkscape Centerline tracing mode, results check and limits."
sources:
  - https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Centerline tracing for line art

Standard tracing (Potrace, Inkscape Trace Bitmap in Brightness cutoff mode) creates a silhouette-like **filled outline** that follows the shape of the image (`potrace-vectorisation.md`). **Centerline tracing** reduces a shape to an open path, a single stroke down the middle of each line, which is editable and re-weightable.

## When to use
- Handwritten text and other line drawings, where you want to change stroke width or colour afterwards. The Inkscape manual says Centerline tracing (autotrace) is best used with these.
- A rough pass to feed into a clean-up (`line-cleanup-and-inbetween-passes.md`).

## Tools
- **Inkscape**: Path > Trace Bitmap, Single scan tab, *Centerline tracing (autotrace)*. Use Update to refresh the preview, then apply to create the vector object. The manual compares the same letter traced with Brightness cutoff (outline) and Centerline tracing (open path).
- The *Autotrace* single-scan mode traces object outlines like Brightness cutoff; it is the separate *Centerline tracing (autotrace)* mode that gives open paths.

## Check the result
- Stroke follows the middle of each line; no spurs at junctions.
- Closed shapes are closed; endpoints are not left dangling.
- Node count is reasonable (`trace-cleanup-and-node-reduction.md`).

## Limits
- Variable-width lines lose their width: you get a uniform stroke; re-apply width afterwards (`variable-width-strokes.md`).
- Crossings and thick areas can produce messy junctions (check them by eye).

## Verify
- [ ] Overlay the trace on the source at 400%.
- [ ] Spot-check junctions and endpoints.

## Checked

2026-11-09. Confirmed against the Inkscape manual "Tracing an image" page (Trace Bitmap workflow, Autotrace and Centerline tracing (autotrace) mode descriptions, outline versus centerline figure). Removed unconfirmed claims: autotrace command-line flags, Illustrator Image Trace strokes option, scan dpi and line-width preprocessing numbers.
Method: documentation only; no commands were run.
