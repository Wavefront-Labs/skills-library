---
id: creative-arts.fashion-design.clo-3d.topstitch-and-puckering
name: topstitch-and-puckering
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-trims, 3d-trims, clo-topstitch, clo-puckering, stitch-library, segment-topstitch]
level: practitioner
status: draft
description: "Add topstitching in CLO 3D: segment and free topstitch tools, stitch presets and parameters (length, spacing, thread), multiple rows, and controlled seam puckering."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Topstitch and puckering in CLO

**Goal:** visible stitching that matches the tech pack, and realistic puckering where seams
draw in.

## Applying
- **Segment Topstitch** tool: click a segment to apply the current topstitch preset along it.
- **Free Topstitch**: start and end points anywhere along edges.
- Topstitch on internal lines for decorative stitching.
- Library presets (single, double, triple, coverstitch looks); create custom presets.

## Parameters (Property Editor)
- Stitch **length**, **thickness/thread**, colour, **distance from edge** (e.g. 1.5-6 mm),
  **number of lines** and spacing between lines (twin needle 6 mm).
- 3D geometry or texture-based stitch; displacement for depth in renders.
- Match tech pack SPI: e.g. 10 SPI = 2.54 mm stitch length.

## Puckering
- Topstitch properties include **Puckering** (intensity, interval/spacing) that pulls the
  fabric slightly along the stitch, imitating seam pucker, especially on denim and
  outerwear.
- Use subtly; heavy pucker looks like poor quality unless that's the intent (washed denim).

## Workflow tips
- Apply topstitch after fit is settled; changing patterns can misplace stitches.
- Save brand-standard presets (e.g. "Denim twin 6mm, 8 SPI, 30-weight gold thread").

## Gotchas
- Topstitch on wrong side of a seam (wrong offset direction) looks odd; flip side.
- Very fine stitches render poorly at low texture resolution.
- Puckering on all seams makes garments look cheap.

## Verify
- [ ] Stitch distance, rows and length match the tech pack.
- [ ] Presets saved for reuse.
- [ ] Puckering only where intended.
