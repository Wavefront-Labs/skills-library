---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.hardware-architectural-metrics-spfm-lfm
name: hardware-architectural-metrics-spfm-lfm
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [hardware-metrics, spfm, lfm, pmhf, fmeda, diagnostic-coverage, fit-rate]
level: practitioner
status: gated
description: "Compute SPFM, LFM and PMHF from FMEDA data and compare with the ISO 26262 targets by ASIL, with diagnostic coverage and failure-rate sourcing."
sources:
  - "ISO 26262-5:2018 Road vehicles - Functional safety - Part 5: Product development at the hardware level (https://www.iso.org/standard/68387.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hardware architectural metrics (SPFM, LFM, PMHF)

Professional practice guidance; apply ISO 26262-5 and your safety manager's method. Target values below should be confirmed in the current edition.

1. FMEDA: list each hardware element and failure mode with failure rate (FIT = failures per 10^9 h), classify by effect on the safety goal: safe, single-point or residual (no or insufficient coverage), multiple-point (latent or detected/perceived).
2. **Diagnostic coverage (DC)** of each safety mechanism: percent of the failure mode detected (typical classes: low 60%, medium 90%, high 99% per the standard's reference tables (gated: unconfirmed, source is paywalled or blocked)).
3. **SPFM** (single-point fault metric) `= 1 - (sum of SPF + RF rates)/(sum of safety-related rates)`; **LFM** (latent fault metric) accounts for undetected multiple-point faults.
4. Targets (ISO 26262-5:2018 (gated: unconfirmed, source is paywalled or blocked)): ASIL B: SPFM >= 90%, LFM >= 60%; ASIL C: SPFM >= 97%, LFM >= 80%; ASIL D: SPFM >= 99%, LFM >= 90%. **PMHF** (or the alternative evaluation of residual risk): below 100 FIT for ASIL B and C and below 10 FIT for ASIL D (gated: unconfirmed, source is paywalled or blocked). Confirm in the current edition.
5. Sources of failure rates: generic databases (for example SN 29500 and FIDES; check whether IEC TR 62380 is still current (gated: unconfirmed, source is paywalled or blocked)), supplier FMEDA, field returns; document assumptions and mission profile (temperature).
6. Improve by adding diagnostics (watchdog, ADC plausibility, ECC, lockstep CPU, loopback tests) or architecture changes.
7. Document the results as part of the hardware safety analysis.

**Gotchas:** claiming high DC without evidence; ignoring latent faults of the safety mechanism itself.

## Verify
- [ ] FMEDA spreadsheet totals reproduce the SPFM, LFM, PMHF numbers on independent recalculation.
- [ ] Each diagnostic coverage claim has a justification or test evidence.
