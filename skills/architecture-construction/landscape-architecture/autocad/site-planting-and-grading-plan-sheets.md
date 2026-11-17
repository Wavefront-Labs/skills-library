---
id: architecture-construction.landscape-architecture.autocad.site-planting-and-grading-plan-sheets
name: site-planting-and-grading-plan-sheets
category: architecture-construction
field: landscape-architecture
product: autocad
tags: [autocad, autocad-civil-3d, dwg, landscape-architecture, landscape-drawings, site-plan, planting-plan, grading-plan, hardscape-plan, layout-plan, setting-out, coordinates, survey-xref, topographic-survey, contours, spot-elevations, plant-symbols, plant-tags, plant-schedule, dynamic-blocks, attributes, dataextraction, hatch, layers, xrefs, viewports, landscape-construction-documents, lcs, tree-protection-plan]
level: practitioner
status: draft
description: "Produce landscape construction sheets in AutoCAD on a georeferenced survey: layout, planting plans with tagged blocks and auto plant schedules, grading with spots and contours, and details."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Site, planting and grading plan sheets in AutoCAD

**Goal:** a landscape drawing set where the plan sits on the real survey
coordinates, plant counts come from the drawing (not a tally by hand), and grading
reads clearly to the contractor.

## 1. Base set-up
- Xref the **topographic survey** at its real coordinates (don't move it to 0,0 — the
  contractor will set out from those coordinates). Check units (`INSUNITS`) and that
  a known survey point reads the same coordinates as the survey sheet.
- Xref the architect's building footprint, aligned to the survey by the architect's
  stated grid/coordinates. Check alignment on at least two points.
- If your office uses Civil 3D, surfaces and grading tools make spot levels and
  contours live; plain AutoCAD does the same drafting manually.

## 2. Layers by plan type
`L-HARD-PAVE`, `L-HARD-WALL`, `L-SOFT-TREE`, `L-SOFT-SHRB`, `L-SOFT-LAWN`,
`L-GRAD-SPOT`, `L-GRAD-CONT-PROP`, `L-GRAD-CONT-EXST` (dashed), `L-IRRG`,
`L-TREE-PROT`, `L-ANNO`. One model; each sheet's viewport freezes what it doesn't need.

## 3. Layout / setting-out plan
- Dimension hardscape from fixed points (building corners, survey stations) or give
  **coordinates** of key points (path centreline start/ends, radius centres) in a
  table. Radii and curves: give centre, radius and tangent points.
- Paving joints and material codes keyed to the details.

## 4. Planting plan with counted blocks
- Trees and specimen shrubs as **blocks** at mature canopy size (or a stated
  percentage of it) with an attribute for species code; shrub/perennial **beds**
  as hatched areas tagged with species code, density (plants/m²) and area.
- Use **DATAEXTRACTION** (or a script/LISP or Civil 3D tools) to count blocks by
  attribute and pull bed areas into the **plant schedule**: code, botanical name,
  common name, size at planting (pot size / girth / height), spacing, quantity.
  Bed quantities = area × density, rounded up.
- Tag style: species code + quantity at a leader to each group.
- Show existing trees to be retained with their **root protection areas** (e.g. per
  BS 5837 in the UK — typically radius 12 × stem diameter at 1.5 m, capped).

## 5. Grading plan
- Existing contours dashed and lighter; proposed contours solid, labelled at
  intervals. Spot elevations at building entries (threshold), top/bottom of walls
  (TW/BW), steps, drains, high points and changes in fall.
- Show **fall arrows** with gradients (e.g. 1:60) on paving, and drainage
  connections. See `architecture-construction.landscape-architecture.grading-drainage-design.contour-grading-spot-elevations-and-surface-drainage`.

## 6. Sheets and details
Details at 1:10 or 1:20 (paving build-ups, edges, tree pits, walls), keyed with
callouts. Plot to PDF; check symbol and text sizes at 100%.

## Gotchas
- Survey moved to 0,0 — setting-out coordinates lost.
- Counting plants by eye; schedule and plan disagree.
- Tree symbols drawn at planting size → over-planted in 10 years.
- Proposed and existing contours indistinguishable.

## Verify
- [ ] Survey coordinates confirmed on two points; architect's footprint aligned.
- [ ] Plant schedule quantities generated from blocks/areas and match tags.
- [ ] Every hardscape element dimensioned or coordinated.
- [ ] Spot levels at all thresholds, walls, steps and drains; falls labelled.
- [ ] Retained trees show protection areas.
