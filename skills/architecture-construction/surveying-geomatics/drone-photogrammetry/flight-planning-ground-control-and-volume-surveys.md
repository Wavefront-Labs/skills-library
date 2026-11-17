---
id: architecture-construction.surveying-geomatics.drone-photogrammetry.flight-planning-ground-control-and-volume-surveys
name: flight-planning-ground-control-and-volume-surveys
category: architecture-construction
field: surveying-geomatics
product: drone-photogrammetry
tags: [drone-photogrammetry, drone, uav, uas, photogrammetry, aerial-survey, flight-planning, gsd, ground-sample-distance, overlap, sidelap, ground-control-points, gcp, check-points, rtk-drone, ppk, orthophoto, orthomosaic, dsm, dtm, dem, point-cloud, stockpile-volume, earthworks-volume, pix4d, agisoft-metashape, dji, structure-from-motion, geomatics]
level: practitioner
status: draft
description: "UAV survey: plan GSD and overlap, lay ground control and independent check points, process to orthophoto, DSM and point cloud, and compute stockpile/earthworks volumes you can defend."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drone survey — flight planning, ground control and volumes

**Goal:** an orthophoto and surface model with a stated, checked accuracy — not just a
pretty map.

## 1. Legal and site prerequisites
Confirm airspace and operator permissions under your national aviation rules (e.g. UK
CAA, US FAA Part 107, EASA categories), landowner permission, and any site induction.
Check weather (wind, rain) and plan around people on site. This skill does not
replace the regulator's requirements — check them for your jurisdiction.

## 2. Flight planning
- **GSD (ground sample distance)** drives everything: GSD ≈ (sensor width × flight
  height) / (focal length × image width). A common rule: expect horizontal accuracy of
  about 1–2 × GSD and vertical about 2–3 × GSD with good control.
- **Overlap:** typically 75–80% forward and 65–75% side for mapping; more (80/80) over
  vegetation, water edges, uniform surfaces like sand or snow, which match poorly.
- **Flight height** above the *ground*, not take-off point, on sloping sites — use
  terrain-follow or the GSD at the highest ground will be finer and at the lowest coarser.
- Add **oblique** images or a cross-hatch grid for vertical faces, stockpile sides and
  buildings.
- Fly with consistent light; avoid low sun (long shadows) and mixed cloud (exposure jumps).
- Shutter speed fast enough to avoid motion blur; mechanical shutter preferred over
  rolling shutter, or enable rolling-shutter correction in processing.

## 3. Ground control and check points
- **GCPs:** high-contrast targets (or painted marks) surveyed with RTK GNSS or total
  station. Rule of thumb: at least 5, around the perimeter plus some in the middle;
  more on large or long corridor sites and at elevation extremes.
- **Check points:** additional surveyed targets **not used** in processing. These give
  your honest accuracy statement.
- **RTK/PPK drones** reduce how many GCPs you need, but you still need check points —
  and at least one GCP for a vertical check, because camera-position-only solutions can
  have a height bias.
- Target size: several GSD wide (e.g. ≥10× GSD) so the centre can be picked precisely.

## 4. Processing (Pix4D, Metashape, DJI Terra, etc.)
1. Import images; confirm camera model and geotags; set the output CRS and geoid.
2. Align/tie-point step. Look at the calibration report: proportion of images
   calibrated, reprojection error (often under ~1 pixel when good).
3. Mark GCPs in several images each; run optimisation.
4. Review **check-point RMSE** X, Y, Z. That's your stated accuracy.
5. Generate dense cloud, DSM, orthomosaic. Classify/filter ground to make a DTM if
   vegetation or machines are present.

## 5. Volumes
- Define the **base surface** explicitly: a design surface, an earlier survey, or a
  triangulated toe of the stockpile. The base choice causes most volume disputes.
- Remove machinery, people and vegetation from the surface before computing.
- Report cut/fill and net volume, the base method, the date, and the vertical accuracy.
  A 2 cm vertical bias over a 10,000 m² area is 200 m³ — state the uncertainty.

## Gotchas
- Water, glass and uniform surfaces don't reconstruct; expect holes or noise.
- "Bowling" (doming) of the model with too few GCPs and nadir-only images: fix with
  obliques and well-spread control.
- Wrong geoid/height reference gives a constant height offset across the whole model.
- Vegetation is surface, not ground: photogrammetry cannot see through canopy (LiDAR can partly).

## Verify
- [ ] Permissions and flight log recorded per your regulator.
- [ ] Planned GSD and overlap achieved (check the processing report).
- [ ] Independent check-point RMSE reported and within spec.
- [ ] Volume report states base surface method and uncertainty.
- [ ] Output CRS, units and height datum written in the deliverable metadata.

*Uncertainty:* the accuracy multiples of GSD are rules of thumb from practice; your
achieved check-point RMSE is the real figure.
