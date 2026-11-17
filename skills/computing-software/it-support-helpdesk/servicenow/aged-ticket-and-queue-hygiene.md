---
id: computing-software.it-support-helpdesk.servicenow.aged-ticket-and-queue-hygiene
name: aged-ticket-and-queue-hygiene
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, queue-management, aged-tickets, backlog-management, queue-hygiene, stale-tickets, pending-reasons, backlog-review, ageing-report]
level: practitioner
status: draft
description: "Keep queues healthy: ageing reports, a weekly backlog review, pending-state discipline, stale-ticket rules, and closing or escalating tickets that have been sitting for weeks."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# aged-ticket-and-queue-hygiene

Goal: the backlog is small, current and honest — no ticket has silently
waited a month.

## Ageing report
ServiceNow list/report on active incidents and SCTASKs grouped by
assignment group with age buckets (`opened_at` relative): 0–2 days, 3–7,
8–14, 15–30, 30+. Also "last updated more than 5 days ago"
(`sys_updated_on`) — idle tickets matter more than old ones.
Encoded query example for idle tickets in your group:
`active=true^assignment_group=javascript:getMyGroups()^sys_updated_on<javascript:gs.daysAgoStart(5)`

## Weekly backlog review (30 minutes, team lead + agents)
For each ticket in the oldest buckets / idle list:
- Still valid? Close with reason if user no longer needs it (with their
  confirmation or after the documented reminder process).
- Who owns the next action, and by when? Write it in work notes.
- Blocked on another team/vendor? Escalate with a specific ask.
- Should it be a problem record or a project/change rather than an
  incident?

## Pending-state discipline
On hold / Pending must carry a **reason** (Awaiting caller, Awaiting
vendor, Awaiting change) and a follow-up date. Pending pauses SLAs — abuse
hides delays. Rules:
- Awaiting caller: 3 reminders over ~7 days, then resolve with a note
  (automate with a scheduled flow).
- Awaiting vendor: vendor case number in the ticket; check weekly.
- Awaiting change: link the change; resolves when the change completes.

## Preventing backlog
- Daily triage of new and unassigned tickets.
- Don't accept "parking" tickets for future work — make them requests or
  projects.
- Capacity: backlog growing steadily = demand > capacity; report it with
  data rather than absorbing it.

## Gotchas
- Mass-closing old tickets to make numbers look good destroys trust; contact
  the users.
- Agents with 40 open tickets lose track — set WIP limits per agent.

## Verify
Nothing over 30 days without a documented reason and owner; idle-5-days
count trending down; backlog size stable or falling week over week.
