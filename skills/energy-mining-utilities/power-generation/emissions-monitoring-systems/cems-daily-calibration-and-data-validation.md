---
id: energy-mining-utilities.power-generation.emissions-monitoring-systems.cems-daily-calibration-and-data-validation
name: cems-daily-calibration-and-data-validation
category: energy-mining-utilities
field: power-generation
product: emissions-monitoring-systems
tags: [emissions-monitoring-systems, power-generation, cems, ams, continuous-emissions-monitoring, stack-monitoring, nox, so2, co, co2, o2, opacity, particulate, calibration-drift, zero-and-span, daily-calibration, calibration-gas, protocol-gas, cylinder-gas-audit, linearity, rata, part-75, part-60, en-14181, qal1, qal2, qal3, ast, cusum, data-substitution, data-availability, extractive, dilution-probe]
level: practitioner
status: draft
description: "Run the daily zero/span checks on a plant CEMS, judge drift, handle out-of-control periods and validate hourly data so compliance reports stand up (US Part 60/75 and EU EN 14181 terms)."
sources: ["US EPA 40 CFR Part 60 Appendix F and Part 75 (public, paraphrased)", "EN 14181 Stationary source emissions — QA of automated measuring systems (concepts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CEMS daily calibration and data validation

**Goal:** keep the continuous emissions monitoring system (CEMS — called AMS in EU
terms) producing data that is valid, defensible and available, so the plant's
compliance reports are right first time. The plant-side craft is mostly routine
checks done carefully, and knowing when data has stopped being valid.

## 1. Know your regulatory frame
- **US:** 40 CFR Part 60 (NSPS, Appendix F QA procedures) and/or **Part 75** (acid
  rain / trading programmes) — daily calibration error tests, quarterly linearity or
  cylinder gas audits, annual/semiannual RATA (relative accuracy test audit against a
  reference method).
- **EU/UK:** **EN 14181** — QAL1 (instrument certified suitable), QAL2 (calibration
  function from parallel reference tests, typically every 3–5 years), **QAL3**
  (ongoing drift and precision checks by the operator, often with CUSUM or Shewhart
  charts), AST (annual surveillance test).
Your permit names which applies and the exact limits; the procedures below are the
shared core.

## 2. The daily zero and span check
1. Usually automatic at a set time. The analyser (or the probe, for system checks)
   is flooded with **zero gas** then **span/upscale gas** of certified concentration.
2. Check the **certificate**: cylinder concentration, expiry date, and that it is a
   traceable (in the US, EPA Protocol) gas in the right range — commonly 80–100 % of
   span for upscale, but confirm your rule.
3. **Calibration drift** = difference between response and the reference value, as %
   of span. Typical Part 75 limits are around 2.5 % of span for gas monitors (with an
   alternative for low-span analysers); Part 60 often allows 2× the performance
   spec. Know your numbers.
4. **System vs analyser:** gas injected at the probe tests the whole sample path
   (filters, heated line, chiller). Gas at the analyser only tests the analyser. A
   pass at the analyser but fail at the probe → leak or absorption in the sample line.

## 3. When a check fails
- The monitor is **out of control** from the hour of the failed check (or the last
  passing check, depending on rule) until a passing check after corrective action.
- Fix the cause — leak, chiller fault, wet filter, failing lamp or cell, empty
  cylinder — then rerun the check. Log what was done and when.
- Data during the out-of-control period is invalid: it is replaced by **substitute
  data** (Part 75 has specific, often punitive, substitution routines) or recorded as
  unavailable. That's why fast repair matters.
- Don't adjust the analyser to pass the check then call the earlier hours valid;
  adjustment happens after the failed check is recorded.

## 4. Validating hourly data
- Each hour needs a minimum number of valid readings (in the US, commonly at least one
  valid reading per 15-minute quadrant).
- Flag hours during calibration, maintenance, startup/shutdown per permit rules.
- Check diluent (O2 or CO2) — corrected concentrations (e.g. to 6 % or 15 % O2) are
  meaningless if the diluent is wrong.
- Compare with plant data: NOx tracks load and combustion settings; a flat line often
  means a stuck analyser or frozen data.
- Track **data availability** against the permit minimum (often ~90–95 % per period).

## Gotchas
- Moisture: condensation in a chilled extractive system strips SO2 and NO2 — low
  readings that pass analyser-only checks.
- Bottles near empty give unstable spans; change before the pressure drops too low.
- Clock drift between DAHS and DCS confuses event reconciliation; check time sync.
- Uncertain: drift limits and substitution rules quoted are typical and vary by
  regulation, pollutant and analyser span — confirm with your permit and DAHS vendor.

## Verify
- [ ] Daily zero and span ran, drift within limits, results stored in the DAHS.
- [ ] Calibration gas certificates current and in the correct range.
- [ ] Any failed check: out-of-control period recorded, cause fixed, passing check run.
- [ ] Hourly data validity and diluent correction reviewed.
- [ ] Data availability on track for the reporting period.
