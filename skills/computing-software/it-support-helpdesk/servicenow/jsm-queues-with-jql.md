---
id: computing-software.it-support-helpdesk.servicenow.jsm-queues-with-jql
name: jsm-queues-with-jql
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-queues, jql, queue-management, agent-queues, ticket-triage, atlassian]
level: practitioner
status: draft
description: "Build Jira Service Management agent queues with JQL: triage, my-open, SLA-at-risk and waiting-on-customer queues, ordering, columns, and no overlaps."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/create-and-edit-queues/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/use-jql-to-filter-slas/"
  - "https://support.atlassian.com/jira-software-cloud/docs/jql-functions/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-queues-with-jql

JSM queues are saved JQL filters scoped to one service project, with an order and a set
of columns. Good queues answer "what should I work on next" without the agent filtering.

## A working queue set
```text
Unassigned triage   resolution = EMPTY AND assignee = EMPTY ORDER BY "Time to first response" ASC
My open             resolution = EMPTY AND assignee = currentUser() ORDER BY "Time to resolution" ASC
SLA at risk         resolution = EMPTY AND "Time to resolution" < remaining("2h") ORDER BY "Time to resolution" ASC
Breached            resolution = EMPTY AND "Time to resolution" = breached() ORDER BY created ASC
Waiting on customer status = "Waiting for customer" ORDER BY updated ASC
Major incidents     issuetype = Incident AND priority = Highest AND resolution = EMPTY
Stale               resolution = EMPTY AND updated <= -5d ORDER BY updated ASC
```
SLA functions (`breached()`, `remaining()`, `elapsed()`, `paused()`, `running()`,
`withinCalendarHours()`) only work on SLA fields, quoted by their exact name.

## Steps (Queues > Manage queues > New queue)
1. Write the JQL in basic mode, switch to JQL for SLA functions and ORDER BY.
2. Choose columns: Key, Summary, Request type, Reporter, Status, SLA fields, Assignee,
   Updated. Remove columns agents never sort by.
3. Order queues in the sidebar to follow the work order (triage first); star the ones
   each team uses.
4. For multi-team projects, add a Team or component clause so each team sees its own
   triage queue, plus one shared queue for unrouted items.

## Design rules
- Every open ticket should land in exactly one triage-type queue; overlapping queues
  cause two agents to grab the same ticket and gaps let tickets rot.
- Sort by the SLA that matters, not created date, so the most at-risk item is on top.
- Review the Stale queue weekly; it is the queue-hygiene list.
- Sidebar counts can be approximate on very large projects; use a filter or dashboard
  gadget for exact totals.

## Gotchas
- `currentUser()` gives one queue per agent without duplicating queues.
- Queues are project-scoped; cross-project views need a Jira filter and dashboard.
- Status names in JQL are internal names, not the customer-facing portal names.
- Renaming an SLA breaks every JQL that quotes it; rename SLAs rarely.

## Verify
Pick ten random open tickets and confirm each appears in the queue the team expects; run
the triage JQL in issue search and check its count matches the sidebar.
