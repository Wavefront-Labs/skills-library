---
id: computing-software.it-support-helpdesk.servicenow.cab-meetings-and-change-schedule-conflicts
name: cab-meetings-and-change-schedule-conflicts
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cab-meeting, change-schedule, change-advisory-board, change-collision, change-enablement]
level: practitioner
status: gated
description: "Prepare and run a CAB meeting that actually assesses changes, and use the change schedule to catch collisions with other changes, blackouts and maintenance windows."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/concept/change-schedule.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cab-meetings-and-change-schedule-conflicts

## Change schedule and collisions
- The **change schedule** (Change > Schedules, or Change Schedule app) shows planned
  changes on a timeline with blackout and maintenance schedules overlaid.
- ServiceNow's **conflict detection** checks a change against: other changes on the same
  CI (and optionally related CIs), blackout windows, maintenance windows the change falls
  outside, and the assigned-to's other changes. Run it (Conflicts tab > Refresh
  Conflicts) after setting CI and planned dates.
- Fill **Affected CIs** properly; conflict detection is only as good as the CI data.
- Desk relevance: before a planned change, add a KB note and a service status entry so
  agents can answer calls during the window.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Preparing for CAB
- Agenda built automatically from changes in **Assess** / **Authorize** state for the next
  period (CAB Workbench builds agendas and timeboxes items).
- Each change on the agenda must have: risk assessment completed, implementation plan,
  test evidence, backout plan, schedule, conflicts reviewed, communication plan.
- Send the agenda 24-48 hours before; changes missing information are deferred, not
  discussed.

## Running CAB
- Timebox per change (3-5 minutes for normal risk). Questions to ask: what is the impact
  if it fails, how do we know it worked, how long does backout take, who is on call.
- Decide: approve, approve with conditions, reject, defer. Record the decision and
  conditions on the change in the meeting.
- Review recent failed changes and emergency changes briefly; trend for repeat causes.
- Standard changes don't come to CAB; if one fails, review whether it should stay
  standard.

## Pitfalls
- CAB as a rubber stamp: approvals with no questions on high-risk changes.
- Changes dated in the same window on shared infrastructure (storage, network core)
  without a joint plan.

## Verify
Every change approved this week has no unresolved conflicts, and CAB minutes show
decisions and conditions recorded on the change records.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
