---
id: architecture-construction.surveying-geomatics.terrestrial-laser-scanner.scan-planning-registration-and-point-cloud-qa
name: scan-planning-registration-and-point-cloud-qa
category: architecture-construction
field: surveying-geomatics
product: terrestrial-laser-scanner
tags: [terrestrial-laser-scanner, tls, laser-scanning, lidar, point-cloud, scan-planning, registration, cloud-to-cloud, target-based-registration, checkerboard-targets, spheres, georeferencing, control, scan-to-bim, as-built, e57, rcp, leica-rtc360, faro-focus, trimble-x7, cyclone, recap, scene, geomatics, surveying]
level: practitioner
status: draft
description: "Terrestrial laser scanning: plan setups for overlap and coverage, register by targets or cloud-to-cloud, tie to survey control, and QA the cloud before delivering E57 or scan-to-BIM data."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terrestrial laser scanner — planning, registration and point-cloud QA

**Goal:** a registered, georeferenced point cloud whose accuracy you can state, with no
holes where the client needs data.

## 1. Agree the deliverable before you scan
Ask: what will the cloud be used for (measured drawings, scan-to-BIM, clash checks,
deformation)? What accuracy (e.g. ±5 mm local, ±10–20 mm global), what coordinate system,
and what Level of Detail/Accuracy (e.g. USIBD LOA bands, if the client uses them)? Those
answers set scan resolution, setup spacing and whether you need control.

## 2. Scan planning
- Walk the site; sketch setup positions on a plan.
- **Overlap:** each setup should share plenty of geometry (or ≥3 targets) with its
  neighbour. In corridors, setups every few metres and at every door and corner.
- **Coverage:** avoid shadows — scan both sides of columns, under tables, above ceiling
  tiles if required. Doors open, through-doorway setups link rooms.
- **Resolution:** pick point spacing at the range that matters (e.g. 6 mm at 10 m) rather
  than "max"; higher density costs time and file size without improving registration.
- **Range and incidence:** grazing angles on floors and walls far from the scanner give
  noisy, sparse data. Shorter range = better.
- Reflective, black, glass and wet surfaces return poorly or create ghosts.

## 3. Targets and control
- **Target-based registration:** checkerboards or spheres, ≥3 common to adjacent setups,
  not collinear, spread in height and plan.
- **Georeferencing:** survey some targets with a total station from control (see
  total-station skill) and use them as constraints. This also gives an independent
  check on the cloud's global accuracy.
- Scanners with built-in inclinometers/compensators — keep tilt compensation on unless
  you're scanning steep or inverted.

## 4. Registration
- **Cloud-to-cloud (ICP)** in software (Cyclone, ReCap, SCENE, Trimble RealWorks etc.)
  works well with good overlap and distinct geometry; it can drift along long
  featureless corridors or tunnels (the "banana" effect). Add targets or control there.
- Read the registration report: per-link errors and overall mean/RMS. Look for one bad
  link dragging the network — unlink it and re-register.
- **Constrain to control last**, then review residuals on control targets. Residuals
  much above the instrument spec point to a mis-picked target or a disturbed mark.

## 5. Point-cloud QA
- Section through the cloud (horizontal slice at ~1 m, vertical slices through walls).
  Double walls or ghosting = registration error.
- Check **independent check points** (surveyed but not used in registration) against
  the cloud.
- Remove noise: people, moving vehicles, mixed pixels on edges, reflections in glass.
- Confirm the coordinate system and units in the export header.

## 6. Deliverables
- **E57** is the vendor-neutral exchange format; RCP/RCS for Autodesk tools; LAS/LAZ for
  GIS. State coordinate system, units, date, and accuracy in a metadata note.
- Unified or per-scan? Scan-to-BIM teams usually want structured per-setup data plus a
  unified decimated cloud for viewing.

## Gotchas
- A setup knocked mid-scan gives a smeared scan; re-shoot it.
- Sunlight and heat reduce range and add noise outdoors; dark or wet stone returns weakly.
- Floor flatness and deformation work need tighter control and repeatable targets.
- File sizes explode: plan storage and transfer (hundreds of GB on large jobs).

## Verify
- [ ] Deliverable accuracy, coordinate system and LOA agreed in writing before scanning.
- [ ] Every setup links to the network with acceptable error; no single bad link.
- [ ] Control residuals and independent check points within spec.
- [ ] Slices show no double surfaces.
- [ ] Export metadata states CRS, units and accuracy.

*Uncertainty:* accuracy figures and LOA band names are illustrative; use the client's
specification and your scanner's stated performance.
