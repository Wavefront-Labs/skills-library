---
id: architecture-construction.surveying-geomatics.hydrographic-surveying.bathymetry-sound-velocity-and-tide-reduction
name: bathymetry-sound-velocity-and-tide-reduction
category: architecture-construction
field: surveying-geomatics
product: hydrographic-surveying
tags: [hydrographic-surveying, hydrography, bathymetry, bathymetric-survey, echo-sounder, single-beam, multibeam, mbes, sonar, sound-velocity, svp, bar-check, patch-test, latency, roll, pitch, heave, motion-sensor, tide, tide-reduction, chart-datum, rtk-tides, dredge-survey, dredging, channel-survey, iho-s44, hypack, qinsy, geomatics]
level: advanced
status: draft
description: "Bathymetric survey: calibrate the sounder (bar check, sound velocity, patch test), reduce depths to chart datum by tide gauge or RTK, and compute dredge volumes to an IHO S-44 order."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hydrographic surveying — bathymetry, sound velocity and tide reduction

**Goal:** depths reduced to the right vertical datum, at the right position, with
known uncertainty — for charts, dredge payment, or construction in water.

## 1. Specification
Agree the standard (commonly an **IHO S-44** order, or a port/dredging authority spec,
e.g. a USACE-style manual for US navigation projects), coverage (line spacing or full
bottom coverage), vertical datum (chart datum / LAT, local datum, or ellipsoid), and
deliverables (soundings, surface, volumes, charts).

## 2. System and offsets
- Measure **lever arms** from the vessel reference point to the GNSS antenna, motion
  sensor and transducer, ideally by total-station survey of the vessel out of the water.
- Record transducer **draft** (static) and estimate **squat/settlement** with speed.
- Motion sensor (heave, pitch, roll) and heading are essential for multibeam; single
  beam benefits from heave compensation.

## 3. Calibration
- **Bar check** (single beam): lower a plate/bar to known depths below the transducer
  and compare readings — checks draft and average sound velocity.
- **Sound velocity profile (SVP):** cast a profiler at the start, during (when conditions
  change — tide state, freshwater inflow, temperature), and end. Wrong sound velocity
  distorts depths and, for multibeam, bends the outer beams (frowns/smiles across the swath).
- **Patch test** (multibeam): latency, roll, pitch and yaw offsets from purpose-run lines
  over a slope and a flat area. Re-do after any transducer removal.
- Daily: position check alongside a known mark; draft check.

## 4. Running the survey
- Main lines plus **cross lines** (checks; typically ~5–10% of main line length) to
  compare depths at intersections.
- Speed constant and appropriate to ping rate and coverage requirement.
- Watch for aeration (bubbles under the hull in turns or chop), weed, fish and
  suspended sediment / fluid mud, which can give false bottoms. Dual-frequency sounders
  help distinguish soft layers.

## 5. Tide / vertical reduction
- **Tide gauge method:** observed water level from a gauge tied to chart datum; apply to
  soundings by time (and by zone/co-tidal correction if far from the gauge).
- **RTK/PPK GNSS heights (ellipsoid-referenced):** reduce via a separation model
  between ellipsoid and chart datum (e.g. a national vertical-separation model). Avoids
  gauge distance errors but needs good GNSS and correct lever arms and heave.
- Check: compare gauge-based and GNSS-based water levels; they should agree within the
  error budget.

## 6. Processing and products
- Clean spikes and noise (manually and with filters), apply SVP, tide, motion and
  offsets (HYPACK, QINSy, CARIS and similar).
- Grid to a surface at a resolution appropriate to density.
- **Dredge volumes:** compare surface to the design (or pre-dredge) prism, including
  side slopes and **overdepth** allowances defined in the contract. State which
  allowances are payable.
- Cross-line comparison statistics and a Total Propagated Uncertainty estimate support
  the claimed order.

## Gotchas
- Wrong draft entered = a constant depth bias over the whole survey.
- Mixing up depths below transducer and below water surface.
- Datum confusion: chart datum varies along a coast; don't assume it equals the local land
  levelling datum.
- Water safety: lifejackets, man-overboard drills and a competent skipper are not optional.

## Verify
- [ ] Spec, datum and coverage agreed in writing.
- [ ] Offsets measured; bar check / SVP / patch test recorded.
- [ ] Cross-line differences within spec.
- [ ] Vertical reduction method stated and independently checked.
- [ ] Volume report states design prism, overdepth and pay allowances.

*Uncertainty:* this is a general outline; IHO S-44 order thresholds and dredging
contract terms must be read directly from the current documents.
