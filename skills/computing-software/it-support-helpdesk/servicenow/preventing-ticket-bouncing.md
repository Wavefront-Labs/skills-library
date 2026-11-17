---
id: computing-software.it-support-helpdesk.servicenow.preventing-ticket-bouncing
name: preventing-ticket-bouncing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, queue-management, ticket-reassignment, reassignment-count, ticket-ping-pong, ownership, warm-transfer, resolver-group-agreements]
level: practitioner
status: draft
description: "Stop tickets ping-ponging between groups: reassignment_count reports, clear group scope definitions, warm handoffs, owner-stays-accountable rules, and bounce reviews."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# preventing-ticket-bouncing

Goal: a ticket reaches the team that fixes it within one or two hops, and
someone stays accountable to the user throughout.

## Measure
ServiceNow incident has **reassignment_count** (increments on assignment
group change). Report: incidents with reassignment_count ≥ 3, grouped by
category and by the groups involved; the audit history shows the path
(`sys_audit` / activity stream). The worst offenders are usually a handful
of category/group pairs.

## Causes and fixes
| Cause | Fix |
|---|---|
| Unclear group scope ("is this network or desktop?") | written scope per resolver group with examples; boundary cases decided once |
| Weak triage information | escalation package standard (symptoms, tests done, scope) — groups may reject only for missing package items |
| Wrong category → wrong routing rule | fix categorisation, routing table |
| "Not us" without evidence | reassigning group must note why and which group should own it — evidence-based |
| Ownership lost | service desk remains incident owner/communicator even when resolver group works it |

## Rules that work
- **No blind reassignment**: talk (chat/call) to the receiving group for
  anything beyond routine — warm handoff.
- **Max hops**: on the 3rd reassignment the ticket goes to the team leads of
  both groups to agree an owner within a set time.
- Receiving group can **ask** for missing info but keeps the ticket while
  waiting, rather than sending it back.
- Swarming for unclear issues (see swarming skill) instead of serial
  bouncing.

## Bounce review
Monthly: top 10 bounced tickets reviewed by the group leads; outcomes →
scope doc updates, routing rule changes, KB for triage.

## Gotchas
- Using reassignment_count as an agent performance metric pushes agents to
  hold tickets they can't fix; use it on processes, not people.
- Group-to-group "internal tickets" outside ITSM hide bouncing from data.

## Verify
Share of incidents with reassignment_count ≥ 3 falls month on month, and
users report a single point of contact in CSAT comments.
