---
id: engineering-technology.electrical-engineering.power-system-analysis.harmonics-assessment
name: harmonics-assessment
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [electrical-engineering, flicker, harmonic-filter-sizing, harmonics, harmonics-assessment, ieee-519, power-quality, power-system-analysis, thd, voltage-sag-analysis]
level: advanced
status: draft
description: "Assess harmonic distortion at the point of common coupling against IEEE 519 and size passive filters; note sag and flicker indices."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Harmonics and power quality assessment

1. **Sources:** six-pulse converters inject orders `6k +/- 1` (5, 7, 11, 13); twelve-pulse `12k +/- 1`. Switch-mode supplies add triplens in the neutral.
2. **Metrics:** `THD_V = sqrt(sum V_h^2) / V_1`; for current, use total demand distortion (TDD) relative to maximum demand current rather than instantaneous fundamental.
3. **IEEE 519 (2014 edition; revised 2022):** limits apply at the point of common coupling. Voltage limits by bus voltage (for example about 5 percent THD at 1 to 69 kV and 8 percent at or below 1 kV) and current limits by the ratio of short-circuit current to maximum demand current (stiffer systems allow more). Check the edition and the utility's own rules.
4. **Resonance screen:** `h_r = sqrt(Ssc / Qc)`; avoid capacitors tuned near characteristic orders.
5. **Passive filter sizing:** tune slightly below the target order (for example 4.7 for the 5th) to survive component tolerance and temperature drift; size the capacitor for fundamental plus harmonic current and voltage; check the filter does not resonate with the source at a lower order.
6. **Sag and flicker:** IEEE 1159 classifies a sag as 0.1 to 0.9 pu RMS for half a cycle to one minute; flicker is assessed with Pst and Plt from a flickermeter per IEC 61000-4-15.

**Verify:** measure with a Class A power-quality analyser per IEC 61000-4-30 across a representative week and compare the 95th percentile to the limit.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
