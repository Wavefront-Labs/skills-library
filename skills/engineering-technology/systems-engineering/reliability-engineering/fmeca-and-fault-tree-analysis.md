---
id: engineering-technology.systems-engineering.reliability-engineering.fmeca-and-fault-tree-analysis
name: fmeca-and-fault-tree-analysis
category: engineering-technology
field: systems-engineering
product: reliability-engineering
tags: [reliability-engineering, rams, fmea, fmeca, mil-std-1629a, iec-60812, aiag-vda-fmea, action-priority, rpn, criticality-analysis, fault-tree-analysis, fta, iec-61025, minimal-cut-sets, mtbf, mttr, failure-rate, fit, reliability-block-diagram, rbd, availability, mil-hdbk-217f, telcordia-sr-332, exponential-distribution, redundancy]
level: advanced
status: gated
description: "Run FMEA/FMECA (MIL-STD-1629A, IEC 60812, AIAG-VDA action priority) and fault trees (IEC 61025), then quantify with failure rates, MTBF, reliability block diagrams and availability."
sources: ["MIL-STD-1629A Procedures for Performing a Failure Mode, Effects and Criticality Analysis", "IEC 60812:2018 Failure modes and effects analysis", "AIAG & VDA FMEA Handbook (2019)", "IEC 61025:2006 Fault tree analysis", "NUREG-0492 Fault Tree Handbook", "MIL-HDBK-217F Notice 2", "Telcordia SR-332", "IEC 61078 Reliability block diagrams"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FMECA and fault tree analysis — bottom-up and top-down, then put numbers on it

**Goal:** find how the system can fail (FMEA, bottom-up), how a specific undesired event can happen (FTA, top-down), and quantify reliability and availability so design decisions are based on numbers. This is engineering guidance; safety-critical programmes must follow their governing standard (e.g. ARP4761, ISO 26262, IEC 61508) and independent review.

## 1. FMEA / FMECA
**Setup:** define system boundary, indenture level (functional or hardware/piece-part), mission phases, and the failure definition. Base it on the current functional architecture.

**Worksheet columns (MIL-STD-1629A Task 101 / IEC 60812; the column list is the usual practice and IEC 60812 (gated: unconfirmed, source is paywalled or blocked)):** item/function, failure mode, cause/mechanism, mission phase, local effect, next-higher effect, end effect, detection method, compensating provisions, severity, remarks/actions.

**Severity classes (1629A):** I Catastrophic, II Critical, III Marginal, IV Minor (checked against the NASA-hosted copy of MIL-STD-1629A, section 4.4).

**Criticality (Task 102, quantitative):**
C_m = β · α · λ_p · t, and item criticality C_r = Σ C_m over modes of that severity,
where λ_p = part failure rate, α = failure-mode ratio (modes of a part sum to 1.0), β = conditional probability the mode produces the end effect (1.0 actual, above 0.1 to below 1.0 probable, above 0 to 0.1 possible, 0 none; checked in 1629A Task 102, 3.2.1.2), t = operating time. Plot on a criticality matrix (severity vs. C_r or probability level A–E).

**Risk ranking — RPN vs. AP:**
- Classic **RPN = S × O × D** (each 1–10, range 1–1000). Weakness: equal RPNs hide very different risks (S=10, O=1, D=10 and S=1, O=10, D=10 both score 100); thresholds like "act if RPN > 100" are arbitrary.
- **AIAG-VDA (2019) Action Priority** replaces RPN with a lookup table giving **High / Medium / Low** priority, weighting severity first, then occurrence, then detection. Any S = 9–10 with non-trivial occurrence lands High ((gated: unconfirmed, source is paywalled or blocked), AIAG-VDA handbook is paid). Its seven steps ((gated: unconfirmed, source is paywalled or blocked)): planning & preparation, structure, function, failure analysis, risk analysis, optimisation, results documentation.

## 2. Fault tree analysis (IEC 61025)
1. Define one precise **top event** ("loss of propulsion thrust > 5 s during ascent").
2. Develop downward with gates: **OR** (any input), **AND** (all inputs), **k-out-of-n / voting**, **INHIBIT** (input plus condition), **PRIORITY-AND** (sequence, dynamic). Leaves: basic events, undeveloped events, house events (switched on/off for configurations).
3. Find **minimal cut sets** (Boolean reduction / MOCUS). Single-element cut sets are single-point failures — list them.
4. Quantify (independent events): AND → P = Π p_i; OR → P = 1 − Π(1 − p_i) ≈ Σ p_i when small. Top event ≈ Σ P(MCS) (rare-event approximation, valid when each term ≪ 0.1).
5. Importance: Fussell–Vesely and Birnbaum rank which basic events to fix.
6. Model **common-cause failures** (e.g. beta-factor, β ≈ 1–10 % of the component rate (gated: unconfirmed, source is paywalled or blocked)) for redundant identical units — otherwise redundancy looks far better than it is.

## 3. Reliability numbers
- Constant failure rate (useful-life region): R(t) = e^(−λt), **MTBF = 1/λ**. At t = MTBF, R = 0.368 (computed e^-1 = 0.3679).
- **FIT** = failures per 10⁹ h. 2,000 FIT → λ = 2×10⁻⁶ /h → MTBF = 500,000 h (computed).
- Prediction sources: MIL-HDBK-217F N2 (dated, still contract-cited), Telcordia SR-332, FIDES, field data (preferred).
- **RBD:** series R_s = Π R_i (λ_s = Σ λ_i); parallel R_p = 1 − Π(1 − R_i); k-out-of-n with identical units R = Σ_{i=k..n} C(n,i) R^i (1−R)^(n−i).
- **Availability:** inherent A_i = MTBF / (MTBF + MTTR); operational A_o = MTBM / (MTBM + MDT) includes logistics delay. Example: MTBF 5,000 h, MTTR 4 h → A_i = 0.9992 (computed 0.99920).
- Demonstration (time-terminated test, r failures in T hours): lower confidence bound MTBF_L = 2T / χ²(1−CL; 2r+2) — check the χ² tail convention of your table (convention checked: with r = 0 the formula must equal T / -ln(1-CL); scipy chi2.ppf(CL, 2r+2) gives 434 h for T = 1000, CL = 0.9, matching 434 h; the upper-tail notation above corresponds to the CL quantile).

## Gotchas
- FMEA done after design freeze is paperwork; run it at PDR and update at CDR.
- Mixing hardware and functional FMEA levels in one worksheet double-counts effects.
- 1/λ is meaningless for wear-out items (bearings, batteries, seals); use Weibull with β > 1.
- MTBF of 500,000 h does not mean a unit lasts 57 years (500,000 / 8,766 = 57.0).
- FTA assumes independence unless you model dependence; shared power, software or environment breaks it.
- Feed failure-mode verification items into engineering-technology.systems-engineering.verification-validation.verification-cross-reference-matrix.

## Verify
- [ ] FMEA boundary, indenture level and severity scale documented; every Cat I/II or AP-High item has an action with owner.
- [ ] Failure-mode ratios α sum to 1.0 per item.
- [ ] Fault tree top event is specific; minimal cut sets listed; all single-point failures dispositioned.
- [ ] Common-cause failures modelled for redundant identical items.
- [ ] RBD, FTA and FMEA use the same failure-rate dataset and mission time.
- [ ] Predicted reliability/availability compared against the allocated requirement with stated margin.
