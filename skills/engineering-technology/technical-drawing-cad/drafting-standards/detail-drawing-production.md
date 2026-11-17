---
id: engineering-technology.technical-drawing-cad.drafting-standards.detail-drawing-production
name: detail-drawing-production
category: engineering-technology
field: technical-drawing-cad
product: drafting-standards
tags: [engineering-drawing, technical-drawing, detail-drawing, part-drawing, orthographic-projection, first-angle, third-angle, view-selection, section-views, hatching, auxiliary-view, detail-view, dimensioning, functional-dimensioning, tolerancing, general-tolerances, iso-2768, iso-22081, iso-128, iso-129, iso-5456, iso-3098, iso-7200, iso-5457, iso-21920, asme-y14.5, asme-y14.100, asme-y14.3, title-block, line-types, autocad, solidworks, inventor, creo, fusion-360]
level: practitioner
status: draft
description: "Make a manufacturable detail drawing: view selection, first/third-angle projection, sections, ISO 128 lines, functional dimensioning, general tolerances, title block."
sources: ["ISO 128 series, ISO 129-1, ISO 5456-2, ISO 3098, ISO 7200, ISO 2768-1, ISO 22081 (titles and scope only)", "ASME Y14.5-2018, ASME Y14.3, ASME Y14.100 (titles and scope only)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Producing a detail drawing that can be made without a phone call

**Goal:** one sheet per part that a machinist or inspector can build and check with no
questions: enough views, every feature sized and located once, tolerances on what
matters, and a title block that states which standards govern.

## 1. Decide the governing system first
- **ISO** (Europe, most of Asia): ISO 128 lines/views, ISO 129-1 dimensioning,
  **first-angle** projection by default, ISO 8015 independency principle unless stated.
- **ASME** (North America, US defence/aero): ASME Y14.5-2018 dimensioning and
  tolerancing, Y14.3 views, Y14.100 drawing practice, **third-angle** projection,
  Rule #1 (envelope) applies.
State it in the title block and show the projection symbol (truncated cone). Mixing
conventions on one drawing is a classic source of reversed views.

## 2. Choose views
1. **Main view** = the view showing most shape, drawn in the part's functional or
   machining orientation (a turned part lies with its axis horizontal).
2. Add only the views needed to define every feature: many prismatic parts need 2-3;
   turned parts often 1 plus a section or end view.
3. Prefer a **section** to a view full of hidden lines. Full, half, offset, aligned
   and broken-out sections each have their place; removed sections for shaft keyways.
4. **Detail views** (circle + letter, enlarged 2:1 or 5:1) for small features;
   **auxiliary views** for true shape of inclined faces.
5. Standard scales: 1:1, 1:2, 1:5, 1:10, 2:1, 5:1. Note any non-sheet scale beside
   the view.

## 3. Lines and lettering
- Two line widths in ratio 2:1. Common pair on A3/A4: **0.5 mm** wide (visible
  outlines, cutting-plane ends) and **0.25 mm** narrow (dimensions, hatching, centre
  lines, hidden); bump to 0.7/0.35 on A0/A1. Border 0.7 mm.
- Hatching: narrow lines at 45 degrees, uniform spacing (2-4 mm typical). Adjacent
  parts in assembly sections get opposite direction or different spacing. Do **not**
  hatch ribs, webs, shafts, pins, bolts, keys or balls cut lengthwise.
- Lettering heights from the 2.5 / 3.5 / 5 / 7 / 10 mm series: 3.5 mm for dimensions
  and notes is safe; 2.5 mm is the minimum and only if the print stays legible after
  reduction.

## 4. Dimension functionally
1. Pick datums from function: mating faces, bore axes, locating holes. Dimension
   from those, not from whatever edge was convenient to draw.
2. Each feature sized and located **once**. No duplicates; a reference dimension, if
   any, goes in parentheses.
3. Avoid long chains of tolerated dimensions where accumulation matters; use baseline
   or GD&T position from datums instead (see the
   `engineering-technology.technical-drawing-cad.gd-t.position-tolerancing-with-datums` skill).
4. Place dimensions outside the outline, about 10 mm from it and about 7 mm between
   rows; smaller first, larger outside, so extension lines don't cross dimension lines.
5. Dimension features in the view where their shape is clearest; never dimension to
   a hidden line.
6. Holes: diameter, depth and thread callouts (`M8x1.25 - 6H`, thread depth, drill
   depth), counterbore/countersink symbols.

## 5. Tolerances and notes
- Tight tolerances only where function demands; everything else under a general
  tolerance note, e.g. "General tolerances ISO 2768-m" (linear/angular). For general
  geometrical tolerances ISO 22081 is the current route; ISO 2768-2 is still widely
  quoted, so check which your organisation and suppliers accept.
- Surface texture per ISO 21920-1 symbols (it superseded ISO 1302); general value in or
  near the title block (e.g. Ra 3.2 all over, Ra 0.8 on bearing seats).
- Notes: material and condition, finish/coating, edge breaks ("break sharp edges
  0.2-0.5 x 45 deg"), heat treatment, applicable standards.

## 6. Title block essentials (ISO 7200 fields / ASME Y14.100 equivalents)
Part number, title, revision, sheet n of m, scale, projection symbol, units, material,
general tolerance and finish, drawn/checked/approved names and dates, governing
standards. The part number and revision must match the PDM record.

## Worked mini-example
A flanged bushing: main view is a full section along the axis (shows bore, counterbore
and flange together); one end view for the 4-hole PCD. Datums: flange face A, bore
axis B. Holes located by position from A and B, not chained from the outside diameter.
Two views, one section, no hidden lines.

## Verify
- [ ] Projection symbol and governing standard in the title block.
- [ ] Every feature sized and located exactly once; nothing measured off hidden lines.
- [ ] Tight tolerances traceable to a function; the rest covered by the general note.
- [ ] Hatching absent on ribs, shafts and fasteners in lengthwise section.
- [ ] Text at least 2.5 mm and readable on the reduced print.
