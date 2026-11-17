---
id: computing-software.it-support-helpdesk.servicenow.assignment-groups-and-workload-balancing
name: assignment-groups-and-workload-balancing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, assignment-group-membership, workload-balancing, assignment-groups, group-manager, backlog-dashboard]
level: practitioner
status: gated
description: "Administer assignment group membership and managers, then balance ticket workload across agents using backlog dashboards, caps and reassignment rules."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/users-and-groups/concept/c_Groups.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/advanced-work-assignment/concept/advanced-work-assignment.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-user-interface/page/use/dashboards/concept/c_Dashboards.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# assignment-groups-and-workload-balancing

## Group membership hygiene
- Groups (`sys_user_group`) have a **Manager**, members (`sys_user_grmember`), a type
  (set type `itil` or your assignment type so the group appears in assignment pickers),
  and a group email.
- Group managers can add/remove members without admin if the `group_manager` role and
  delegation are set up; do this so changes don't wait on platform admins.
- Leavers: membership removal belongs on the offboarding checklist; a terminated user
  still in a group keeps receiving assignments and notifications.
- Quarterly: export each group's members, send to the manager to confirm. Remove anyone
  inactive (`active=false`) automatically with a scheduled job.
- Give each group a description stating what it handles and its escalation path; the
  assignment lookup and agents both rely on it.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Seeing the workload
Build a dashboard (or Workspace list) per group:
- Open tickets by assignee (bar), including "unassigned".
- Ageing buckets by assignee (0-2, 3-5, 6-10, >10 days).
- Tickets assigned today per agent vs closed today.
- SLA at risk / breached by assignee.

## Balancing
- **Pull model**: agents take from the unassigned group queue oldest-first or by SLA
  remaining; a lead reassigns when someone holds more than the agreed cap (e.g. 15 open).
- **Push model**: Advanced Work Assignment routes work items to available agents by
  capacity (max items per channel) and presence. Set capacity per channel realistically.
- Account for non-ticket work: an agent on phones today should get fewer queue tickets.
- On absence: a lead redistributes the absent agent's tickets on day 1, not day 5.
  Filter `assigned_to.active=true` alone doesn't catch holidays; use the schedule.

## Pitfalls
- Counting tickets, not effort: one complex escalation can equal ten password resets.
- Leaving "unassigned" out of dashboards hides the real backlog.

## Verify
Every assignment group has a manager, accurate members and a description; no active
agent holds more than the cap, and unassigned tickets are under the agreed age.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
