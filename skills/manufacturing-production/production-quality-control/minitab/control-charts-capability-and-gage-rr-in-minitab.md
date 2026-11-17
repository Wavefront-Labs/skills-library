---
id: manufacturing-production.production-quality-control.minitab.control-charts-capability-and-gage-rr-in-minitab
name: control-charts-capability-and-gage-rr-in-minitab
category: manufacturing-production
field: production-quality-control
product: minitab
tags: [minitab, minitab-statistical-software, control-charts, xbar-r, xbar-s, i-mr, p-chart, u-chart, tests-for-special-causes, process-capability, capability-sixpack, cp, cpk, pp, ppk, normality-test, anderson-darling, box-cox, johnson-transformation, nonnormal-capability, gage-rr, crossed-gage-rr, anova-method, ndc, number-of-distinct-categories, attribute-agreement-analysis, doe, factorial-design, assistant-menu, stat-menu, spc, msa, six-sigma, quality-statistics, jmp, production-quality-control]
level: practitioner
status: draft
description: "Do the core production quality analyses in Minitab: lay out data, build control charts with the right tests, run capability (normal and non-normal), crossed gage R&R, and a basic factorial DOE."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control charts, capability and gage R&R in Minitab

**Goal:** get from a column of production measurements to a defensible chart, Cpk or
gage R&R result in Minitab, without the classic layout and option mistakes. Menu paths
are from Minitab Statistical Software 20–22 (desktop/web); older versions differ slightly.
JMP has equivalents under Analyze › Quality and Process. Choosing *which* chart and
subgroup design is in
engineering-technology.industrial-manufacturing-systems-engineering.quality-engineering.control-chart-design-and-spc-rollout.

## 1. Data layout (most errors start here)
- **One column per variable, one row per observation** (stacked). Add columns for
  subgroup ID, date/time, machine, operator, part.
- For subgrouped charts, either a subgroup-ID column or a constant subgroup size.
- Text in a numeric column (e.g. "NA", "<0.1") turns the column to text (header shows `-T`) — clean it.

## 2. Control charts
`Stat › Control Charts › Variables Charts for Subgroups › Xbar-R` (n ≤ ~8) or `Xbar-S`
(larger n); `Variables Charts for Individuals › I-MR` for single readings;
`Attributes Charts › P` (proportion defective, varying n) or `U` (defects per unit).
- **Xbar-R Options › Tests**: turn on the tests you'll actually react to (Test 1 point
  beyond 3σ is default; many plants add 2 (9 in a row one side) and 5/6). More tests = more false alarms.
- **Estimate** tab: compute limits from a known stable baseline period only (`Use the following subgroups`), then
  **Options › Parameters** to fix historical mean/σ for ongoing monitoring — otherwise
  limits move every time you add data.
- **Stages** (Options › Stages) to show limit changes after a documented process change.
- I-MR on non-normal data (e.g. flatness, particle counts) gives misleading limits —
  check normality first or chart a transformed variable.

## 3. Capability
1. Check stability first (control chart). Capability of an unstable process is meaningless.
2. `Stat › Basic Statistics › Normality Test` (Anderson-Darling). p < 0.05 → not normal.
3. Normal: `Stat › Quality Tools › Capability Analysis › Normal` — enter subgroup size or ID column, LSL/USL.
   `Capability Sixpack` gives chart + normality + capability on one page.
4. Non-normal: `Capability Analysis › Nonnormal` with a fitted distribution (use
   `Individual Distribution Identification` to choose) or Box-Cox/Johnson transformation.
- **Cp/Cpk** use within-subgroup σ (potential); **Pp/Ppk** use overall σ (actual
  performance). Customers (e.g. automotive PPAP) often require Ppk ≥ 1.67 initial,
  Cpk ≥ 1.33 ongoing — check the customer manual.
- Report **with confidence intervals** (Options › Include confidence intervals) for small samples.

## 4. Gage R&R (crossed)
Study design: typically 10 parts spanning the process range, 3 operators, 2–3 trials,
randomised and blind. Lay out columns Part, Operator, Measurement.
`Stat › Quality Tools › Gage Study › Gage R&R Study (Crossed)` → **ANOVA** method.
- Enter **Process tolerance** in Options to get %Tolerance as well as %Study Var.
- Read: **%Study Var (or %Tolerance) < 10% acceptable, 10–30% maybe, > 30% unacceptable** (AIAG MSA);
  **ndc ≥ 5**.
- Operator × Part interaction significant → operators measure some parts differently (technique/fixture).
- Attribute (pass/fail) gauges: `Attribute Agreement Analysis`; look at kappa and agreement with standard.

## 5. Basic DOE
`Stat › DOE › Factorial › Create Factorial Design` (e.g. 2-level, 3 factors, full,
2 replicates, centre points) → run in randomised order shown → enter responses →
`Analyze Factorial Design` → Pareto of effects, then reduce the model, check residual plots.

## Gotchas
- Using Xbar-R limits calculated from data that include the out-of-control period.
- Entering the wrong subgroup size → wildly wrong within-σ and Cpk.
- Running gage R&R with parts all from a narrow production slice → %Study Var looks terrible.
- Reporting Cpk on 20 points without confidence intervals.

## Verify
- [ ] Data stacked, numeric columns numeric, subgroup ID correct.
- [ ] Control limits come from a stable baseline and are fixed for monitoring.
- [ ] Normality checked before choosing capability method; Cp/Cpk vs Pp/Ppk stated correctly.
- [ ] Gage R&R uses ANOVA with tolerance entered; %Tol/%SV and ndc reported.
- [ ] Every output saved with the project file and the data date range.
