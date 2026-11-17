---
id: architecture-construction.construction-estimating-scheduling.cpm-scheduling.forward-backward-pass-and-schedule-quality-checks
name: forward-backward-pass-and-schedule-quality-checks
category: architecture-construction
field: construction-estimating-scheduling
product: cpm-scheduling
tags: [construction-estimating-scheduling, cpm-scheduling, critical-path-method, cpm, forward-pass, backward-pass, early-start, late-finish, total-float, free-float, slack, critical-path, precedence-diagram, pdm, network-logic, dcma-14-point, schedule-assessment, open-ends, lags, leads, hard-constraints, high-float, crashing, fast-tracking, schedule-quality, aace]
level: practitioner
status: draft
description: "Compute a CPM network by hand (forward/backward pass, total and free float) and run the DCMA 14-point style quality checks on logic, lags, constraints and float."
sources: ["DCMA 14-Point Schedule Assessment", "AACE International Recommended Practices on CPM scheduling", "GAO Schedule Assessment Guide (GAO-16-89G)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forward/backward pass and schedule quality checks

**Goal:** understand exactly how software calculates dates and float, so you can check
it, explain it, and spot a schedule whose critical path is an artefact of bad logic.

## 1. The forward pass (earliest dates)
Use day-numbering where an activity starting at day 0 with duration 5 finishes at 5.
- Start activity: ES = 0. EF = ES + duration.
- For each successor via finish-to-start: ES = **max** of predecessors' (EF + lag).
- SS link: successor ES ≥ predecessor ES + lag. FF link: successor EF ≥ predecessor
  EF + lag.
- Project finish = the largest EF.

## 2. The backward pass (latest dates)
- Finish activity: LF = project EF (or the contract date if constrained).
  LS = LF − duration.
- For each predecessor: LF = **min** of successors' (LS − lag).
- **Total float** TF = LS − ES (= LF − EF). Time an activity can slip without delaying
  completion.
- **Free float** FF = min(successor ES) − EF − lag. Time it can slip without delaying
  any successor.
- **Critical path** = the longest chain, TF = minimum (0 when no constraints).

Worked mini-example: A(3) → B(5) → D(2); A → C(2) → D.
Forward: A 0–3, B 3–8, C 3–5, D 8–10. Backward: D 8–10, B 3–8, C 6–8, A 0–3.
C has TF = 3, FF = 3; A–B–D is critical.

## 3. Quality checks (DCMA 14-point thresholds as a common yardstick)
Run on incomplete activities. Thresholds commonly quoted:
| Check | Threshold |
|---|---|
| Missing logic (no pred or succ) | ≤ 5% |
| Leads (negative lags) | 0 |
| Lags | ≤ 5% of relationships |
| Relationship types FS | ≥ 90% |
| Hard constraints | ≤ 5% |
| High float (> 44 working days) | ≤ 5% |
| Negative float | 0 (or explained) |
| High duration (> 44 working days) | ≤ 5% |
| Invalid dates (actuals in future / forecasts in past) | 0 |
| Resources assigned | if required by contract |
| Missed tasks vs baseline | ≤ 5% |
| Critical path test | delaying a critical task delays finish |
| CPLI (critical path length index) | ≥ 0.95 |
| BEI (baseline execution index) | ≥ 0.95 |
These are assessment triggers, not laws; explain exceptions rather than gaming them.

## 4. Reading results
- **High float** usually = missing successor; add the logic to the real follower.
- **Negative float** = a constraint or contract date can't be met by the current logic.
- **Parallel near-critical paths** (TF within ~10 days of critical) are risky; report
  them alongside the critical path.
- **SS/FF pairs** are fine for overlap but each needs both ends tied or work can
  "float" freely at one end (dangling activities).

## 5. Shortening (when the finish is too late)
1. **Check logic first** — remove preferential links that aren't real.
2. **Fast-track**: overlap critical activities (FS → SS + lag) where risk is acceptable.
3. **Crash**: add resources to critical activities with the lowest cost per day saved;
   stop when another path becomes critical. Recalculate after every change.

## Gotchas
- Different calendars on linked activities produce float that doesn't add up by hand.
- Software "critical" flag may use TF ≤ 0 or longest path — know which.
- Progress override vs retained logic changes the remaining path after updates.
- Summary/hammock activities must not carry logic.
- Level-of-effort activities can appear on the critical path falsely.

## Verify
- [ ] You can hand-compute ES/EF/LS/LF and TF/FF for a small network and match the software.
- [ ] Every incomplete activity has a predecessor and successor (bar start/finish).
- [ ] Lags, leads and hard constraints are within thresholds or justified.
- [ ] High-float activities reviewed for missing logic.
- [ ] Critical path test: extending a critical activity extends completion.
- [ ] Near-critical paths reported.
