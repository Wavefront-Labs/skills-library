---
id: architecture-construction.surveying-geomatics.topographic-surveying.detail-pickup-feature-coding-and-contours
name: detail-pickup-feature-coding-and-contours
category: architecture-construction
field: surveying-geomatics
product: topographic-surveying
tags: [topographic-surveying, topo-survey, detail-survey, site-survey, feature-coding, field-codes, linework, string-coding, breaklines, spot-heights, tin, dtm, contours, contour-interval, invert-levels, manholes, utilities, tree-survey, existing-conditions, civil-3d, 12d, autocad, total-station, gnss-rtk, geomatics, surveying]
level: practitioner
status: draft
description: "Topographic site survey: plan the brief, shoot detail with feature codes that build linework automatically, capture breaklines properly, and produce a TIN and contours that represent the ground."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Topographic survey — detail pickup, coding and contours

**Goal:** a site survey drawing whose surface and features the designer can trust
without a site visit.

## 1. Agree the brief
Before going out: extent (plus a margin beyond the boundary — designers always need
the neighbour's levels), coordinate system and height datum, scale/density, which
features (trees with spread/girth? drainage inverts? services? building floor and eaves
levels?), and file format/CAD template. Many disputes come from a vague brief.

## 2. Control first
Set and observe control (see control-networks skill), with enough marks left for the
designer and setting-out team later. Record descriptions and witness diagrams.

## 3. Feature coding
Use a consistent **code list** that your CAD/processing software turns into linework
and symbols (e.g. Civil 3D description keys, 12d codes, Trimble/Leica feature libraries).
- Point codes: `TREE`, `MH`, `LP` (lamp post).
- String/line codes with line control: e.g. `KERB1 ST` (start), `KERB1` (continue),
  `KERB1 END`, plus curve and close commands. Number separate strings of the same
  feature (`KERB1`, `KERB2`) so they don't join across the road.
- Attributes: tree species/girth/spread, manhole cover and invert levels, pipe sizes.
Coding in the field is far faster than drawing by hand in the office, and less error-prone.

## 4. Pickup technique
- **Breaklines** — every change of grade: top and bottom of banks, kerb top and channel,
  edges of paving, walls (top and base), ditches (top, bottom, both sides). Contours
  will be wrong wherever a breakline is missing.
- **Density** — spot heights on a rough grid (spacing set by brief and terrain, e.g.
  5–20 m) plus extra on any undulation. Flat ground needs fewer; rolling ground more.
- **Buildings** — corners, door thresholds and finished floor level, eaves/ridge if
  required.
- **Drainage** — lift covers (safely; confined-space rules apply — never enter), measure
  depths to invert and record pipe direction and size.
- **Overhead and underground services** — visible evidence only unless a utility
  survey (PAS 128 / ASCE 38 type) is commissioned. Label as such.

## 5. Processing
1. Import, check codes processed into the right layers; fix stray strings that join
   wrong points.
2. Build a **TIN** using spot heights and breaklines; exclude points that aren't ground
   (tops of walls only if they're breaklines of the surface you want, tree points, roofs).
3. Inspect the TIN in 3D or with triangle display: long skinny triangles across a
   building or outside the surveyed area mean false surface — add a boundary.
4. Generate **contours** at the agreed interval (e.g. 0.25 m, 0.5 m, 1 m), labelled.
5. Check contours visually: they should never cross, should "V" upstream in channels
   and turn round banks crisply.

## Gotchas
- Wrong target height after the pole was changed: a whole string sits at the wrong level.
- Surveying a car-park full of cars: the surface goes over the roofs if you don't watch.
- Large trees: record trunk position at breast height, not the canopy edge.
- Hidden services: never present a topo as a utility survey.

## Verify
- [ ] Brief (extent, datum, features, format) written and agreed.
- [ ] All breaklines picked up; contours behave correctly at kerbs, banks and channels.
- [ ] TIN bounded; no triangles spanning un-surveyed areas or buildings.
- [ ] Independent check shots on a few hard features agree within tolerance.
- [ ] Drawing notes state CRS, datum, date, control, and limitations.

*Uncertainty:* code syntax varies by software; the examples are illustrative, not a
specific vendor's library.
