---
id: humanities.archaeology.field-survey.fieldwalking-and-geophysical-prospection
name: fieldwalking-and-geophysical-prospection
category: humanities
field: archaeology
product: field-survey
tags: [field-survey, archaeology, prospection, fieldwalking, surface-collection, transects, gridded-collection, artefact-scatter, geophysics, magnetometry, gradiometry, fluxgate, resistivity, earth-resistance, gpr, ground-penetrating-radar, lidar, aerial-photography, cropmarks, remote-sensing, landscape-survey, site-detection, gps, rtk, non-intrusive-survey, desk-based-assessment]
level: practitioner
status: draft
description: "Find and map sites before digging: desk-based assessment, gridded fieldwalking, choosing magnetometry vs resistivity vs GPR, LiDAR and cropmark reading, and honest negative evidence."
sources:
  - "Historic England, Geophysical Survey in Archaeological Field Evaluation (2008)"
  - "Gaffney, C. & Gater, J. Revealing the Buried Past: Geophysics for Archaeologists"
  - "Renfrew, C. & Bahn, P. Archaeology: Theories, Methods and Practice (survey chapter)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fieldwalking and geophysical prospection

**Goal:** locate and characterise sites across a landscape without excavating, and record
both what you found *and how hard you looked*, so absence of finds means something.

## 1. Desk-based assessment first
Before anyone walks a field, pull together: the national/regional Historic Environment
Record (HER/SMR) entries, historic maps (tithe, enclosure, early Ordnance Survey or local
equivalents), aerial photographs across several years and seasons, available LiDAR, geology
and soil maps, and previous reports. Draw it as one GIS layer stack (see
`humanities.archaeology.gis-for-archaeology.building-an-archaeological-site-gis`). The
geology decides which geophysical method will work, so this step is not optional.

## 2. Fieldwalking (surface collection)
- **When:** ploughed, weathered fields — ideally after rain has washed the surface. Record
  plough date and visibility (a 0–100% or good/moderate/poor scale) per unit; visibility
  controls recovery more than walker skill.
- **Layout:** transects typically 10–20 m apart, collected in 10–20 m stints, or a gridded
  collection (e.g. 10×10 m or 20×20 m squares) over a known scatter. Lay out with GNSS; RTK
  gives centimetre accuracy, handheld GPS ±3–5 m, which is fine for transect stints but not
  for small grids.
- **Collect consistently:** decide in advance what is collected (all worked flint and pottery?
  burnt flint counted but discarded?) and bag by unit with unit ID on and in the bag.
- **Walker bias:** rotate walkers and record who walked what; some people spot flint, others
  pottery.
- Output: density plots per material class and period, not dots of "finds".

## 3. Geophysics — choosing a method
| Method | Detects | Good for | Struggles with |
|---|---|---|---|
| Magnetometry (fluxgate gradiometer) | Magnetic contrasts: fired features, ditch fills, pits | Fast area coverage (several ha/day with a cart) — the default first pass | Igneous geology, alluvium, modern iron, fences, pylons |
| Earth resistance | Moisture contrast: walls, rubble, ditches | Masonry buildings, wet/dry contrasts | Very dry or waterlogged ground; slow |
| GPR | Reflections from interfaces, with depth | Floors, walls, depth slices in urban or cemetery work | Clay and saline soils (signal attenuates fast) |

Typical sampling for magnetometry: 1 m traverses × 0.25 m readings (UK guidance minimum
for evaluation); denser for small features. *Unconfirmed for every national standard —
check your regulator's current guidance.*

## 4. LiDAR and aerial evidence
- Use a **DTM** (bare earth) not a DSM, and view it with several visualisations — multi-angle
  hillshade, slope, local relief model, sky-view factor. A single hillshade hides features
  parallel to the light.
- Cropmarks show best in dry summers over cereals; parchmarks over walls in grass. Check
  multiple years — one flight is a sample, not a survey.
- Many "features" are drainage, plough headlands, or recent tracks. Ground-truth before
  you name anything.

## Gotchas
- Wear no metal near a gradiometer: phone, keys, boot eyelets and zips all show up. Re-zero
  (balance) the instrument regularly and log it.
- Geophysics shows **anomalies**, not archaeology. Interpret with a separate layer of
  confidence (probable / possible / uncertain / modern).
- Do not "de-stripe" or over-filter data into pretty pictures and lose the raw grids — keep
  raw data and record every processing step.
- Permissions: landowner consent always; many jurisdictions require a licence for geophysics
  or any collection on protected sites, and metal detecting on scheduled monuments is
  usually illegal.
- Recording zero-finds units is evidence. Leaving them out makes the distribution meaningless.

## Verify
- [ ] Desk-based assessment and geology checked before choosing the method.
- [ ] Every collection unit has location, walker, date, visibility and conditions — including empty units.
- [ ] Geophysics method justified against geology; sampling interval recorded.
- [ ] Raw data archived; processing steps listed; interpretation separated from data plot.
- [ ] Anomalies graded by confidence and, where possible, ground-truthed.
