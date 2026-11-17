---
id: computing-software.it-support-helpdesk.servicenow.ticket-lifecycle-and-queue-management
name: ticket-lifecycle-and-queue-management
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, jira-service-management, zendesk, itsm, itil, itil-4, incident-management, service-request, problem-management, change-management, ticket-lifecycle, ticket-states, on-hold, priority-matrix, impact-urgency, sla, response-time, resolution-time, assignment-group, queue-triage, list-filter, encoded-query, work-notes, additional-comments, knowledge-base, kb-article, major-incident, service-desk]
level: practitioner
status: draft
description: "Run tickets in ServiceNow, Jira Service Management or Zendesk: ITIL record types, states and hold reasons, impact x urgency priority, SLA timers, queue triage, list URLs, KB and major incidents."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ticket lifecycle and queue management (ServiceNow and other ITSM tools)

**Goal:** every ticket has the right record type, an honest priority, the right queue and
a running (or legitimately paused) SLA, and ends linked to its fix and knowledge.
Examples use ServiceNow, with Jira Service Management (JSM) and Zendesk equivalents. UI
labels move between releases (Next Experience vs UI16, JSM cloud vs Data Center): treat
menu names as approximate.

## 1. Pick the right record type (ITIL 4)
- **Incident** — something that worked is broken or degraded. Goal: restore service fast.
- **Service request** — a standard, pre-approved ask (new laptop, access, software).
  Use the catalogue item, not an incident.
- **Problem** — the underlying cause of one or more incidents. Goal: root cause, then a
  *known error* with workaround until fixed.
- **Change** — any modification to production (standard, normal, emergency). Urgent fixes
  still go through (emergency) change.

## 2. States and when to use them
ServiceNow incident defaults: **New → In Progress → On Hold → Resolved → Closed**
(plus **Canceled**). Rules that keep queues honest:
- **On Hold** always needs a reason: *Awaiting Caller, Awaiting Change, Awaiting
  Problem, Awaiting Vendor*. Whether a reason pauses the SLA depends on the SLA
  definition's pause condition — check it rather than assuming.
- **Resolved** means you believe it's fixed; the caller can reopen. Instances usually
  auto-close Resolved tickets after a configured number of days (commonly 7, but it is
  a system setting, so confirm yours).
JSM uses workflow statuses (e.g. *Waiting for support / Waiting for customer*);
Zendesk uses *New, Open, Pending, On-hold, Solved, Closed*.

## 3. Priority = impact x urgency
Impact = breadth (1 org-wide, 2 team/site, 3 one user); urgency = how fast it hurts
(1 now, 2 soon, 3 can wait). ServiceNow default lookup:

| | Urgency 1 | Urgency 2 | Urgency 3 |
|---|---|---|---|
| **Impact 1** | P1 Critical | P2 High | P3 Moderate |
| **Impact 2** | P2 High | P3 Moderate | P4 Low |
| **Impact 3** | P3 Moderate | P4 Low | P5 Planning |

Set impact and urgency and let priority calculate; VIP is a flag, not a priority.

## 4. SLA timers
Most contracts carry two clocks: **response** (first meaningful human touch) and
**resolution** (service restored). An auto-acknowledgement is not a response.
Watch the 50%/75% warnings rather than discovering breaches; pause only when genuinely
waiting on the caller or a third party.

## 5. Queue triage cadence
- Work from **assignment group** queues, not personal email. A sensible default: triage
  the unassigned queue at least hourly, P1/P2 immediately on arrival.
- Triage = validate type and category, set impact/urgency, assign group and person,
  first response to caller.
- Daily: review old On Hold, reopened tickets and SLA warnings.
- Wrong group? Reassign with a work note saying why; a reassignment count above 2-3
  signals ping-pong.

## 6. ServiceNow list and URL tricks
- In the filter navigator: `incident.list` opens the list, `incident.LIST` opens it in a
  new tab, `incident.form` / `incident.FORM` opens a new record.
- Direct URLs: `incident_list.do?sysparm_query=active=true^assignment_group=javascript:getMyGroups()`
  and `incident.do?sys_id=<SYS_ID>`.
- Build a filter, then right-click the breadcrumb (or use the filter's copy-query
  option) to grab the encoded query for bookmarks and reports.
- Right-click a cell › *Show Matching* / *Filter Out* for fast pivots.

## 7. The notes gotcha
In ServiceNow **Additional comments are customer-visible** and normally trigger an email
to the caller; **Work notes are internal**. JSM: *Reply to customer* vs *Add internal
note*; Zendesk: *Public reply* vs *Internal note*. Check which field you typed in before
saving; internal speculation posted publicly is a classic helpdesk embarrassment.

## 8. Link problem and knowledge
- Several incidents with the same cause → raise or link a **Problem** and relate the
  incidents; child incidents can follow the parent.
- Close with a KB link. A good article: title in the user's words, symptoms (exact error
  text), environment, cause, resolution steps, workaround, keywords. Write one whenever
  you solve something undocumented (KCS-style).

## 9. Major incidents
P1 with wide impact → declare a major incident per your process: one major incident
manager, a bridge call, a parent incident with children attached, internal and
customer updates on a fixed cadence (e.g. every 30 minutes, even if "no change"), and a
post-incident review feeding a Problem. Communication detail: see
computing-software.it-support-helpdesk.user-support-communication.ticket-communication-and-escalation.

## Gotchas
- Reopened tickets often keep the original SLA breach; check how your instance counts them.

## Verify
- [ ] Record type matches the definitions in section 1.
- [ ] Impact and urgency are set; priority derived, not overridden.
- [ ] Every On Hold ticket has a reason and a next-contact date.
- [ ] Customer-facing text is in comments, internal detail in work notes.
- [ ] Resolved tickets link a KB article or problem where one applies.
