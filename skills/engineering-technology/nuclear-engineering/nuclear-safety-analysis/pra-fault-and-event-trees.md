---
id: engineering-technology.nuclear-engineering.nuclear-safety-analysis.pra-fault-and-event-trees
name: pra-fault-and-event-trees
category: engineering-technology
field: nuclear-engineering
product: nuclear-safety-analysis
tags: [nuclear-safety-analysis, pra, psa, level-1-pra, probabilistic-risk-assessment, event-tree, fault-tree, initiating-events, minimal-cut-sets, core-damage-frequency, cdf, lerf, fussell-vesely, risk-achievement-worth, raw, birnbaum, common-cause-failure, alpha-factor, cafta, saphire, riskspectrum, nureg-cr-6928, reg-guide-1-200, reg-guide-1-174, asme-ans-ra-s, hra]
level: advanced
status: gated
description: "Build and quantify a Level 1 PRA: initiating events, event trees, fault trees, common-cause failure, minimal cut sets, CDF, F-V/RAW importance, using CAFTA, SAPHIRE or RiskSpectrum."
sources:
  - "ASME/ANS RA-S, Standard for Level 1/Large Early Release Frequency PRA for Nuclear Power Plant Applications"
  - "US NRC Regulatory Guide 1.200, Acceptability of PRA Results for Risk-Informed Activities"
  - "US NRC Regulatory Guide 1.174, Use of PRA in Risk-Informed Decisions on Plant-Specific Changes"
  - "NUREG/CR-6928, Industry-Average Performance for Components and Initiating Events at US Commercial Nuclear Power Plants (and later parameter updates)"
  - "NUREG/CR-5485, Guidelines on Modeling Common-Cause Failures in PRA"
  - "NUREG/CR-6883, The SPAR-H Human Reliability Analysis Method"
  - "IAEA SSG-3, Development and Application of Level 1 PSA for Nuclear Power Plants"
  - "NUREG-0492, Fault Tree Handbook"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PRA fault and event trees — from initiating event to core damage frequency

**Goal:** build a Level 1 internal-events PRA model whose core damage frequency (CDF), dominant cut sets and importance measures can be trusted for risk-informed decisions.

Engineering guidance only. A PRA used for regulatory applications must meet the applicable PRA standard and regulator guidance (in the US, ASME/ANS RA-S as endorsed by RG 1.200) and pass a peer review.

## 1. Initiating events

Group initiators by the mitigating functions they challenge: general transients, loss of main feedwater, loss of offsite power (LOOP), small/medium/large LOCAs, steam generator tube rupture, interfacing-system LOCA, loss of support systems (component cooling, service water, DC bus). Frequencies from NUREG/CR-6928 industry data (and its periodic parameter-estimate updates), Bayesian-updated with plant experience.

## 2. Success criteria

For each initiator, determine what minimum equipment prevents core damage — e.g. "1 of 2 AFW pumps to 1 of 2 SGs" — from thermal-hydraulic analyses (MAAP, RELAP5/TRACE; see engineering-technology.nuclear-engineering.thermal-hydraulics.critical-heat-flux-margin-analysis). Core damage is usually defined as peak cladding temperature exceeding ~1204 °C (2200 °F; the 10 CFR 50.46(b)(1) acceptance limit is 2200 °F per eCFR, and (2200-32)/1.8 = 1204.4 computed) or a collapsed level below top of active fuel for a set time; state your surrogate.

## 3. Event trees

- Headers in chronological order of the safety functions: reactor trip, RCS pressure control, secondary heat removal, feed-and-bleed, ECCS injection, recirculation, containment heat removal.
- Each sequence ends OK, core damage (CD) or transfer (to an ATWS or SGTR tree, for instance).
- Keep dependencies explicit: a header failure changes later success criteria — use split fractions or linked fault trees with house events.

## 4. Fault trees

- Top event = failure of a header's function under its success criterion. Develop to basic events at component failure-mode level: fail to start (per demand), fail to run (λ_run · mission time, typically 24 hgated: unconfirmed, source is paywalled or blocked), unavailable for test/maintenance, operator action failure, support-system failure.
- Standby component unavailability with periodic test interval T: Q ≈ λ_s·T/2 (standard first-order result for a standby component with undetected failures; e.g. λ = 1e-5/h, T = 720 h gives 3.6e-3).
- **Common-cause failure:** model CCF groups for redundant identical components (pumps, valves, diesels, batteries). Use alpha-factor or MGL parameters (NUREG/CR-5485/5497 data); for 2-of-2 redundancy the CCF event typically dominates over independent double failures.
- **Human reliability:** pre-initiator (miscalibration), post-initiator (diagnosis + execution). Use SPAR-H, THERP/CBDT or ASEP; assess **dependency** between actions in the same cut set — combined HEP floors (e.g. ~1e-5 to 1e-6 per combinationgated: unconfirmed, source is paywalled or blocked) are commonly applied; confirm the floor your guidance accepts.

## 5. Quantification

- Tools: CAFTA (EPRI, with FTREX/PRAQuant), SAPHIRE 8 (INL/NRC), RiskSpectrum PSA. Generate minimal cut sets (MCS) per sequence, sum with the rare-event approximation or min-cut upper bound.
- **Truncation:** set the limit so that lowering it by a decade changes CDF by < ~5%; typical cutoffs are 1e-11 to 1e-12 /yr for a CDF in the 1e-5 to 1e-6 rangegated: unconfirmed, source is paywalled or blocked).
- Apply recovery rules (offsite power recovery curves, repair) as post-processing only where justified, and delete mutually exclusive cut sets (e.g. two trains in maintenance at once if Tech Specs forbid it).
- Parametric uncertainty: lognormal distributions with error factors; propagate by Monte Carlo/LHS with state-of-knowledge correlation for identical components. Report mean, 5th and 95th percentiles.

## 6. Importance measures

| Measure | Meaning | Common significance threshold |
|---|---|---|
| Fussell-Vesely (F-V) | fraction of CDF from cut sets containing the event | > 0.005 (gated: secondary sources only) |
| Risk Achievement Worth (RAW) | CDF(event failed) / CDF | > 2 (gated: secondary sources only) |
| Risk Reduction Worth (RRW) | CDF / CDF(event perfect) | — |
| Birnbaum | ∂CDF/∂P(event) | — |

F-V 0.005 and RAW 2 are the component risk-significance criteria reported in NRC and industry papers on NEI 00-04 (RG 1.201 endorses NEI 00-04 Rev. 0); only secondary sources were read, so confirm in NEI 00-04 or RG 1.201 (gated: unconfirmed). Common-cause RAW and system-level RAW use different criteria. Use the ones your application specifies. Benchmarks for decisions (RG 1.174): ΔCDF < 1e-6/yr and ΔLERF < 1e-7/yr are "very small"; NRC subsidiary objectives of CDF < 1e-4/yr and LERF < 1e-5/yr (gated: unconfirmed, the NRC PDF fetch returned only a cover sheet; confirm in the current RG 1.174).

## Gotchas

- Circular logic between support systems (AC needs cooling water, cooling water needs AC) must be broken deliberately, or quantification silently drops cut sets.
- Truncation set too high hides CCF and multi-HFE cut sets — exactly the ones that matter.
- Missing CCF across component types or diverse trains is sometimes right; missing it within identical trains is never right.
- Over-crediting operator recovery in the dominant sequences is the classic peer-review finding.

## Verify

- [ ] Every initiator group has a documented frequency source and success criteria tied to T-H analyses.
- [ ] CDF converged with respect to truncation (lowering a decade changes it < 5%).
- [ ] Top 50-100 cut sets reviewed by system engineers and operators for realism and illogical combinations.
- [ ] CCF modelled for all redundant identical components; HFE dependencies assessed.
- [ ] Mean CDF and uncertainty bounds reported; F-V and RAW lists generated and sanity-checked.
- [ ] Model compared with a similar-plant SPAR model or prior revision and differences explained.
