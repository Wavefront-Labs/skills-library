---
id: architecture-construction.landscape-architecture.grading-drainage-design.contour-grading-spot-elevations-and-surface-drainage
name: contour-grading-spot-elevations-and-surface-drainage
category: architecture-construction
field: landscape-architecture
product: grading-drainage-design
tags: [grading-drainage-design, grading, grading-plan, contour-grading, contours, spot-elevations, spot-levels, slope, gradient, percent-slope, falls, cross-fall, crown, interpolation, ridge, swale, valley, high-point, low-point, cut-and-fill, earthworks-balance, positive-drainage, building-threshold, damp-proof-course, dpc, accessible-route, ramp-gradient, channel-drain, gully, catch-basin, surface-water, landscape-architecture]
level: practitioner
status: draft
description: "Grade a site with contours and spot levels: slope maths, falls by surface, drainage away from buildings, swales and ridges, accessible gradients, and checking cut and fill."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contour grading, spot elevations and surface drainage

**Goal:** proposed levels that drain every surface positively to a defined outlet,
keep water away from buildings, meet accessibility gradients, and roughly balance
earthworks.

## 1. The maths you use every day
- **Gradient** = rise ÷ run. As a ratio (1:50), percent (2%) or degrees — convert:
  1:50 = 2%; 1:20 = 5%; 1:12 ≈ 8.3%.
- **Contour spacing** for a slope: horizontal distance = contour interval ÷ gradient.
  At 0.5 m contours and 1:20 slope, contours are 10 m apart.
- **Interpolation:** level at a point between two spots = level₁ + (distance from
  point 1 × gradient). Check every pair of adjacent spots gives the intended slope.

## 2. Typical falls (rules of thumb; check local standards and products)
- Hard paving: ~1:40–1:60 (1.7–2.5%) to drain; never flatter than ~1:80 on
  unsealed or textured surfaces. Large-format smooth paving can be flatter only with
  precise laying.
- Lawn: ~1:50–1:30 to shed water; steeper than ~1:3 is hard to mow.
- Planting beds: minimal fall required, but don't let them pond against buildings.
- Swales: longitudinal ~1:100–1:50, side slopes ~1:3–1:4 for mowing and safety.
- **Accessible routes:** ≤ 1:20 counts as a level route in many codes; ramps
  ~1:12–1:20 with landings, cross-falls ≤ ~1:40–1:50 (ADA: 1:48). Check your code.

## 3. Building interface
- Fall **away from buildings** for at least the first few metres (e.g. 1:40–1:60);
  ground levels typically ~150 mm below damp-proof course (DPC) in UK practice except
  at level thresholds, which need a drainage channel and detailed design.
- Spot level every door threshold, top of step, ramp start/end and landing.

## 4. Drawing the grading plan
1. Fix the givens: building finished floor levels, existing levels at boundaries
   (you usually can't change the neighbour), road/kerb levels, outfall inverts.
2. Set **high points and low points**; decide where water goes (drains, swales,
   rain gardens, permeable paving).
3. Place **spot elevations** at corners, changes of grade, drains, walls (TW/BW),
   steps, and along centrelines.
4. Draw proposed contours that tie into existing contours where grading ends.
   Contours point **uphill in valleys/swales** and **downhill on ridges**.
5. Add **fall arrows** with gradients on paving.
6. Check: no surface traps water (closed contour loops are hollows unless they're
   intentional basins), every low point has an outlet.

## 5. Cut and fill
- Compare proposed vs existing surfaces (grid method, end-area method, or software
  surfaces). Aim to balance on site where possible — exporting or importing soil is
  costly. Allow for topsoil strip and re-spread, and bulking/compaction factors
  (vary by soil; get geotechnical advice for anything large).

## Gotchas
- Spot levels that contradict each other (uphill fall arrows).
- Paving at 1:100 that ponds once laid with normal tolerance.
- Grading that dumps water on the neighbour.
- Level threshold with no channel drain.

## Verify
- [ ] Every adjacent spot pair gives the intended gradient.
- [ ] All surfaces drain to a defined outlet; no unintended closed contours.
- [ ] Falls away from buildings; thresholds detailed.
- [ ] Accessible routes within gradient and cross-fall limits.
- [ ] Cut/fill volumes calculated and reviewed.
