---
id: health-medicine.endocrinology.diabetes-technology.cgm-ambulatory-glucose-profile-review
name: cgm-ambulatory-glucose-profile-review
category: health-medicine
field: endocrinology
product: diabetes-technology
tags: [endocrinology, diabetes-technology, cgm, continuous-glucose-monitoring, ambulatory-glucose-profile, agp, time-in-range, tir, time-below-range, time-above-range, glucose-management-indicator, gmi, coefficient-of-variation, glycaemic-variability, hypoglycaemia, nocturnal-hypoglycaemia, dawn-phenomenon, postprandial-hyperglycaemia, dexcom, freestyle-libre, intermittently-scanned-cgm, compression-low, sensor-interference, automated-insulin-delivery, insulin-pump]
level: practitioner
status: gated
description: "Read a CGM ambulatory glucose profile systematically: data sufficiency, consensus time-in-range targets, hypoglycaemia first, daily patterns, GMI/CV, and sensor artefacts."
sources: ["Battelino et al., Clinical Targets for Continuous Glucose Monitoring Data Interpretation: Recommendations From the International Consensus on Time in Range, Diabetes Care 2019 (PMC6973648)", "International Consensus on Use of Continuous Glucose Monitoring (Danne et al., Diabetes Care 2017)", "ADA Standards of Care in Diabetes - Diabetes Technology section (annual)", "Manufacturer IFUs for CGM systems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

*Targets in the metrics table were checked against Battelino et al., Diabetes Care 2019 (PMC6973648). General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

# Reviewing a CGM ambulatory glucose profile (AGP)

**Goal:** turn 14 days of CGM data into one or two specific, safe treatment changes in a
few minutes — hypoglycaemia first, then the biggest hyperglycaemic pattern.

## 1. Check the data are sufficient
- **≥14 days** of data with **≥70% sensor wear** (≈10 of 14 days) before trusting the metrics.
- Note gaps (night-time gaps hide lows), the device, sensor changes, and whether the person
  uses multiple daily injections, a pump or automated insulin delivery (AID).

## 2. Compare core metrics with consensus targets (type 1 and type 2, most adults)
| Metric | Range | Target |
|---|---|---|
| Time in range (TIR) | 70–180 mg/dL (3.9–10.0 mmol/L) | **>70%** (~>16 h 48 min/day) |
| Time below range (TBR) level 1+2 | <70 mg/dL (3.9 mmol/L) | **<4%** |
| TBR level 2 | <54 mg/dL (3.0 mmol/L) | **<1%** |
| Time above range (TAR) level 1+2 | >180 mg/dL (10.0 mmol/L) | <25% |
| TAR level 2 | >250 mg/dL (13.9 mmol/L) | <5% |
| Coefficient of variation (CV) | — | **≤36%** |
- **Older/high-risk** (frailty, hypoglycaemia unawareness): TIR >50%, TBR <1%, TAR >250 <10%.
- **Pregnancy (type 1)**: 63–140 mg/dL (3.5–7.8 mmol/L) >70%, below 63 <4%, below 54 <1%.
- Each 10% gain in TIR (2.4 h/day) corresponds to roughly 0.5% lower HbA1c in the consensus paper (approximate, population-level; the 0.8% upper figure previously quoted is unconfirmed and removed).
- **GMI** estimates HbA1c from mean glucose; discordance with lab HbA1c is common (red cell
  lifespan, haemoglobin variants) — trust CGM metrics for decisions, note the gap.

## 3. Read the AGP in a fixed order
1. **Hypoglycaemia first.** When (overnight, post-exercise, late post-meal 2–4 h after bolus)?
   Fix TBR before addressing hyperglycaemia; high CV (>36%) predicts hypoglycaemia risk.
2. **Overnight and fasting.** Flat overnight median = basal about right. Steady rise from ~03:00
   = dawn phenomenon / insufficient basal; falling overnight = excess basal (or AID compensating).
3. **Meals.** Rises >~50–60 mg/dL (~3 mmol/L) after a meal (gated: unconfirmed, source is paywalled or blocked) suggest carb ratio, timing (pre-bolus
   15–20 min (gated: unconfirmed, source is paywalled or blocked)) or missed boluses. Look at the 25–75% band width: wide = behaviour/variable intake.
4. **Daily view.** Scan individual days to separate a true pattern from a few outliers.
5. **Agree one or two changes** and the date to review.

## 4. Device-specific considerations
- **AID systems**: adjust carb ratios, active-insulin time and target settings rather than
  manual basal; check time in automated mode and causes of exits.
- Pump users: link highs to infusion-set age (>2–3 days (gated: unconfirmed, source is paywalled or blocked)) and missed site changes.
- Sensor accuracy is lower on day 1 (gated: unconfirmed, source is paywalled or blocked) and at extremes; interstitial glucose lags blood by ~5–15 min (gated: unconfirmed, source is paywalled or blocked),
  more during rapid change — confirm hypoglycaemia symptoms or discordant readings with fingerstick.

## Gotchas
- **Compression lows**: brief, sharp overnight drops from lying on the sensor — not true
  hypoglycaemia; don't cut basal for them.
- **Interfering substances** (device-dependent; check IFU): paracetamol/acetaminophen
  (older Dexcom models (gated: unconfirmed, source is paywalled or blocked)), high-dose vitamin C (some Libre sensors (gated: unconfirmed, source is paywalled or blocked)), hydroxyurea (gated: unconfirmed, source is paywalled or blocked). Remove sensors
  for MRI/CT/diathermy per manufacturer.
- Averages mask opposite patterns (lows on weekdays, highs at weekends) — check daily views.
- Alarm settings: ensure low alerts are on, especially with unawareness; alarm fatigue reduces wear.
- Metrics reflect the period, not adherence to the plan — ask what happened before changing doses.

## Verify
- [ ] ≥14 days and ≥70% wear confirmed, or limitations noted.
- [ ] TIR, TBR (<70 and <54), TAR, CV and GMI recorded against the correct target set.
- [ ] Hypoglycaemia patterns addressed before hyperglycaemia.
- [ ] Each proposed change is tied to a specific time-of-day pattern.
- [ ] Artefacts (compression lows, interference, sensor day 1) excluded.
- [ ] Follow-up review date agreed.
