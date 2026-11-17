---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.primary-and-secondary-on-call-roles
name: primary-and-secondary-on-call-roles
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, on-call, secondary-on-call, escalation, rotation-design, pager]
level: practitioner
status: docs-checked
description: "Define primary and secondary on-call responsibilities, escalation timing, handover between them, and when the secondary takes interrupts or backs up major incidents."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/workbook/on-call/", "https://response.pagerduty.com/oncall/being_oncall/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primary and secondary on-call

**Goal:** a page is always answered, and the person answering is not left alone during a big incident.

## Roles
| | Primary | Secondary |
|---|---|---|
| First notified | Yes | Only after the primary does not acknowledge, if used as fall-through |
| Duties | Acknowledge, triage, work toward resolution, escalate as needed | Depends on the team: fall-through for missed pages, or non-urgent production work while the primary takes pages |
| Expectation | Pager response time set per service by the team | Agreed by the team; write it down |

The SRE Book says teams split the duties differently: one team uses the secondary as a fall-through for pages the primary
misses; another has the primary handle only pages while the secondary handles all other non-urgent production activities.
It also notes that where a secondary rotation is not strictly needed, two related teams can serve as each other's
secondary with fall-through handling. Pick one model and write it down.

## Response times
The SRE Workbook on-call chapter ties response time to the service: its example table pairs a revenue-impacting network
outage with a 5 minute response (the SRE must stay within reach of a charged, authenticated laptop and coordinate heavily
with the secondary) and a stuck customer order batch system with 30 minutes (the SRE can run a short errand and the
secondary need not cover). Set your own numbers per alert class.

## Escalation
- PagerDuty's on-call guide recommends a 5 minute escalation timeout, staggered notification methods (push, then
  phone or SMS) and a backup on-call schedule as the next level; it suggests the whole team as the third level.
- PagerDuty's rule of thumb: never hesitate to escalate. The SRE Workbook stresses clear escalation paths for
  psychological safety.
- Major incident roles (incident commander, communications) come from your incident process, not from the secondary slot.

## Practices
- Handoff: the Workbook's example guidelines have the outgoing on-call send a handoff email and the incoming one read it
  at shift start. The secondary should know open incidents too.
- Follow-the-sun: the Workbook describes 24/7 teams split across two sites, so nobody is paged at night.
- Commute and errand coverage: the Workbook notes that with a strict pager response SLO, someone else must cover
  while the primary is out of reach.

## Verify
- [ ] The paging tool's escalation policy matches the written policy, including the timeout and who is next.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Being On-Call" (primary and secondary models, mutual secondary teams,
escalation paths), the SRE Workbook chapter "On-Call" (response-time table, handoff email, follow-the-sun, commute
coverage) and PagerDuty's "Being On-Call" page (5 minute escalation timeout, backup schedule, whole team as third level,
"Never hesitate to escalate"). Removed: the invented 5/10/20 minute ladder, the reimbursement and pager-load metric
advice, test-page cadence and the claim that the secondary is expected to act as communications lead.
Method: documentation only; no commands were run.
