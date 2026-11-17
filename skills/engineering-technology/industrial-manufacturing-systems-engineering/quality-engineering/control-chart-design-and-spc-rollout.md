---
id: engineering-technology.industrial-manufacturing-systems-engineering.quality-engineering.control-chart-design-and-spc-rollout
name: control-chart-design-and-spc-rollout
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: quality-engineering
tags: [spc, statistical-process-control, control-chart, shewhart, xbar-r, xbar-s, i-mr, individuals-chart, p-chart, np-chart, c-chart, u-chart, rational-subgrouping, control-limits, western-electric-rules, nelson-rules, process-capability, cpk, ppk, cp, msa, gauge-rr, measurement-system-analysis, ndc, aiag, iatf-16949, reaction-plan, control-plan, minitab, jmp, quality-engineering]
level: practitioner
status: gated
description: "Design SPC for a characteristic: MSA gate, rational subgrouping, X-bar/R, I-MR or attribute chart choice, control-limit formulas, run rules, Cpk vs Ppk and reaction plans."
sources:
  - "Montgomery, Introduction to Statistical Quality Control"
  - "AIAG, Statistical Process Control (SPC) reference manual"
  - "AIAG, Measurement Systems Analysis (MSA) reference manual"
  - "Wheeler, Understanding Statistical Process Control"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-chart design and SPC rollout

**Goal:** put a control chart on the characteristics that matter, built so that a
signal means the process changed and an operator knows exactly what to do about it.

## 1. Choose what to chart
Chart the **process** inputs or outputs that drive a critical characteristic (from the
PFMEA and control plan), not every dimension on the drawing. Prefer charting a
controllable input (mould temperature, torque) when it predicts the output well.

## 2. Pass the measurement gate first (MSA)
A gauge that cannot see the variation makes the chart noise. Run a crossed gauge
R&R (typically 10 parts spanning the process range × 3 operators × 2-3 trials; ANOVA
method in Minitab/JMP). AIAG-style guidance (thresholds confirmed only in secondary study guides, not the paywalled manual (gated: unconfirmed, source is paywalled or blocked); check the current MSA edition and the customer's requirement):
- %GRR (vs study variation or tolerance, state which) < 10% acceptable; 10-30% may be
  acceptable depending on application and cost; > 30% unacceptable.
- **Number of distinct categories (ndc) ≥ 5.**
Also confirm resolution: the gauge should read to about 1/10 of the tolerance or process spread.

## 3. Design rational subgroups
A subgroup should contain only common-cause variation: consecutive parts from one
stream (one cavity, one spindle), taken close together. Variation between subgroups
is then what the chart tests. Mixing 4 cavities in one subgroup inflates R and gives
limits so wide the chart never signals. Frequency: often enough to catch a shift
before much product is made (e.g. 5 consecutive parts every hour, more after changeovers).

## 4. Pick the chart
- Variables, subgroup n = 2-9: **X-bar & R**. n ≥ 10: X-bar & S.
- Variables, one reading at a time (batch chemistry, slow processes): **I-MR**.
- Attributes: defectives → **p** (varying n) or **np** (constant n); defects → **c**
  (constant area) or **u** (varying).

## 5. Compute limits from the process (never from the spec)
Collect 20-25 subgroups (~100 readings) from a stable period.
- X-bar & R, n = 5 (A2 = 0.577, D3 = 0, D4 = 2.114, d2 = 2.326; recomputed from the normal range distribution: d2 = 2.326, A2 = 0.5768, D4 = 2.115 by simulation, tables give 2.114):
  UCL/LCL(x̄) = x̿ ± A2·R̄; UCL(R) = D4·R̄; σ_within = R̄ ÷ d2.
- I-MR: limits = x̄ ± 2.66·MR̄; UCL(MR) = 3.267·MR̄ (computed: 3/1.128 = 2.66, 1 + 3·0.8525/1.128 = 3.267).
- p chart: p̄ ± 3·√(p̄(1 - p̄) ÷ n).

Worked example: x̿ = 25.002 mm, R̄ = 0.040 mm, n = 5 → x̄ limits 24.979 to 25.025 mm;
R UCL 0.085 mm; σ_within = 0.0172 mm (all recomputed; Cpk below also recomputed). Remove only subgroups with an identified,
corrected special cause, then recompute once.

## 6. Capability, after stability
Only a stable (in-control) process has a meaningful capability.
- **Cpk** = min(USL - μ, μ - LSL) ÷ (3·σ_within). Spec 25.00 ± 0.08:
  min(0.078, 0.082) ÷ 0.0516 ≈ **1.51**.
- **Ppk** uses overall standard deviation s; Ppk well below Cpk means drift between
  subgroups that the chart should already be showing.
Common targets: Cpk ≥ 1.33 for ongoing production, ≥ 1.67 for initial/special
characteristics in automotive PPAP (commonly quoted (gated: unconfirmed, source is paywalled or blocked)); confirm the customer's requirement.

## 7. Run rules and reaction plan
Use a small, fixed set of rules (e.g. Western Electric/Nelson: 1 point beyond 3σ;
2 of 3 beyond 2σ same side; 7-9 in a row one side of centre; 6 trending). More rules =
more false alarms. Write the **reaction plan** per chart: stop/contain, check gauge,
check the known causes in order, who to call, how to disposition suspect parts since
the last good subgroup. Recalculate limits only after a deliberate process change.

## Gotchas
- Spec limits on a control chart turn it into a sorting chart; keep them off.
- Autocorrelated data (continuous processes) gives false signals on I-MR; consider
  longer sampling intervals or time-series methods.
- Tool-wear processes trend by design; use a sloped centreline or adjust-by-rule.

## Verify
- [ ] Gauge R&R passed (%GRR basis stated, ndc ≥ 5) before charting.
- [ ] Subgroups are rational: one stream, consecutive parts.
- [ ] Limits computed from ≥ 20 subgroups of process data, not from the specification.
- [ ] Cpk reported only for a stable process, alongside Ppk.
- [ ] Each chart has a written reaction plan the operator can follow.
