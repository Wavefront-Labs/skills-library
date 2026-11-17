---
id: computing-software.it-support-helpdesk.servicenow.incident-on-hold-and-awaiting-caller
name: incident-on-hold-and-awaiting-caller
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-on-hold, on-hold-reason, awaiting-caller, auto-close, sla-pause, incident-management]
level: practitioner
status: gated
description: "Run ServiceNow On Hold correctly: hold reasons, SLA pause conditions, awaiting-caller reminders and auto-resolve, and resuming when the caller replies."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/incident-management/reference/r_IncidentStates.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/incident-management/concept/c_IncidentManagementProcess.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/c_ServiceLevelManagement.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# incident-on-hold-and-awaiting-caller

On Hold (incident state 3) exists so the clock stops while you genuinely cannot act.
Abused, it hides backlog and inflates SLA attainment.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Base hold reasons (`hold_reason`)
| Value | Reason | Typical SLA treatment |
|---|---|---|
| 1 | Awaiting Caller | Pause resolution SLA |
| 5 | Awaiting Change | Pause (change is scheduled) |
| 3 | Awaiting Problem | Pause (linked problem holds the fix) |
| 4 | Awaiting Vendor | Often *not* paused: the vendor is your supplier, the OLA/UC applies |

Pausing is defined by each SLA definition's pause condition (e.g.
`state=3^hold_reason=1`), not by the state itself. Read your definitions.

## Awaiting Caller procedure
1. Post a customer-visible comment saying exactly what you need ("reply with the error
   text and a photo of the screen") and when the ticket will auto-resolve.
2. Set State = On Hold, On hold reason = Awaiting Caller.
3. Base behaviour: when the caller comments (portal or email reply) a business rule moves
   the incident back to In Progress and clears the hold reason. Confirm it is active.
4. Reminders and auto-resolve: a scheduled flow, e.g. reminder after 2 business days,
   second after 4, then Resolved with close code "Caller unresponsive" after 5. Resolved
   still lets the caller reopen until auto-close (`glide.ui.autoclose.time`, default 7
   days from Resolved to Closed).

## Rules a team lead should enforce
- The hold reason must be true. Awaiting Vendor with no vendor case number in work notes
  is a red flag; Awaiting Change needs the change in the `rfc` field.
- Hold-age report: `state=3^sys_updated_on<javascript:gs.daysAgoStart(7)` grouped by
  assignment group.
- Never hold a P1/P2 to stop the SLA clock; escalate instead.

## Gotchas
- An agent's *work note* does not resume the ticket; a caller *comment* does.
- Caller out-of-office auto-replies count as comments and pull the ticket off hold. Add an
  inbound action condition that ignores mail with `Auto-Submitted: auto-replied`.
- Changing pause conditions doesn't recalculate existing task SLAs unless you run SLA
  repair.

## Verify
On a test incident: set Awaiting Caller, confirm the task SLA shows Paused, reply as the
caller by email, confirm the state returns to In Progress and the SLA resumes.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
