---
id: computing-software.digital-forensics-incident-response.incident-response-process.ir-program-metrics
name: ir-program-metrics
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ir-metrics, mttd, mttr, dwell-time, kpi, dfir]
level: practitioner
status: draft
description: "Measure an IR program with defensible metrics (dwell time, MTTD, MTTA, MTTC, MTTR, recurrence) using consistent timestamps and definitions."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://cloud.google.com/security/resources/m-trends"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IR program metrics

**Goal:** numbers that show whether detection and response are improving, computed the same
way every quarter.

## Timestamps to record on every case (UTC)
| Field | Definition |
|---|---|
| T0 compromise | Earliest attacker activity found (revised as the investigation learns more) |
| T1 detection | First alert or report that, in hindsight, was this incident |
| T2 acknowledged | Analyst starts working the alert |
| T3 declared | Incident declared |
| T4 contained | Attacker can no longer act (last containment action verified) |
| T5 eradicated | Persistence and access removed |
| T6 recovered | Affected services back to normal |
| T7 closed | Post-incident review complete |

## Metrics
- **Dwell time** = T1 - T0. Benchmark against Mandiant M-Trends' global median.
- **MTTD** = mean(T1 - T0); always report the **median** too, one long APT case skews means.
- **MTTA** = T2 - T1; **MTTC** = T4 - T3; **MTTR** (recover) = T6 - T3.
- Detection source mix: % found internally vs by third party, customer or the attacker.
- Recurrence: incidents with the same root cause within 12 months.
- Post-incident actions closed on time (%).
- Readiness coverage: % critical assets with EDR, log sources onboarded, playbooks tested.

## Rules
- Define MTTR explicitly; "repair", "respond", "recover" and "resolve" are all in use.
- Only SEV3 and above go into time metrics; SEV4 noise distorts everything.
- Report distributions (box plot per quarter), not only averages.
- T0 moves earlier as the investigation finds older activity: recompute at case close.

## Gotchas
- Metrics that reward closing fast encourage under-scoping; pair speed with recurrence and
  re-open rate.
- Mixed time zones in tickets: store UTC, display local.

## Verify
Recalculate last quarter from raw case data with a script. If it differs from the published
dashboard, the dashboard definition is wrong.
