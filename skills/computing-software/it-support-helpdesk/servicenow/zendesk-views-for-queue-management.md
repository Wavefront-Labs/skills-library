---
id: computing-software.it-support-helpdesk.servicenow.zendesk-views-for-queue-management
name: zendesk-views-for-queue-management
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-views, queue-management, ticket-views, play-mode, sla-sorting, triage]
level: practitioner
status: draft
description: "Design Zendesk views as work queues: unassigned triage, my tickets, SLA-sorted group views, pending and on-hold sweeps, shared vs personal views, Play mode."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408888828570-Creating-views-to-manage-ticket-workflow"
  - "https://support.zendesk.com/hc/en-us/articles/4408829459866-Defining-and-using-SLA-policies"
  - "https://support.zendesk.com/hc/en-us/articles/4408883104538-Using-views-to-manage-ticket-workflow"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-views-for-queue-management

Views are saved ticket filters with columns, grouping and sort. They are the agent's work
queue, so design them around the order work should be done.

## View set
| View | Conditions (all) | Sort |
|---|---|---|
| Unassigned - my groups | Status < Solved; Assignee is -; Group is (current user's groups) | Next SLA breach ascending |
| My open | Status < Solved; Assignee is (current user) | Next SLA breach |
| Group X - all open | Status < Solved; Group is X | Next SLA breach |
| Urgent/VIP | Status < Solved; Priority is Urgent OR tag contains vip | Requested |
| Pending sweep | Status is Pending; Hours since pending > 72 | Updated ascending |
| On-hold (vendor) | Status is On-hold | Updated ascending |
| Recently solved | Status is Solved; Hours since solved < 24 | Solved descending |

"Status less than Solved" includes New, Open, Pending, On-hold; use "Status is Open" for
actionable-now views.

## Rules
- Sort by **Next SLA breach** wherever SLA policies are on; that is what makes a view a
  priority queue.
- Group by priority or ticket form only if it helps; grouping breaks the global sort.
- Shared views for teams, personal views for individual habits; limit shared views so
  the list stays readable (Zendesk shows the first dozen or so in the sidebar).
- Use **Play mode** (Play button on a view) for triage teams so agents take the next
  ticket instead of cherry-picking.
- Pending and on-hold views exist so waiting tickets are actively chased, not forgotten.

## Gotchas
- View counts refresh periodically, not live; a count can lag a minute.
- Views can't use "Hours since" below 1 hour and time conditions are evaluated on refresh.
- Tickets in no view are invisible work: build an "Everything open, no group" safety view.
- Agents in multiple groups see "current user's groups" as all of them; check with a
  restricted test agent.

## Verify
Take a sample of open tickets and confirm each appears in exactly one triage view the
team watches; compare the Unassigned view count with an Explore query for the same filter.
