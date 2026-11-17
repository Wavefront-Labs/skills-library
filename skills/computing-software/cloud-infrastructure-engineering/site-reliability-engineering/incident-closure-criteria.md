---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-closure-criteria
name: incident-closure-criteria
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, incident-management, incident-closure-criteria, resolution, mitigation, follow-up]
level: practitioner
status: draft
description: "Decide when an incident is mitigated, resolved and closed: objective exit criteria, monitoring period, handover of follow-ups, and the closing communication."
sources: ["https://response.pagerduty.com/after/post_incident_process/", "https://sre.google/workbook/incident-response/", "https://sre.google/sre-book/managing-incidents/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closing an incident

**Goal:** incidents end deliberately, with users safe and follow-up work owned, not when people drift away.

## Stages
| State | Meaning | Who decides |
|---|---|---|
| Mitigated | User impact stopped (rollback, failover, traffic shift), cause may be unknown | IC |
| Resolved | Systems stable, no ongoing impact, temporary mitigations understood | IC |
| Closed | Follow-ups captured, postmortem scheduled/owner assigned, comms complete | IC / incident owner |

## Exit criteria checklist (resolve)
- SLIs back within SLO for a monitoring period (for example 30-60 minutes for SEV1/2) with normal traffic.
- No alerts firing related to the incident; error budget burn back to normal.
- Temporary mitigations documented (who must undo the failover/flag/scale-up and when).
- Data integrity verified if data could be affected (reconciliation done or scheduled).
- Customer-facing status page updated to resolved.

## Closing steps
1. IC announces resolution in the incident and announcement channels with summary: impact window, user impact, mitigation, next steps.
2. Hand over remaining work: tickets with owners for cleanup and action items; postmortem owner and due date (SEV1/2 within 5 business days is common).
3. Release responders explicitly; record end time in the timeline.
4. Archive the channel after the postmortem is published.

## Pitfalls
- Declaring resolved too early, then reopening: prefer a monitoring period.
- Leaving mitigations in place forever (stuck failovers, disabled features).
- Forgetting comms to customers/support.

## Verify
- [ ] Incident record has mitigated/resolved/closed timestamps, owner-assigned follow-ups and a scheduled postmortem.
