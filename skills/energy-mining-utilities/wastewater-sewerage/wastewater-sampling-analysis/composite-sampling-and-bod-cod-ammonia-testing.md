---
id: energy-mining-utilities.wastewater-sewerage.wastewater-sampling-analysis.composite-sampling-and-bod-cod-ammonia-testing
name: composite-sampling-and-bod-cod-ammonia-testing
category: energy-mining-utilities
field: wastewater-sewerage
product: wastewater-sampling-analysis
tags: [wastewater-sewerage, wastewater-sampling-analysis, composite-sample, flow-proportional, time-proportional, autosampler, grab-sample, bod, bod5, cbod, nitrification-inhibitor, atu, seed, gga, cod, dichromate, ammonia, ammonium-nitrogen, ion-selective-electrode, tss, suspended-solids, sample-preservation, holding-time, qc, blanks, duplicates, trade-effluent, effluent-permit, wastewater-lab]
level: practitioner
status: draft
description: "Collect flow-proportional composite wastewater samples and run BOD5, COD and ammonia tests with the QC that makes results defensible for permits and trade effluent."
sources:
  - "Standard Methods 5210 B (BOD), 5220 (COD), 4500-NH3 and 1060 (sample collection and preservation), paraphrased"
  - "US EPA 40 CFR 136 holding-time tables, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composite sampling and BOD, COD and ammonia testing

**Goal:** produce results that represent the day's wastewater and stand up to a regulator
or a disputing trade discharger.

## 1. Composite sampling
- **Flow-proportional** composites (volume or frequency proportional to flow, from the flow
  meter signal) represent load; **time-proportional** is acceptable only where flow is
  steady or the permit allows. Grab samples for pH, temperature, DO, residual chlorine and
  anything that changes quickly.
- Intake in a well-mixed, turbulent point (after a flume, not in a dead corner), away from
  floor deposits and surface scum; intake line purged before each draw.
- Refrigerated autosampler at ~ 4 °C (≤ 6 °C, not frozen) during the composite.
- Clean bottles and lines regularly — biofilm in the line seeds the sample.
- Mix the composite thoroughly before splitting; solids settle in seconds.

## 2. Preservation and holding times (typical)
- BOD: chilled, start within ~48 h (ideally same day); no acid.
- COD and ammonia: chilled, acidified with H2SO4 to pH < 2 if not analysed promptly; hold up
  to ~28 days.
Record sample ID, start/end times, total volume, and preservation on the chain of custody.

## 3. BOD5 essentials
1. Dilute so that **depletion is at least 2 mg/L and residual DO at least 1 mg/L** after
   5 days at 20 ± 1 °C in the dark. Run several dilutions.
2. Dilution water: aerated, nutrient/buffer added, blank depletion ≤ 0.2 mg/L.
3. **Seed** samples lacking bacteria (disinfected effluent, industrial waste); correct for
   seed. Neutralise pH 6–8 and dechlorinate first.
4. **cBOD**: add nitrification inhibitor (ATU/TCMP) when the permit is carbonaceous BOD —
   final effluents from nitrifying plants read falsely high without it.
5. Run a **glucose–glutamic acid (GGA)** check each batch; typical acceptance ~198 ± 30.5 mg/L.

## 4. COD
Dichromate digestion (vials, 150 °C, 2 h), then colorimetric read. Pick the range
(low/high) to fit the sample; homogenise solids. Chloride interferes — mercuric sulphate in
vials masks it up to a limit; high-chloride samples (seawater intrusion) need dilution or a
special method. Dispose of vials as hazardous waste (chromium, mercury, silver).

## 5. Ammonia
Ion-selective electrode (add alkaline ISA to convert NH4+ to NH3, read promptly, calibrate
across the expected range with fresh standards) or colorimetric (salicylate/phenate) kits.
Online analysers need weekly grab-sample comparison.

## 6. QC that matters
Method blank, duplicate (or spike) every batch or ~10%, calibration check standard,
control charts. Report with method, units (mg/L as N for ammonia) and qualifiers when a QC
check failed — don't silently report.

## Gotchas
- COD:BOD ratio jumps are a quick sanity check (raw sewage commonly ~2:1); a big change
  hints at a toxic or industrial discharge, or a lab error.
- Toxic samples suppress BOD: higher dilution giving higher calculated BOD = toxicity.
- Leaving samples on the bench warms them and the BOD falls.

## Verify
- [ ] Composite flow-proportional, chilled throughout, well mixed before splitting.
- [ ] Holding times and preservation met and recorded.
- [ ] BOD dilutions meet depletion/residual rules; blank and GGA in limits.
- [ ] COD range correct, chloride considered; waste disposed properly.
- [ ] Batch QC passed or result qualified.

*Uncertain:* holding times and acceptance limits are from US-style methods; check your
national standard and accredited-lab requirements.
