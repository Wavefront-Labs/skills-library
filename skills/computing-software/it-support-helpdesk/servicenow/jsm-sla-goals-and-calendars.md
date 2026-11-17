---
id: computing-software.it-support-helpdesk.servicenow.jsm-sla-goals-and-calendars
name: jsm-sla-goals-and-calendars
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-sla, sla-goals, sla-calendars, time-to-first-response, time-to-resolution, sla, atlassian]
level: practitioner
status: draft
description: "Configure Jira Service Management SLAs: start/pause/stop conditions, goals per priority with JQL, working-hours calendars and holidays, and debugging odd SLA timers."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/create-service-level-agreements-slas/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/use-jql-to-filter-slas/"
  - "https://support.atlassian.com/jira-service-management-cloud/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-sla-goals-and-calendars

A JSM SLA is a timer field defined by **conditions** (when to start, pause, stop) and
**goals** (target time per JQL-matched set of tickets, each on a calendar).

## Conditions (Project settings > SLAs)
| SLA | Start | Pause on | Stop |
|---|---|---|---|
| Time to first response | Work item created | Status: Waiting for customer | Comment: for customers; Entered status: Resolved |
| Time to resolution | Work item created | Status: Waiting for customer, Pending vendor | Resolution set |
| Time to approve | Entered status: Waiting for approval | none | Left status |

Pausing on "waiting for customer" is fair only if customer replies move the ticket back
to an active status; otherwise the clock never restarts.

## Goals
Goals are evaluated top to bottom; the first JQL that matches wins, and the last row is
the catch-all ("All remaining work items").
```text
priority = Highest                 2h   24/7 calendar
priority = High                    8h   Business hours
issuetype = "Service request"      3d   Business hours
All remaining work items           5d   Business hours
```
A goal row with no target times tickets without counting breaches.

## Calendars
- One calendar per support region: time zone, working days and hours, holidays.
- Add public holidays every year; a holiday missing from the calendar turns into breaches.
- Assign the calendar per goal row, so a P1 runs 24/7 while the rest use office hours.

## Investigating "the SLA is wrong"
1. Hover the SLA on the ticket: it shows the cycle, paused time, goal and calendar used.
2. Check which goal row matched; if priority or request type changed after creation the
   goal is re-evaluated on the current values.
3. Check status history for a pause status that was never left.
4. After changing SLA config, existing open tickets recalculate; closed ones keep history
   unless you trigger recalculation.

## Gotchas
- SLA edits change historical reports; record the change date in the SLA description.
- Reopening starts a new cycle; reports use the latest cycle unless you query
  `completed()`.
- Keep SLA names stable; JQL quotes them by name.

## Verify
Create test tickets at each priority, pause and resume them, check remaining time against
the calendar by hand, and run `"Time to resolution" = breached()` to confirm reports.
