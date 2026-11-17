---
id: creative-arts.fashion-design.clo-3d.grading-in-clo
name: grading-in-clo
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-export, clo-grading, clo-grade, graded-patterns, size-run-3d, avatar-sizes]
level: practitioner
status: draft
description: "Grade garments in CLO 3D: importing graded DXF nests or setting grade rules, switching sizes, checking fit per size on matching avatars, and exporting graded patterns."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.astm.org/d6673-10r20.html
  - https://www.clo3d.com/en/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grading in CLO

**Goal:** check the whole size run virtually: each size on an avatar of that size, before
the size set sample.

## Getting graded patterns in
- **Import a graded DXF (AAMA/ASTM)** from the 2D CAD: CLO reads the size nest; choose the
  base size. This keeps production grading as the source of truth.
- Or grade in CLO: use the **Grading** feature to create a size list and grade rules
  (point movements per size) on pattern points; see the CLO manual for the version's grading
  editor.

## Switching and checking
1. Select the size from the size list; patterns update; garment re-simulates.
2. Set up **avatars per size** (avatar size editor to each size's body measurements from the
   brand size chart).
3. Simulate each size on its avatar; review fit maps (strain/stress), lengths, proportions
   of details (pocket placement, logos).
4. Note issues per size for the grading team (e.g. "XL: armhole too deep, reduce grade
   0.3 cm").

## Graphics and trims across sizes
Graphics and button positions may need per-size adjustment; check spacing (buttons may
need to change count on larger sizes).

## Exporting
Export graded patterns back as DXF for the CAD team if changes were made in CLO; keep a
single source of truth (communicate which system owns the grade).

## Gotchas
- Using one avatar for all sizes hides grading problems.
- Graphics fixed in mm may look too small on large sizes; decide scaling rules.
- Re-importing a DXF after CLO edits can overwrite sewing/trims; plan the round trip.

## Verify
- [ ] Each size simulated on a matching avatar.
- [ ] Fit issues logged per size.
- [ ] Source of truth for grading agreed.
