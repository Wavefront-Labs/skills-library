---
id: engineering-technology.electrical-engineering.circuit-analysis.instrumentation-circuits
name: instrumentation-circuits
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [adc-anti-alias-filter, circuit-analysis, current-shunt, electrical-engineering, error-budget, instrumentation-amplifier, instrumentation-circuits, measurement-error, shunt-and-ct-sensing]
level: practitioner
status: draft
description: "Design current sensing and signal-conditioning stages: shunts, CTs, instrumentation amplifiers, anti-alias filters and error budgets."
sources:
  - "https://www.ncees.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Measurement and instrumentation circuits

1. **Shunt:** `V = I R`; dissipation `I^2 R` and temperature coefficient set accuracy; use four-terminal (Kelvin) connection so lead resistance is excluded. High-side sensing needs an amplifier with common-mode range covering the bus voltage.
2. **Current transformer:** AC only, secondary must never be open-circuited while primary energised; burden resistor converts secondary current to voltage.
3. **Instrumentation amplifier:** classic three-op-amp gain `G = (1 + 2 R1/Rg)(R3/R2)`; common-mode rejection depends on resistor matching; keep source impedances balanced.
4. **Anti-alias filter:** corner well below half the sample rate; required stopband attenuation at `fs/2` is roughly 6 dB per ADC bit to push aliases below one LSB (for example 72 dB at 12 bits). Use a higher-order active filter or oversample and decimate.
5. **Error budget:** combine independent errors by root-sum-square; list gain, offset, reference, temperature, noise and quantisation.

**Verify:** inject a known current and compare the ADC reading across the temperature range.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
