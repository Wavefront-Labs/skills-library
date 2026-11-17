---
id: engineering-technology.technical-authentication-testing.dimensional-metrology.cmm-inspection-and-uncertainty-budgets
name: cmm-inspection-and-uncertainty-budgets
category: engineering-technology
field: technical-authentication-testing
product: dimensional-metrology
tags: [cmm, coordinate-measuring-machine, dimensional-metrology, gd-and-t, asme-y14-5, datum-alignment, 3-2-1-alignment, probing-strategy, stylus-qualification, iso-10360, mpe, measurement-uncertainty, gum, uncertainty-budget, gauge-r-and-r, grr, msa, iso-14253-1, decision-rules, guard-band, first-article-inspection, fai, as9102, thermal-compensation, calypso, pc-dmis]
level: advanced
status: draft
description: "Program CMM inspections to ASME Y14.5 datums, verify per ISO 10360, build a GUM uncertainty budget, run gauge R&R, apply ISO 14253-1 decision rules and AS9102 FAI."
sources: ["ASME Y14.5-2018 Dimensioning and Tolerancing", "ISO 10360-2 and -5 Acceptance and reverification tests for coordinate measuring systems", "JCGM 100:2008 Evaluation of measurement data - Guide to the expression of uncertainty in measurement (GUM)", "ISO 14253-1 Decision rules for verifying conformity or nonconformity with specifications", "AIAG Measurement Systems Analysis Reference Manual", "SAE AS9102 Aerospace First Article Inspection Requirement", "ISO 15530-3 CMM uncertainty using calibrated workpieces"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMM inspection and uncertainty budgets — measure what the drawing means, and know how sure you are

**Goal:** produce CMM results that evaluate each characteristic as ASME Y14.5 defines it, with a stated expanded uncertainty and a documented accept/reject decision rule.

## 1. Before programming

- Read the drawing as a contract: which Y14.5 edition (2009 vs 2018 changed datum and profile rules), default rule (Rule #1 envelope), and the datum reference frame (DRF) for each feature control frame.
- Soak the part at 20 °C (ISO 1 reference) — rule of thumb, 1 hour per 25 mm section, or until the part sensor reads stable. Steel grows ~11.5 µm/m/K, aluminium ~23 µm/m/K.
- Check the machine's ISO 10360-2 verification (MPE_E, e.g. "1.8 + L/300 µm") is current, and qualify every stylus on the reference sphere; reject if the qualified diameter's form error exceeds your lab limit (often ~1 µm on a good machine).

## 2. Alignment and datums

- Build the DRF in datum precedence: primary plane constrains 3 degrees of freedom, secondary line/axis 2, tertiary point 1 (3-2-1). Use many points on datum features, not the minimum 3-2-1.
- Simulate datums as Y14.5 intends: the primary plane is a **tangent (high-point, constrained)** plane, not a least-squares plane through the surface; a datum bore at MMB is a fixed-size simulator, which allows datum shift. Most CMM software (PC-DMIS, Calypso, etc.) offers these fitting options — select them explicitly.
- A "best-fit" alignment over all features is for diagnostics only; it does not report against the drawing.

## 3. Probing strategy

- Points per feature: at least 8-12 evenly spaced points on circles where form matters, more (or scanning) for form, profile and small tolerances. Too few points underestimate form error.
- Probe perpendicular to the surface; keep the stylus short and stiff, ball as large as the feature allows (mechanical filtering) but consistent with the spec.
- Scanning speed changes results through dynamic error: validate the speed against touch points on a ring gauge.
- Report size per definition: two-point local size vs. least-squares vs. maximum-inscribed — choose what the tolerance means.

## 4. Uncertainty budget (GUM)

u_c = √(Σ (c_i·u_i)²), U = k·u_c with k = 2 (~95%). Type A from repeat measurements (standard deviation of the mean or of single readings as appropriate); Type B from certificates and specs (rectangular: a/√3).

Example, Ø50 mm aluminium bore, part at 22 °C with temperature compensation:

| Source | Basis | u (µm) |
|---|---|---|
| CMM MPE_E 1.97 µm | rectangular | 1.14 |
| Repeatability, 10 cycles | Type A, s | 0.80 |
| Part temperature ±0.5 K | 50 mm × 23e-6 × 0.5/√3 | 0.33 |
| Expansion coefficient ±10% | 50 mm × 2 K × 2.3e-6/√3 | 0.13 |
| Form/sampling effect | estimate | 1.00 |
| **u_c** | | **1.75** |
| **U (k=2)** | | **3.5** |

Using the length MPE for a diameter is an approximation; ISO 15530-3 (calibrated workpiece substitution) gives a better task-specific value.

## 5. Gauge R&R (AIAG MSA)

10 parts × 3 operators × 2-3 trials, ANOVA method. %GRR (vs. tolerance or total variation) < 10% acceptable, 10-30% conditionally acceptable, > 30% unacceptable; number of distinct categories ndc ≥ 5. On automated CMMs, operator variance often reflects fixturing and loading.

## 6. Decision rules (ISO 14253-1)

Default: prove conformance only if the result lies inside the tolerance reduced by U at each limit (acceptance zone), and prove nonconformance only outside the tolerance extended by U. With tolerance ±10 µm and U = 3.5 µm, accept only within ±6.5 µm; results between are indeterminate and need a better method or a customer-agreed rule (ASME B89.7.3.1 alternatives). Aim for tolerance-to-uncertainty ratio ≥ 4:1.

## 7. First-article inspection (AS9102)

Balloon every design characteristic, including notes and specs. Form 1: part number accountability; Form 2: material, special processes and functional test accountability with certs; Form 3: each characteristic with result and measuring tool. Partial FAI after design, process, tooling, location or 2-year production-lapse changes (check your customer's revision).

## Gotchas

- Least-squares datum planes give optimistic results on warped parts.
- Reporting "in tolerance" with no uncertainty statement shifts risk to the customer.
- Fixture clamping distorts thin parts; measure released, or as specified (restrained-condition note).
- Unqualified star-stylus tips, or a crashed stylus, silently shift every feature.

## Verify

- [ ] Drawing standard edition and DRF are documented in the program.
- [ ] Machine verification is current and all styli qualified this session.
- [ ] Datums are fitted as tangent/constrained simulators, not least-squares.
- [ ] Uncertainty budget exists and the TUR is ≥4:1 or a decision rule is agreed.
- [ ] Gauge R&R %GRR < 10% (or justified) with ndc ≥ 5.
- [ ] AS9102 forms reference every ballooned characteristic.
