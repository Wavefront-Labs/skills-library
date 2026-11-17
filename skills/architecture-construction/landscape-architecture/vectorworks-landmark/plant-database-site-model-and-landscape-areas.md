---
id: architecture-construction.landscape-architecture.vectorworks-landmark.plant-database-site-model-and-landscape-areas
name: plant-database-site-model-and-landscape-areas
category: architecture-construction
field: landscape-architecture
product: vectorworks-landmark
tags: [vectorworks-landmark, vectorworks, landmark, landscape-bim, bim, plant-tool, plant-objects, plant-catalog, plant-database, landscape-area, planting-style, site-model, dtm, site-modifiers, grade-limits, pads, cut-and-fill, existing-tree-tool, hardscape-tool, irrigation-tools, worksheets, schedules, data-tags, classes, design-layers, sheet-layers, viewports, ifc, landscape-architecture]
level: practitioner
status: draft
description: "Use Vectorworks Landmark's plant objects and catalog, landscape areas, site model with modifiers, existing trees and worksheets to drive plans and schedules from one BIM model."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plant database, site model and landscape areas in Vectorworks Landmark

**Goal:** one Landmark file where plants, planted areas, hardscape and terrain are
intelligent objects, so schedules, quantities and cut/fill update when the design does.
(Menu names below follow recent Vectorworks versions; they move between releases —
check your version's help if a command isn't where stated.)

## 1. Organise
- **Design layers** for physical elevation (Site, Ground Floor, Roof Terrace) with
  correct elevations; **classes** for what things are (`Plants-Trees`,
  `Plants-Shrubs`, `Hardscape-Paving`, `Site-DTM`, `Annotation`). Sheet layers hold
  viewports for each drawing.
- Set the **georeference** in Document Settings if working from a coordinate survey.

## 2. Plants: the catalog is the asset
- Plant objects carry data: botanical/common name, size at planting, mature spread,
  spacing, price, nursery, and more. Build or import your **office plant catalog**
  (the Plant Catalog / Plant Manager, depending on version) once and reuse it.
- Place with the **Plant tool**: single, poly-line (along a path), or fill an area at
  set spacing (triangular/rectangular) — the count is calculated for you.
- Show plants at **mature spread** for planting plans; tag with data tags that read
  the object's data (code + quantity).

## 3. Landscape areas
- **Landscape Area** objects represent planted beds, lawn or meadow with a mix of
  species and percentages/densities; they report area and calculated plant
  quantities to schedules without placing every plant symbol.
- Define reusable **planting styles** for mixes (e.g. "Shade mix A").

## 4. Site model
1. Import survey points or 3D contours; create a **Site Model** (DTM) from them.
   Check for spikes (bad points) in 3D view; edit source data, not the mesh.
2. Shape proposed grades with **site modifiers**: pads (level areas with fall),
   grade limits (where modification stops), and 3D polygon/contour modifiers for
   swales and slopes.
3. Update the site model; read **cut and fill** volumes from the object info /
   site model report. Iterate to balance earthworks where possible.
4. Hardscape objects can drape on or modify the site model.

## 5. Existing trees
The Existing Tree tool records species, DBH/stem diameter, canopy, condition and
retain/remove status, and can display root protection zones — the base for a tree
protection plan (method per local standard, e.g. BS 5837 in the UK).

## 6. Worksheets and schedules
- Worksheets with database rows (e.g. all plant objects grouped by name) produce
  **plant schedules**, hardscape area takeoffs and tree schedules that update live.
- Export to Excel for the cost consultant; IFC export for BIM coordination.

## Gotchas
- Plant catalog entries missing data (sizes, spacing) → schedules with blanks.
- Plant objects on wrong design layer elevation → 3D floating trees.
- Site model rebuilt from contours with spikes from mis-tagged survey points.
- Plans drawn as plain 2D symbols — then nothing schedules.

## Verify
- [ ] Layers at correct elevations; classes applied consistently.
- [ ] Every plant is a plant object linked to a catalog entry with full data.
- [ ] Landscape area quantities appear in the schedule.
- [ ] Site model has no spikes; cut/fill figures reviewed.
- [ ] Schedules update after a design change (test by moving something).
