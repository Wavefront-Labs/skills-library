---
id: law-government.occupational-health-and-safety-practice.industrial-hygiene.air-sampling-and-noise-dosimetry-against-exposure-limits
name: air-sampling-and-noise-dosimetry-against-exposure-limits
category: law-government
field: occupational-health-and-safety-practice
product: industrial-hygiene
tags: [occupational-health-and-safety-practice, industrial-hygiene, occupational-hygiene, exposure-assessment, air-sampling, personal-sampling, breathing-zone, sampling-pump, calibration, field-blank, niosh-methods, osha-methods, twa, time-weighted-average, stel, ceiling-limit, oel, pel, rel, tlv, acgih, wel, similar-exposure-group, seg, aiha-strategy, 95th-percentile, noise-monitoring, noise-dosimetry, dosimeter, sound-level-meter, dba, lex-8h, exchange-rate, hearing-conservation, local-exhaust-ventilation, lev]
level: advanced
status: gated
description: "Measure workplace exposures properly: similar exposure groups, calibrated personal air sampling, 8-h TWA and STEL maths, noise dosimetry, comparing to the right OEL, and turning results into controls."
sources: ["OSHA 29 CFR 1910.95 (eCFR)", "UK Control of Noise at Work Regulations 2005 reg 4 (legislation.gov.uk)", "NIOSH noise topic page (cdc.gov/niosh/noise)", "AIHA, A Strategy for Assessing and Managing Occupational Exposures", "NIOSH Manual of Analytical Methods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Air sampling and noise dosimetry against exposure limits

**Goal:** know whether workers' exposure to an airborne contaminant or noise is
acceptable, with data defensible enough to drive spending on controls.

## 1. Plan before you sample
- **Basic characterisation:** processes, materials (safety data sheets), tasks, shift
  patterns, existing controls, complaints, health surveillance results.
- Group workers into **similar exposure groups (SEGs)** — same task, materials,
  controls. The AIHA exposure-assessment strategy is the common framework.
- Pick the **right limit** for your jurisdiction and purpose: legal limits (OSHA PELs,
  UK WELs in EH40, EU binding/indicative OELVs, national lists) vs. often more
  protective advisory limits (ACGIH TLVs, NIOSH RELs). Note limit type: 8-hour TWA,
  15-minute STEL, or ceiling. Limits **vary by jurisdiction** and are revised —
  check the current edition.
- Choose the validated **method** (NIOSH Manual of Analytical Methods, OSHA methods,
  UK MDHS, ISO): it specifies sampler (filter cassette, sorbent tube, cyclone for
  respirable fraction), flow rate, minimum/maximum volume, and the lab analysis.
  Use an accredited lab.

## 2. Air sampling in the field
1. **Calibrate pumps** with the sampling media in line before and after; post-cal
   drift beyond about ±5% generally invalidates or flags the sample (gated: unconfirmed, source is paywalled or blocked); the validated method sets the actual tolerance.
2. Sampler in the **breathing zone** (within ~30 cm of nose/mouth, usually lapel),
   outside any respirator.
3. Sample the **full shift** where possible, or enough of it to represent it; record
   start/stop times, tasks done, controls in use, anything unusual.
4. **Field blanks** (handled like samples, no air drawn) per batch.
5. Chain-of-custody form to the lab.

## 3. The arithmetic
8-hour TWA = Σ(Cᵢ × tᵢ) / 480 min, where Cᵢ is concentration over period tᵢ (minutes),
counting unsampled time as zero **only** if you know exposure was zero.

Example: 0.6 mg/m³ for 300 min, 1.5 mg/m³ for 120 min, 0 for 60 min →
(180 + 180 + 0)/480 = **0.75 mg/m³**.

Extended shifts: some regimes require adjusting limits for >8 h (e.g. the Brief & Scala
model (gated: unconfirmed, source is paywalled or blocked)) — check local guidance. Mixtures with additive effects: Σ(Cᵢ/OELᵢ) > 1 means
over the limit.

Statistics: one sample proves little. With enough samples per SEG (about 6 or more is a common rule (gated: unconfirmed, source is paywalled or blocked)), fit a lognormal
distribution and compare the **95th percentile** to the OEL (a common decision rule),
using tools like IHSTAT/IHDA-class software.

## 4. Noise
- **Sound level meter** to survey areas; **personal dosimeters** for worker dose.
- Know the regime's parameters: OSHA uses 90 dBA PEL with a 5 dB exchange rate and an
  85 dBA action level for hearing conservation (29 CFR 1910.95, confirmed against the eCFR text); NIOSH recommends 85 dBA with a 3 dB
  exchange rate; the EU Physical Agents (Noise) Directive uses 80/85 dB(A) action values
  and an 87 dB(A) limit (with hearing protection taken into account) as L_EX,8h, plus
  peak limits. Set the dosimeter (criterion level, exchange rate, threshold) to match.
- Field-calibrate the dosimeter with an acoustic calibrator before and after.
- Hearing protectors: apply a derating to labelled attenuation (the derating scheme is set by your regime (gated: unconfirmed, source is paywalled or blocked)); real-world
  protection is lower than the label.

## 5. Report and act
Report: SEG, task, sample results, TWA/STEL vs. which limit, uncertainty, and a clear
conclusion (acceptable / control needed / insufficient data). Recommend controls by
the hierarchy: substitution, enclosure, **local exhaust ventilation** (with capture
velocity checks), process change, then respirators with a fit-tested programme.

## Verify
- [ ] SEGs defined; the right limit and current edition chosen.
- [ ] Validated method, calibrated pump, breathing-zone placement, blanks.
- [ ] TWA calculated with documented assumptions for unsampled time.
- [ ] Dosimeter settings match the applicable noise regime.
- [ ] Report states a conclusion and controls, not just numbers.
