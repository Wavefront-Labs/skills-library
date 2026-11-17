---
id: manufacturing-production.production-quality-control.measurement-system-analysis.running-a-gage-rr-and-acting-on-it
name: running-a-gage-rr-and-acting-on-it
category: manufacturing-production
field: production-quality-control
product: measurement-system-analysis
tags: [measurement-system-analysis, msa, gage-rr, gauge-r-and-r, grr, repeatability, reproducibility, equipment-variation, appraiser-variation, part-variation, percent-tolerance, percent-study-variation, ndc, bias-study, linearity-study, stability-study, type-1-gage-study, cg, cgk, attribute-agreement-analysis, kappa, aiag-msa, vda-5, calibration, calibration-recall, gauge-control, resolution, 10-to-1-rule, production-quality-control]
level: practitioner
status: draft
description: "Prove a gauge is fit before trusting its data: plan and run a crossed gage R&R, type-1, bias/linearity and attribute agreement studies, interpret results, fix the gauge, and manage calibration."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a gage R&R and acting on it

**Goal:** know how much of the variation you see is the measurement, not the part — and
fix the measurement when it's too much. Software steps for Minitab are in
manufacturing-production.production-quality-control.minitab.control-charts-capability-and-gage-rr-in-minitab;
this skill is planning, running and acting. References: AIAG MSA manual (4th ed.), VDA Volume 5 (more uncertainty-based).

## 1. Before any study: resolution and calibration
- **Resolution**: the gauge should read in steps of ≤ 1/10 of the tolerance (the
  "10:1 rule"; some allow 1/10 of process spread instead). A 0.01 mm caliper on a ±0.01 mm
  feature cannot work, whatever the R&R says.
- Gauge **calibrated** and in date, with a label; zero checked against a master.

## 2. Type-1 study (one gauge, one master, quick capability)
Measure a reference part/master ~25–50 times (one operator). Compute **Cg** and **Cgk**
(bias included); common acceptance **Cg, Cgk ≥ 1.33** (Bosch/VDA practice). Good first check for a new or repaired gauge.

## 3. Crossed gage R&R (variables)
**Plan:**
- **10 parts** that span the **real process range** (not 10 consecutive near-identical parts).
- **3 appraisers** who actually use the gauge in production.
- **2–3 trials** each.
- Number the parts discreetly; present them in **random order**, each appraiser **blind**
  to previous readings. Same method, same location, same fixture as production.
**Run:** record every reading directly in the study sheet/software. Don't discard "odd" readings.
**Read the results (ANOVA method preferred):**
| Metric | Rule of thumb (AIAG) |
|---|---|
| %GRR of tolerance or study variation | < 10% good; 10–30% may be acceptable depending on importance and cost; > 30% unacceptable |
| ndc (number of distinct categories) | ≥ 5 |
| Repeatability (EV) ≫ Reproducibility (AV) | Gauge/fixture problem: wear, clamping, resolution, part locating |
| Reproducibility (AV) ≫ Repeatability | People problem: method, training, reading parallax, unclear procedure |
| Operator×part interaction significant | Some appraisers struggle with certain parts — technique |
Use **%Tolerance** for a gauge used to accept/reject parts; **%Study Var** for a gauge used for SPC/process improvement.

## 4. Bias, linearity and stability
- **Bias**: measure a reference part of known value (measured by a better method) many
  times; average minus reference. Correct the gauge or apply known offset only if approved.
- **Linearity**: bias at several reference sizes across the range — bias changing with size suggests a scale/calibration issue.
- **Stability**: measure the same master over weeks, plot on a control chart; drift indicates wear or environment.

## 5. Attribute agreement (go/no-go, visual)
- ~30–50 parts, including borderline ones, with known standard decisions.
- 2–3 appraisers, 2–3 trials, blind and random.
- Look at within-appraiser repeatability, appraiser vs standard, and **kappa** (≥ 0.75 good, < 0.4 poor — common guide).
- Misses (accepting bad) are worse than false alarms; report them separately.

## 6. Fixing a failing gauge
- High EV: better fixture/locating, cleaner contact points, higher resolution, temperature control, sturdier gauge.
- High AV: one written method (where, how much force, how many readings), training,
  digital readout, poka-yoke fixture.
- Re-run the study after the fix; document both.

## Gotchas
- Choosing parts from one shift's output — tiny part variation makes %SV look awful.
- Appraisers seeing their earlier readings or the part numbers.
- Running the study in the metrology lab when the gauge is used on the shop floor.
- Calibration overdue but gauge still on the line — do a **recall assessment** of
  everything measured since the last good calibration if it fails calibration.

## Verify
- [ ] Gauge resolution ≤ 1/10 tolerance; calibration in date.
- [ ] Parts span process range; random, blind, production method.
- [ ] %GRR (right denominator) and ndc reported; EV vs AV used to target fixes.
- [ ] Attribute studies report misses and kappa.
- [ ] Failing gauge fixed and re-studied before release to production.
