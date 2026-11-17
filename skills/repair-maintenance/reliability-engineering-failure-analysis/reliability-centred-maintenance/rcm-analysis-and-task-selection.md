---
id: repair-maintenance.reliability-engineering-failure-analysis.reliability-centred-maintenance.rcm-analysis-and-task-selection
name: rcm-analysis-and-task-selection
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: reliability-centred-maintenance
tags: [reliability-centred-maintenance, rcm, rcm2, sae-ja1011, sae-ja1012, maintenance-strategy, failure-modes, functional-failure, failure-consequences, hidden-failures, condition-based-maintenance, pf-interval, preventive-maintenance, pm-optimisation, run-to-failure, failure-finding, redesign, asset-criticality, cmms, maintenance-planning]
level: advanced
status: draft
description: "Run an RCM analysis on an asset: functions, functional failures, failure modes, consequence logic, then pick on-condition, scheduled, failure-finding or run-to-failure tasks with justified intervals."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RCM analysis and maintenance task selection

**Goal:** decide what maintenance an asset should get — and what it shouldn't —
from how it fails and what each failure costs, instead of copying OEM manuals or
"we've always changed it every 6 months".

> Draft: this follows the logic of SAE JA1011/JA1012-style RCM. Rigorous RCM is
> facilitated, cross-functional and slow; "RCM-lite" versions trade rigour for speed —
> say which you did.

## 0. Pick the right assets
RCM is expensive (often 1–3 days of a team per complex system). Use a **criticality
ranking** first (safety, environment, production loss, cost) and apply full RCM to
the top ~10–20%; use simpler PM review for the rest.

## 1. The team and the boundary
Facilitator + operator + maintainer (mechanical/electrical) + someone who knows
the process. Define the **system boundary** (from inlet flange to discharge valve,
including motor and starter?) and the **operating context** (duty/standby,
continuous/batch, redundancy, spares on site).

## 2. The seven questions, worked through in order
1. **Functions:** what must it do, to what standard? Write with numbers: "Transfer
   water from tank A to tank B at not less than 800 L/min." Include secondary functions
   (contain, protect, control, look acceptable).
2. **Functional failures:** each way it fails to meet the standard (total: no flow;
   partial: < 800 L/min; leaks).
3. **Failure modes:** the specific cause at a level you can act on — "impeller worn
   by abrasion", "mechanical seal fails due to dry running", "bearing fails from
   lubrication breakdown". Include human error and wear-out.
4. **Failure effects:** what happens — evidence of failure, safety/environment
   impact, production impact, repair time.
5. **Consequences** — classify in this order:
   - **Hidden** (nobody knows it failed in normal operation — protective devices,
     standby pumps, relief valves).
   - **Safety/environmental.**
   - **Operational** (affects output, quality, service).
   - **Non-operational** (repair cost only).
6. **Proactive task:** is there a task that is *technically feasible* and *worth doing*?
7. **Default action** if not.

## 3. Task selection logic
- **On-condition (CBM):** possible if there's a detectable potential failure (P) before
  functional failure (F). Inspection interval ≈ **half the P-F interval** (or less), and
  the remaining time after detection must be enough to act. E.g. bearing defect
  detectable by vibration ~3 months before failure → monthly vibration route.
- **Scheduled restoration/discard (time-based):** only if the mode has a clear
  **wear-out age** (Weibull β > 1 — see life-data skill) and most items survive to it.
  Random failure modes (most electronics, many bearings) get no benefit from
  time-based replacement — it can add infant mortality.
- **Failure-finding:** for hidden failures — test the protective device periodically.
  Rough interval: FFI ≈ 2 × MTBF(device) × tolerable unavailability. E.g. MTBF 50 years,
  tolerable 1% unavailability → FFI ≈ 2 × 50 × 0.01 = 1 year.
- **Defaults:** safety/environmental with no adequate task → **redesign mandatory**;
  operational/non-operational → **run-to-failure** if cheaper, or redesign.

## 4. Document and implement
Use a worksheet (one row per failure mode): function, FF, FM, effects, consequence
category, task, interval, who does it, rationale. Then:
- Load tasks into the CMMS with clear task instructions and acceptance criteria.
- Delete or change old PMs that RCM didn't justify (document why — auditors ask).
- Package tasks by craft and interval into routes.

## 5. Living programme
Feed back from work orders: failures that the analysis didn't predict, intervals
that find nothing (extend) or find too much (shorten). Review the analysis after
major failures or changes.

## Gotchas
- Functions written without a performance standard make every later step vague.
- Failure modes at "pump fails" level are useless — go down to cause.
- "Replace every year just in case" on random failures wastes money and introduces faults.
- Skipping hidden-function analysis is how protective devices sit failed for years.

## Verify
- [ ] Asset chosen from a criticality ranking; boundary and context written down.
- [ ] Functions have numeric standards; failure modes are at cause level.
- [ ] Each mode has a consequence category, with hidden failures identified first.
- [ ] Each task passes "feasible and worth doing"; intervals justified (P-F, wear-out age, FFI).
- [ ] Tasks loaded in CMMS and old unjustified PMs retired with rationale.
