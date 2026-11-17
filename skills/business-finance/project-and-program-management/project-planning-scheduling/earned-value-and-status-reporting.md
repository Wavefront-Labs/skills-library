---
id: business-finance.project-and-program-management.project-planning-scheduling.earned-value-and-status-reporting
name: earned-value-and-status-reporting
category: business-finance
field: project-and-program-management
product: project-planning-scheduling
tags: [project-and-program-management, project-planning-scheduling, project-management, earned-value, evm, earned-value-management, cpi, spi, eac, etc, tcpi, bac, planned-value, actual-cost, wbs, baseline, change-control, status-report, rag-status, critical-path, earned-schedule, pmbok, project-controls]
level: practitioner
status: draft
description: "Track projects with earned value: baseline and WBS prerequisites, EV credit rules, PV/EV/AC, CPI, SPI, EAC and TCPI with a worked example, and a one-page status report."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Earned value tracking and status reporting

**Goal:** know objectively whether a project is ahead or behind on schedule and
cost — and forecast where it will finish — instead of reporting "80% done" by feel.

## 1. Prerequisites
EVM only works on a decent plan:
- **WBS** decomposed to work packages small enough to measure (rule of thumb: 1–4
  weeks or ≤ ~80 hours of effort each).
- Each work package has a **budget** (hours or money) and is **scheduled** in time.
- A **baseline** is frozen (scope, schedule, budget). Changes go through change
  control and re-baseline only that portion.
- Actual cost (or hours) is captured per work package, on the same basis as the budget.

## 2. The three numbers (at the status date)
- **PV — planned value:** budget of the work *scheduled* to be done by now.
- **EV — earned value:** budget of the work *actually completed* by now.
- **AC — actual cost:** what that work actually cost.
**BAC** = total budget at completion.

How to credit EV: use objective rules, set up front:
- **0/100** (credit only when finished) for short packages;
- **50/50** (half at start, half at finish);
- **milestones/weighted steps** for longer packages;
- % complete by physical measure (metres laid, documents approved) — never "% of hours spent".

## 3. Worked example
BAC = 100k. Month 4: PV = 40k, EV = 32k, AC = 38k.
| Metric | Formula | Value | Reading |
|---|---|---|---|
| Schedule variance | EV − PV | −8k | Behind schedule |
| Cost variance | EV − AC | −6k | Over budget |
| SPI | EV ÷ PV | 0.80 | Getting 80% of planned progress |
| CPI | EV ÷ AC | 0.84 | Each 1.00 spent earns 0.84 |
| EAC (if CPI persists) | BAC ÷ CPI | ≈118.8k | Forecast final cost |
| ETC | EAC − AC | ≈80.8k | Still to spend |
| VAC | BAC − EAC | ≈−18.8k | Expected overrun |
| TCPI | (BAC − EV) ÷ (BAC − AC) | ≈1.10 | Efficiency needed to finish on budget |
A TCPI well above 1.0 (here 1.10 vs a CPI of 0.84) means "finish on budget" is not
credible; report a revised forecast rather than hoping.

Alternative EAC formulas exist (e.g. AC + (BAC − EV) if the overrun was a one-off;
including SPI if schedule pressure drives cost). State which you used.

## 4. Schedule caution
SPI drifts toward 1.0 near the end because EV eventually equals PV at completion
even if late. Use the **critical path** (float consumed, forecast finish of critical
tasks) for schedule judgement, and SPI as a supporting signal. *Earned schedule*
is an extension that addresses this.

## 5. Status report (one page)
- Overall RAG with **objective thresholds** (e.g. green CPI/SPI ≥ 0.95, amber 0.90–0.95,
  red < 0.90 — set per organisation).
- Key metrics: CPI, SPI, EAC vs BAC, forecast end date vs baseline.
- Milestones: done / next / at risk.
- Top risks and issues with owners and actions; decisions needed from sponsors.
- Changes approved since last report.

## Gotchas
- **Front-loading EV:** crediting progress generously early, then a long "90% done" tail.
- AC captured late (invoices lag) makes CPI look great; accrue costs.
- Scope creep without change control makes all numbers meaningless.
- EVM on a level-of-effort activity (PMO support) is not meaningful; EV = PV by definition.

## Verify
- [ ] Baseline frozen; changes go through change control.
- [ ] EV credited by pre-agreed objective rules per work package.
- [ ] CPI, SPI, EAC and TCPI computed and the EAC formula stated.
- [ ] Schedule judgement uses the critical path, not SPI alone.
- [ ] Report RAG follows stated thresholds and lists decisions needed.
