---
id: computing-software.digital-forensics-incident-response.incident-response-process.maintaining-an-incident-decision-log
name: maintaining-an-incident-decision-log
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [decision-log, incident-documentation, incident-commander, dfir, case-tracking]
level: practitioner
status: draft
description: "Record incident decisions with time, options considered, rationale, approver and reversal conditions so actions can be defended and reviewed later."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/61/r2/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining an incident decision log

**Goal:** capture why the team did what it did. Regulators, insurers, courts and the post-incident
review will ask why a host was left online, why the ransom was or was not paid, why notification
was or was not made. Notes of what happened (the timeline) do not answer why.

## Entry format
| Field | Content |
|---|---|
| ID / time (UTC) | D-012, 2026-10-12 16:20Z |
| Decision | Delay containment of FIN-WS042 for 24 h to monitor C2 |
| Options considered | Isolate now; monitor 24 h; monitor indefinitely |
| Rationale | Need to identify second-stage hosts; no exfil observed; EDR blocking in place |
| Risks accepted | Attacker may move laterally; mitigated by alerting on host's accounts |
| Decided by / consulted | IC (A. Name); consulted Legal, CISO |
| Review / reversal trigger | Any new host contacted, or 2026-10-13 16:00Z |
| Outcome (filled later) | Isolated 2026-10-13 09:10Z after second host found |

## What belongs in it
- Containment timing and method; monitor-vs-contain choices.
- Scope boundaries ("not imaging the 300 kiosks; triage only").
- Engagement of third parties, law enforcement, insurers.
- Notification and disclosure decisions (with legal; consider privilege labelling).
- Ransom / extortion decisions; public statement approvals.
- Downgrades of severity and case closure.

## Practice
- The scribe writes it live; the IC reviews at each stand-up.
- Append-only; corrections are new entries referencing the old one.
- Keep it with legal guidance on privilege (often prepared at counsel's direction).

## Gotchas
- Writing speculation about blame or liability; stick to facts and reasoning.
- Decisions made in side calls never reach the log; IC must restate them in the command channel.

## Verify
Each major action in the timeline has a decision entry explaining it, with a named decider.
