---
id: computing-software.it-support-helpdesk.servicenow.sla-definitions-start-pause-stop
name: sla-definitions-start-pause-stop
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla, service-level-management, sla-definition, task-sla, start-condition, pause-condition, stop-condition, retroactive-start, response-sla, resolution-sla, response-resolution-sla]
level: advanced
status: gated
description: "Configure ServiceNow SLA definitions correctly: response vs resolution SLAs, start/pause/stop/reset conditions, retroactive start on priority change, and reading task SLA records."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://developer.servicenow.com/dev.do"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sla-definitions-start-pause-stop

Goal: SLA timers measure what the agreement actually promises, so breach
reports are trusted.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Model
- **SLA definition** (contract_sla): table, type (SLA/OLA/UC), duration,
  schedule, and conditions. Each matching ticket gets a **Task SLA**
  (task_sla) record with stage (In progress, Paused, Achieved, Breached,
  Cancelled), elapsed and business elapsed time/percentage.
- Typical set per priority: **Response** (P1 15 min, P2 1 h…) and
  **Resolution** (P1 4 h, P2 8 business hours…).

## Conditions
| Condition | Example (resolution SLA) |
|---|---|
| Start | Priority = 2 AND Active = true |
| Pause | State = On Hold AND On hold reason IN (Awaiting caller, Awaiting vendor) |
| Stop | State IN (Resolved, Closed) |
| Reset (optional) | Priority changes (cancels and restarts the SLA) |
| Cancel | Priority no longer 2 (when not using reset) |
Response SLA usually stops on first assignment-to-person or first
customer-visible comment — define which in the agreement.

## Priority changes
Use **retroactive start** ("Set start to: Created") on priority SLAs so
when a P3 is upgraded to P2, the P2 SLA starts from when the ticket was
opened — otherwise upgrades get a fresh clock and breaches hide. Decide
retroactive pause behaviour too.

## Testing
Create test incidents and walk them through states; check task_sla
elapsed/pause times. The **SLA timeline** UI action on the task SLA shows
when it started/paused/stopped and why — first stop when a user disputes a
breach.

## Gotchas
- Pause conditions that include generic "On Hold" allow agents to stop the
  clock on anything — require specific reasons.
- Schedules must match support hours (see business-hours schedules skill).
- Changing a definition affects only new task SLAs unless repaired via the
  SLA repair tool — plan changes at period boundaries.
- Too many overlapping definitions attach multiple SLAs to one ticket;
  check conditions are mutually exclusive.

## Verify
Sample tickets: one task SLA per type, correct duration/schedule, pauses
only for allowed reasons, breaches correspond to real delays.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
