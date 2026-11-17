---
id: computing-software.it-support-helpdesk.servicenow.assignment-rules-and-data-lookup-routing
name: assignment-rules-and-data-lookup-routing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, queue-management, assignment-group, assignment-rules, assignment-data-lookup, ci-support-group, predictive-intelligence, auto-routing]
level: practitioner
status: gated
description: "Route tickets automatically in ServiceNow: assignment rules vs data lookup rules vs CI support groups, rule ordering, a default catch-all queue, and testing routing changes."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://developer.servicenow.com/dev.do"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# assignment-rules-and-data-lookup-routing

Goal: tickets land in the right group's queue without a dispatcher reading
every one, and nothing falls into a void.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Routing options (ServiceNow)
| Mechanism | Best for | Notes |
|---|---|---|
| **CI / service support group** | anything with a CI or service offering | set "Support group" on the CI/offering; incident flows pick it up — keeps routing data with the service |
| **Data lookup rules** (Assignment Data Lookup) | matrix routing: category × subcategory × location → group | table-driven, maintained by process owners, no code |
| **Assignment rules** (sysrule_assignment) | conditions on any field, ordered | run only when assignment group is empty; lowest order wins |
| Flow/business rule logic | complex cases | harder to maintain, last resort |
| **Predictive Intelligence** (classification) | learning from history | needs clean, large training data; review confidence |
Pick one primary mechanism per table — mixing four makes "why did it go
there?" unanswerable.

## Design
- Default for portal/email tickets: **Service Desk L1** triage group, not
  resolver groups — unless the category is unambiguous (e.g. "Password
  reset" automation).
- Each rule has an owner and a reason; maintain as a table, not tribal
  knowledge.
- Location-based routing for desk-side teams (site field from caller's
  location).
- Catch-all rule at the highest order number → triage group, so nothing
  stays unassigned.

## Testing a change
1. In a sub-production instance, create test incidents covering each rule
   combination (or use the ATF — Automated Test Framework).
2. Check "unassigned" report daily for a week after go-live.
3. Watch reassignment counts for the affected categories (routing errors
   show as quick reassignments).

## Gotchas
- Assignment rules don't fire if a template/flow already set a group.
- Category changes by agents don't re-route unless rules are designed to
  (on update); otherwise reassign manually.
- Inactive groups or groups with no members silently swallow tickets —
  report on open tickets assigned to groups with zero active members.

## Verify
Unassigned active incidents = 0 at shift checks; first-assignment accuracy
(not reassigned within 1 hour) above target for routed categories.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
