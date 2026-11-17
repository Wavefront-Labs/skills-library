---
id: natural-sciences.oceanography.marine-geology-geophysics.multibeam-bathymetry-acquisition-and-processing
name: multibeam-bathymetry-acquisition-and-processing
category: natural-sciences
field: oceanography
product: marine-geology-geophysics
tags: [marine-geology-geophysics, multibeam, multibeam-echosounder, mbes, bathymetry, seafloor-mapping, sound-velocity-profile, svp, xbt, patch-test, roll-pitch-yaw, latency, motion-reference-unit, backscatter, swath-width, line-planning, mb-system, qimera, caris-hips, gridding, iho-s44, tide-correction, seabed-2030, gebco]
level: practitioner
status: draft
description: "Plan, acquire and clean multibeam bathymetry: line spacing for overlap, sound-velocity profiles, patch test, refraction artefacts, cleaning in MB-System/Qimera and gridding at honest resolution."
sources: ["IHO S-44 Standards for Hydrographic Surveys", "MB-System documentation", "Lurton, An Introduction to Underwater Acoustics (Springer)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multibeam bathymetry acquisition and processing

**Goal:** a seafloor grid whose depths and features are real — not refraction smiles,
motion artefacts or over-gridded noise — with the processing traceable.

## 1. Before acquisition
- **Patch test** (calibration) after installation or any sensor change: run specific
  line pairs to solve offsets for **latency**, **pitch**, **roll** and **yaw** (heading).
  Classic geometry: reciprocal lines over a slope (pitch/latency), reciprocal lines over
  flat seafloor (roll), adjacent parallel lines past a feature (yaw). Apply values to the
  acquisition or processing configuration and document them.
- Lever arms (sensor offsets from reference point) surveyed and entered once, correctly.

## 2. Line planning
- Swath width ≈ k × water depth (often 3–5× for modern systems, depending on frequency,
  angle limit and seafloor type). Plan **spacing for 10–30% overlap** of usable swath —
  outer beams are noisiest; don't plan on the full advertised swath.
- Run lines **parallel to contours** where possible (steady depth = steady swath).
- Speed: the along-track sounding density must meet your target resolution; faster
  speed = fewer pings per metre, more motion noise.
- Cross-lines (perpendicular to main lines) give an independent check of accuracy.

## 3. Sound velocity
- Take **sound-velocity profiles** (SVP probe, CTD, or XBT/XSV underway) at the start and
  whenever the water column changes (fronts, river plumes, diurnal heating), typically
  every few hours.
- A **surface sound-velocity sensor** at the transducer is needed for beam steering.
- Wrong SVP shows as **smiles or frowns** across the swath (outer beams curving up or
  down on flat seafloor). Small errors can be fixed in processing by applying the right
  profile; large ones can't fully.

## 4. Processing workflow
1. Import raw data (Kongsberg .all/.kmall, R2Sonic, Reson .s7k) into MB-System,
   QPS Qimera or CARIS HIPS.
2. Apply/check navigation, attitude, heave, SVP, tides or GNSS heights (ellipsoid-referenced
   surveys avoid tide models; state the vertical datum).
3. Automated filtering (angle limits, depth windows, spline/CUBE-type surface filters)
   then **manual cleaning** in 3D/subset editors. Remove spikes; keep real features
   (wrecks, pinnacles) — overly aggressive filters erase small targets.
4. Check **cross-line agreement** against IHO S-44 order uncertainty limits appropriate to
   your survey.
5. **Grid** at a cell size supported by sounding density — commonly ≥3–5 soundings per
   cell. Over-fine grids look sharp but are interpolation. Deeper water → larger footprint
   → coarser honest resolution.
6. Export with metadata (CRS, vertical datum, cell size, processing summary). Consider
   contributing to Seabed 2030/GEBCO via the national data centre.

## 5. Backscatter (brief)
Backscatter strength reflects seabed type (rock/sand/mud) but needs angle-varying gain
correction and consistent system settings across the survey to be comparable.

## Gotchas
- Not re-running the patch test after transducer or MRU work.
- Stale SVP across a front → systematic depth errors at the swath edges.
- Heave artefacts in rough weather appear as along-track ripples.
- Assuming the vendor's "processed" output is clean.
- *Uncertainty note:* swath-width multipliers and density rules vary widely by system.

## Verify
- [ ] Patch-test offsets recorded and applied.
- [ ] SVP log covers the survey in time and space; no residual smiles on flat seafloor.
- [ ] Cross-line differences within the target S-44 order.
- [ ] Grid cell size justified by sounding density.
- [ ] Vertical datum and CRS stated in the deliverable.
