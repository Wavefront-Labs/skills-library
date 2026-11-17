---
id: natural-sciences.environmental-science.air-water-quality-monitoring.low-cost-air-sensor-colocation-and-qaqc
name: low-cost-air-sensor-colocation-and-qaqc
category: natural-sciences
field: environmental-science
product: air-water-quality-monitoring
tags: [air-water-quality-monitoring, air-quality, pm2.5, pm10, particulate-matter, low-cost-sensors, purpleair, plantower, optical-particle-counter, colocation, collocation, fem, frm, reference-monitor, calibration, relative-humidity-correction, epa-correction, linear-regression, sensor-drift, qa-qc, data-completeness, exceedance-analysis, sensor-networks, no2, ozone, electrochemical-sensors]
level: practitioner
status: draft
description: "Make low-cost PM2.5 (and gas) sensor data research-grade: co-locate with a reference monitor, fit a humidity-aware correction, screen channel disagreement and drift, and report uncertainty."
sources: [US EPA Performance Testing Protocols for Air Sensors (PM2.5, 2021; O3 and NO2), Barkjohn et al. 2021 AMT US-wide PurpleAir correction, EPA Air Sensor Toolbox]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Low-cost air sensor co-location and QA/QC

**Goal:** turn a network of cheap optical PM sensors (PurpleAir, Plantower-, Sensirion-
based units) or electrochemical gas sensors into data you can publish, by calibrating
against a regulatory-grade monitor and screening out bad periods.

## 1. Co-locate before you deploy (and after)
- Mount sensors within ~20 m horizontally and ~1 m vertically of the inlet of a
  **Federal Equivalent/Reference Method (FEM/FRM)** monitor or equivalent national
  reference. Ask the agency operating the site; many allow short-term mounting.
- Run **at least 30 days** (EPA's base testing protocol) and ideally across humidity and
  concentration ranges you'll see in deployment. A summer-only calibration fails in a
  humid winter or wildfire smoke.
- Repeat a shorter co-location at the end (or rotate one "travelling" sensor between
  reference and network) to quantify drift.

## 2. Clean before you calibrate
- Average to the reference's resolution — usually **1-hour** and **24-hour** means —
  and require ≥75% completeness per averaging period.
- **Dual-channel check (PurpleAir A/B):** drop or flag hours where the channels differ
  by more than ~5 µg/m³ *and* ~70% (rule used in the US-wide correction paper; treat
  thresholds as a starting point).
- Remove obvious faults: flat lines, values pinned at sensor maximum, negative gas
  readings that persist, and periods after power loss.

## 3. Fit the correction
Optical sensors overestimate PM2.5 at high humidity because particles take up water.
- Baseline model: `PM_ref = b0 + b1·PM_sensor + b2·RH` fitted by ordinary least squares
  on hourly or daily means. The published US-wide PurpleAir equation has this form; use
  it as a fallback when you have no local co-location, but a local fit is better.
- Check whether the relationship bends at high concentration (smoke): published
  extended corrections switch to a different equation above roughly 300–600 µg/m³.
- For electrochemical NO2/O3 sensors, temperature and cross-sensitivity (O3 on NO2
  cells) dominate; multiple regression or random-forest models are common, but they
  overfit without held-out validation.
- **Validate on held-out data** (e.g. last 25% of time, or a different site). Report
  R², slope, intercept, RMSE and normalised RMSE. EPA's PM2.5 targets for base testing
  are roughly slope 1.0 ± 0.35, intercept within ±5 µg/m³, R² ≥ 0.70, RMSE ≤ 7 µg/m³
  — confirm current values in the protocol.

## 4. In the field
- Site sensors 2–6 m high, away from vents, grills, roads' kerbside plume (unless that's
  the question) and obstructions; log metadata (height, orientation, power, photos).
- Monitor network health daily: % reporting, inter-sensor correlation, and sudden
  offsets. A dust-fouled or insect-occupied sensor often shows a step change.
- Document firmware versions; an update can change the raw output.

## 5. Interpreting exceedances
Low-cost data supports spatial patterns and screening, not regulatory compliance.
When a corrected sensor exceeds a standard, express it as "indicative" with the
validation RMSE, and compare to the nearest reference station for the same period.

## Gotchas
- PurpleAir reports `cf_1` and `cf_atm`; corrections are fit to one specific field
  (the US-wide one uses `cf_1`). Mixing them silently biases results.
- Daily means look far better than hourly; report both.
- A correction fit at one reference site transfers imperfectly to different aerosol
  types (dust, sea salt, smoke).

## Verify
- [ ] ≥30 days co-location spanning deployment-like conditions; end-of-study recheck done.
- [ ] Channel-disagreement and completeness screens applied and documented.
- [ ] Correction validated on held-out data, with slope, intercept, R², RMSE reported.
- [ ] Data field (cf_1 vs cf_atm) and firmware recorded.
- [ ] Exceedances reported as indicative with stated uncertainty.
