---
id: computing-software.cybersecurity-defensive.security-operations.soc-capacity-planning
name: soc-capacity-planning
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, soc-capacity-planning, analyst-workload, erlang, alert-volume, staffing-model, queue-management, utilisation]
level: advanced
status: draft
description: "Size SOC staffing from data: alert arrival rates, handle times, utilisation targets, 24x7 shift maths, queue SLAs, and what to change before hiring more analysts."
sources: ["https://www.mitre.org/sites/default/files/2022-04/11-strategies-of-a-world-class-cybersecurity-operations-center.pdf", "https://www.soc-cmm.com/", "https://en.wikipedia.org/wiki/Erlang_(unit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC capacity planning

## Measure the work
From the case/alert system over 90 days:
- **Arrival rate** per hour of week (alerts and cases), not just daily totals: peaks drive staffing.
- **Handle time** per alert type: median and 90th percentile, triage vs full investigation.
- **Escalation ratio**: share of tier 1 alerts escalated to tier 2.
- Non-alert work: hunts, tuning, projects, training, meetings (often 30-40% of time).

## Basic arithmetic
Workload hours per day = sum over alert types (count x handle time) + case work.
Effective analyst hours per shift = shift length x productive utilisation (target ~60-70%;
above 80% queues explode and burnout follows).
Analysts needed per shift = workload hours in that shift / effective hours.

For queue SLAs (e.g. 90% of high alerts picked up within 15 minutes), use queueing (Erlang C)
calculators with arrival rate and handle time per interval; averages underestimate staffing for
bursty arrivals.

## 24x7 coverage
One seat covered 24x7x365 needs ~4.2-5 FTE after leave, training and sickness (8760 hours /
~1800-2000 productive hours per FTE). Two seats at night minimum for safety and escalation.
Options: follow-the-sun across regions, MDR for nights, on-call tier 2 overnight.

## Reduce demand before adding headcount
1. Tune the top 10 noisiest rules (often >50% of volume).
2. Automate enrichment and the top repetitive dispositions (phishing reports, known benign).
3. Move low-fidelity rules to risk scoring.
4. Fix data quality issues that make investigations slow (missing asset/identity context).
Model each change's saved hours; present to leadership with the staffing gap that remains.

## Track
Monthly: alerts per analyst-hour, utilisation, SLA attainment by severity, backlog age, overtime,
attrition. Rising backlog with flat volume = handle time growing (complexity or tooling issues).

## Gotchas
- Counting alerts without handle time hides that a few complex alert types eat most time.
- Ignoring ramp-up: new analysts take 3-6 months to reach full productivity.
- Planning to 100% utilisation leaves no room for incidents, which are bursty by nature.

## Verify
Back-test the model on last quarter: predicted SLA attainment for actual staffing should match the
measured attainment within a few percent.
