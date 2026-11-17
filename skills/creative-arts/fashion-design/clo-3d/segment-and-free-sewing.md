---
id: creative-arts.fashion-design.clo-3d.segment-and-free-sewing
name: segment-and-free-sewing
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-sewing, sewing-lines, segment-sewing, free-sewing, sewing-direction, clo-edit-sewing]
level: practitioner
status: draft
description: "Sew pattern pieces in CLO 3D with Segment Sewing and Free Sewing: picking segments, direction, sewing across multiple segments, editing and checking sewing lengths."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Segment and free sewing in CLO

**Goal:** connect pattern pieces correctly so the garment assembles on the avatar the way
it would be sewn.

## Segment Sewing (N)
- Click one pattern **segment** (edge between two points), then the matching segment on
  the other piece. Whole segments are sewn end to end.
- Click near the **same end** on both segments to set direction; the preview line shows the
  pairing. Wrong direction = twisted sewing.
- Best for edges that match point-to-point (side seams, shoulder seams).

## Free Sewing (M)
- Click a start point and an end point along any edge (not limited to segment ends), then
  the same on the other piece.
- Use when seams don't match whole segments (sewing a sleeve cap to part of an armhole,
  attaching a collar between notches).
- Hold Shift (in recent versions) to continue across multiple segments.

## Editing
- **Edit Sewing (B)**: select sewing lines to delete, reverse direction (right-click >
  Reverse Sewing), or adjust.
- Sewing lines are colour-paired; matching colours show which pairs belong together.
- Check length difference: the Property Editor or the sewing line info shows lengths of each
  side; large differences create gathers or puckers.

## Order and tips
- Arrange pieces on arrangement points first, then sew.
- Sew symmetrical pieces once if pattern symmetry is linked (sewing copies).
- Use notches as points to free-sew between.

## Gotchas
- Sewing the cut line instead of the sew line (in imported DXF) makes garments too big.
- Unintended length mismatches gather fabric where you didn't want it.
- Sewing edges to themselves or crossing seams causes simulation explosions.

## Verify
- [ ] Every seam sewn with correct direction (no crossed lines).
- [ ] Length differences only where ease/gathers are intended.
- [ ] Garment simulates without twisting.
