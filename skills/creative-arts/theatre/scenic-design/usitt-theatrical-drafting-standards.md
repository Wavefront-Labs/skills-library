---
id: creative-arts.theatre.scenic-design.usitt-theatrical-drafting-standards
name: usitt-theatrical-drafting-standards
category: creative-arts
field: theatre
product: scenic-design
tags: [theatre, scenic-design, ground-plan, usitt-drafting-standards, usitt, rp-2, line-weights, title-block, scale, drafting, plate-numbers, vectorworks-set-drafting, vectorworks]
level: practitioner
status: draft
description: "Draft scenery to USITT standards: line types and weights, title blocks, scales, symbols, dimensioning and sheet organisation, including setup in Vectorworks."
sources:
  - "https://www.usitt.org/resources/standards"
  - "https://www.vectorworks.net/spotlight"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USITT theatrical drafting standards

The USITT Recommended Practice for Theatrical Drafting (RP-2) defines conventions
for scenic drawings so shops and venues read them consistently. UK practice is
similar (ABTT/industry convention, metric scales).

## Sheets
- Standard sheet sizes (ANSI D 24x36" common; ISO A1/A2 in metric work).
- **Title block** (lower right or along the bottom/right edge): production,
  venue, drawing title, plate number, scale, date, designer, drafter, revision
  history, approval.
- **Plate numbering** by type (e.g. ground plan, section, elevations, details).
- Scales: 1/2" = 1'-0" for ground plans and elevations in US practice (1/4" for
  large venues); 1:25 or 1:50 metric; details at larger scales (1" = 1'-0",
  1:10, 1:5).

## Line types (RP-2)
- **Thick (heavy)**: outlines of objects/scenery, section cuts.
- **Thin**: dimension lines, extension lines, hidden lines (dashed), centre
  line (long-short dash with "CL" symbol), leaders.
- **Hidden** (dashed): edges not visible from the view, e.g. platforms under
  others.
- **Overhead** (long dash): flown or overhead scenery seen from above in the ground
  plan (borders, bars, flown units).
- **Setting line** and **centre line** labelled; plaster line where relevant.
- **Break lines** for shortened objects.
Two line weights (thin/thick) are standard; a medium weight is commonly added.

## Ground-plan conventions
- Centre line and setting line (or plaster line) as datums; dimensions from
  them.
- Platforms labelled with heights (+1'-6", or +450 mm) from stage floor.
- Masking, fly line set numbers listed in a lineset schedule.
- Arrows for direction of moving scenery; spike marks for multiple
  positions with scene numbers.

## Vectorworks set-up (Spotlight)
- Design layers for set, masking, lighting, venue; sheet layers with viewports
  at scale; classes for line types (e.g. "Set-Hidden", "Set-Overhead") with line
  styles matching RP-2; title block object with revision table.
- Use 2D/3D hybrid symbols for furniture; create sections via Section Viewports.
- Export PDF for shops; DWG for venues using AutoCAD.

## Gotchas
- Mixing scales on one sheet without labelling each view.
- Dimension chains that don't add up.
- No revision tracking — the shop builds from old drawings.

## Verify
- [ ] Every sheet has a complete title block and scale.
- [ ] Line types match RP-2 conventions with a legend.
- [ ] Dimensions referenced to centre/setting lines.
