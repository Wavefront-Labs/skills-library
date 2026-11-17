---
id: architecture-construction.cartography-geospatial-mapping.cadastral-mapping.parcel-fabric-maintenance-from-survey-plans
name: parcel-fabric-maintenance-from-survey-plans
category: architecture-construction
field: cartography-geospatial-mapping
product: cadastral-mapping
tags: [cadastral-mapping, cadastre, cadastral-database, land-parcels, parcel-fabric, arcgis-parcel-fabric, coordinate-geometry, cogo, bearings-and-distances, survey-plan, deposited-plan, plat, subdivision, plan-lodgement, misclosure, traverse-closure, least-squares-adjustment, control-points, rubber-sheeting, spatial-accuracy, upgrade-program, topology, lineage, historic-parcels, land-registry, title, tenure, easements, ladm, iso-19152]
level: advanced
status: draft
description: "Maintain a cadastral parcel map from survey plans: COGO capture, misclosure checks, fitting to control by adjustment, topology and lineage, and honest accuracy statements."
sources: ["Esri ArcGIS Pro Parcel Fabric documentation", "ISO 19152 Land Administration Domain Model (LADM)", "FIG publications on cadastral systems and spatial upgrade"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining a parcel fabric from survey plans

**Goal:** a cadastral map that represents every parcel's legal boundaries as recorded on
survey plans, fits together without gaps or overlaps, gets more accurate over time, and
keeps the history of every change — while being honest that the *map is not the
boundary*.

> Legal status of cadastral maps differs by jurisdiction. In most systems, the survey
> plan, monuments and title documents define the boundary; the map is an index. Never
> issue a map extract as boundary evidence unless your law says it is.

## 1. Inputs
- New lodged/registered **survey plans** (subdivision, consolidation, boundary
  re-establishment): bearings, distances, arc data (radius, arc length, chord), areas,
  connections to survey control marks, record of the plan's datum/bearing basis.
- Title/registry changes (new parcel IDs, cancelled parcels, easements).
- Geodetic control with known coordinates.

## 2. Capture by COGO, not by digitising
Enter each boundary as recorded dimensions (coordinate geometry): bearings/directions,
distances, curves, with the plan as the **record source** on each line. Digitising scanned
plans throws away the record and adds scanning error.
- Note the plan's **bearing basis** (grid, true, magnetic, or arbitrary "plan north")
  and rotate/scale accordingly.
- Distances: ground vs grid — apply the combined scale factor if the fabric is in a
  projected grid (difference can be tens of ppm to hundreds of ppm).

## 3. Check misclosure
Traverse each parcel: the loop should close. Compute linear misclosure and ratio
(e.g. 1:10,000 or better for modern plans — *your jurisdiction sets acceptance*).
Large misclosures usually mean a typo in capture (transposed digits, wrong quadrant,
missing curve) — re-check against the plan before blaming the surveyor.

## 4. Fit to the fabric
- Join the new parcels to existing ones at shared corners (connections, common points).
- **Least-squares adjustment** (ArcGIS Parcel Fabric and other cadastral systems
  support this) distributes errors using measurement weights, holding control points
  fixed. Review residuals; large ones flag blunders.
- Avoid **rubber-sheeting** the whole map to fit new work — it hides errors and moves
  well-located parcels. Use it only in documented upgrade projects with control.

## 5. Topology and lineage
- No gaps or overlaps between parcels of the same type; every parcel closed.
- Retire parent parcels (historic, not deleted) and create children, recording the plan
  that did it. **Lineage** answers "where did this parcel come from" years later.
- Maintain separate layers/types for ownership parcels, easements, road reserves,
  administrative boundaries; they overlap legitimately.

## 6. Spatial accuracy and upgrade
Record estimated accuracy per point/line (e.g. survey-grade vs digitised-from-old-map).
Old map-derived cadastres often carry metres of error. Accuracy improves over time as
new surveys connected to control are adjusted in — show accuracy classes on outputs so
users don't treat 5 m data as 5 cm.

## Gotchas
- Users overlay high-accuracy design/lidar data on low-accuracy cadastre and "find"
  encroachments that are mapping error. Put an accuracy disclaimer on products.
- Datum transformations (old to modern datum) can shift the whole fabric by metres;
  apply the official transformation grid.
- Curves captured as straight chords change parcel areas.

## Verify
- [ ] Every new line carries its record dimensions and plan reference.
- [ ] Parcel misclosures within the acceptance ratio, or explained.
- [ ] Adjustment residuals reviewed; control held fixed.
- [ ] No gaps/overlaps; parents retired with lineage to children.
- [ ] Accuracy class recorded; product disclaimer states the map is not the boundary.
