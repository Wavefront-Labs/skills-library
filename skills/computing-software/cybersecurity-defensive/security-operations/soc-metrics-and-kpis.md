---
id: computing-software.cybersecurity-defensive.security-operations.soc-metrics-and-kpis
name: soc-metrics-and-kpis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, soc-metrics, mttd, mttr, mean-time-to-respond, dwell-time, kpi, sla, detection-coverage, false-positive-rate]
level: practitioner
status: draft
description: "Define SOC metrics that drive improvement (MTTD, MTTR, dwell time, TP rate, coverage) with exact start/stop points and avoid metrics that reward noise."
sources: ["CySA+ CS0-003 objective 4.2 (MTTD, MTTR, alert volume)", "SANS SOC Survey", "MITRE 11 Strategies of a World-Class Cybersecurity Operations Center (Strategy 11, metrics)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC metrics and KPIs

**Goal:** a small set of measured numbers that tell leadership whether the SOC finds and
stops threats fast, and tell the SOC where to improve.

## Define each metric precisely
| Metric | Start | Stop | Note |
|---|---|---|---|
| Time to detect (MTTD) | First malicious activity (from investigation) | First alert or report | Only computable for confirmed incidents; report median |
| Time to acknowledge / triage | Alert created | Analyst first action | Queue health, per priority |
| Time to contain | Incident declared | Containment confirmed | Business impact proxy |
| Time to resolve (MTTR) | Incident declared | Closed (eradicated and recovered) | Long tails are normal: use median and p90 |
| Dwell time | First malicious activity | Containment | Comparable with industry reports |
| True-positive rate | TP alerts / all alerts per detection | | Drives tuning |
| Detection coverage | ATT&CK techniques with a tested detection / techniques in scope | | Programme progress |
| Escaped incidents | Incidents found by third parties or users before the SOC | | The most honest quality signal |

## Practice
1. Make disposition, incident start time and containment time mandatory fields at close.
2. Report medians and p90, by priority, monthly; trends matter more than absolute values.
3. Pair speed with quality: fast triage with a rising escaped-incident count is failure.
4. Review each metric quarterly: if no decision has come from it, drop it.

## Avoid
- Alerts closed per analyst as a performance target: rewards closing without investigating.
- Raw alert volume as success.
- Means for time metrics: one forgotten case dominates.
- Comparing SOCs with different definitions of "incident".

## Gotchas
- SOAR auto-closures distort time-to-triage: report human-handled and automated separately.
- MTTD depends on how hard you look for the start time; document the method.
- Clock sources differ between tools; compute with epoch times from one system of record.

## Verify
- [ ] Each metric has a written definition with start/stop events and data source.
- [ ] A sample of 10 incidents recalculated by hand matches the dashboard.
