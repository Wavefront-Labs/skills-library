---
id: architecture-construction.civil-construction.gps-machine-control.site-calibration-and-grade-checking
name: site-calibration-and-grade-checking
category: architecture-construction
field: civil-construction
product: gps-machine-control
tags: [gps-machine-control, machine-control, 3d-machine-control, gnss, rtk, base-station, rover, vrs, network-rtk, site-calibration, localisation, localization, control-points, residuals, geoid, trimble-earthworks, trimble-business-center, tbc, topcon, topcon-3d-mc, magnet, leica-icon, leica-icg, design-surface, tin, dtm, linework, alignment, grade-check, dozer, excavator, grader, bucket-calibration, sensor-calibration, tolerance]
level: practitioner
status: draft
description: "Run GNSS machine control on a civil site: prepare the design surface, localise to site control, check residuals, calibrate machines, and verify grade with independent rover checks."
sources: ["Trimble, Topcon and Leica machine control user documentation (general concepts)", "General survey practice for RTK GNSS site calibration/localisation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Site calibration and grade checking for GNSS machine control

**Goal:** dozers, excavators and graders cutting to the design surface within tolerance
— which depends less on the machine than on three things: a correct design model,
a correct site localisation, and machines whose sensors are calibrated and checked daily.

> Menu names differ between Trimble (Earthworks/Siteworks/TBC), Topcon (3D-MC, MAGNET)
> and Leica (iCON/iCG). The concepts below apply to all; *verify the exact procedure in
> your system's manual.*

## 1. Prepare the design data
- Get the designer's surfaces (finished level, subgrade, each pavement layer), alignments
  and linework, usually as LandXML/DWG.
- Build machine files in the office software (TBC, MAGNET Office, iCON office, etc.):
  - Use the right surface for the operation — **subgrade**, not finished road level, for
    bulk earthworks (offsetting finished level by pavement depth is wrong on
    crossfalls/widenings).
  - Check the TIN for spikes, holes and triangles bridging across areas they shouldn't;
    review in 3D and with contours.
  - Clip to the work area to keep file size manageable.
- **Version control**: name files with revision and date; remove superseded designs from
  machines. Grading to an old design is a common, expensive error.

## 2. Site calibration / localisation
GNSS gives positions in a global datum; the site works in a local grid and height datum.
- Use **site control points** established by the surveyor (at least 4, ideally more,
  surrounding the work area — not all in a line).
- Measure them with the rover from the base (or VRS) and compute the localisation
  (horizontal transformation + vertical adjustment / geoid model).
- Check **residuals**: typically within ~10–20 mm horizontal and ~20–30 mm vertical for
  earthworks (project tolerance governs). A large residual on one point → disturbed or
  wrong control point; investigate, don't just exclude it silently.
- Load the **same** calibration file on every machine and rover. Mismatched
  calibrations between machines show as steps between their work.
- Base station: on a stable, known point; same base position each day (record setup);
  check radio/cellular coverage across the site.

## 3. Machine setup and calibration
- Measure and enter machine dimensions accurately (antenna positions, boom, stick,
  bucket linkage) per the system's procedure.
- **Bucket/blade calibration** after changing buckets or any repair; record the bucket
  in use (each bucket profile stored separately).
- Sensor checks (IMUs/tilt, rotation) per manufacturer intervals.

## 4. Daily checks (before work)
- **Benchmark check**: place the bucket tip/blade edge on a known check point (site
  control or a check peg) and compare the screen's position and height. Agree a
  tolerance (e.g. ±20–30 mm vertical) and stop if outside.
- Confirm the correct design file and surface is loaded and the right offset is set.
- Check GNSS fix status (RTK fixed, not float) and satellite count/precision.

## 5. Independent grade checking
- A surveyor or foreman with a **rover** checks finished areas against the design
  on a grid (e.g. every 10–20 m and at changes in grade), reporting cut/fill.
- Record and colour-map results; areas out of tolerance get reworked before the next
  layer goes down.
- Hand over **as-built** surface data for quantity and conformance records.

## Gotchas
- Working near tall structures, under trees or in cuttings degrades GNSS — expect float
  solutions; total station-based control may be needed for fine grading.
- Changing localisation mid-job without telling all machines = inconsistent levels.
- Bucket wear changes tip position; recalibrate periodically.

## Verify
- [ ] Machine file built from the current design revision and the correct surface.
- [ ] Localisation residuals within tolerance and identical file on all units.
- [ ] Daily benchmark check logged for every machine.
- [ ] Rover grade checks on completed areas within tolerance.
- [ ] As-built data saved and superseded designs removed from machines.
