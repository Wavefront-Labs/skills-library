---
id: computing-software.it-support-helpdesk.servicenow.retroactive-sla-start-and-pause
name: retroactive-sla-start-and-pause
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, retroactive-sla, sla-definition, retroactive-pause, priority-change, task-sla, service-level-management]
level: advanced
status: gated
description: "Configure ServiceNow retroactive start and retroactive pause on SLA definitions so priority changes measure from ticket creation, and know when they distort results."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/c_SLADefinitions.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/retroactive-start.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/c_SLAConditionRules.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# retroactive-sla-start-and-pause

Typical case: a ticket is logged as P3, upgraded to P1 two hours later. The P3 SLA cancels
and the P1 SLA attaches. Without retroactive start, the P1 clock starts at the upgrade
time and the ticket looks great; with it, the P1 clock starts at creation and may already
be breached.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Settings on the SLA definition (`contract_sla`)
- **Retroactive start**: when the SLA attaches, set its start to a date field on the task
  rather than "now". **Set start to** usually `opened_at` (or `sys_created_on`).
- **Retroactive pause** (only with retroactive start): replay the task's history and
  subtract time the task *would* have been paused under this definition's pause
  condition (e.g. time spent On Hold - Awaiting Caller before the upgrade).
- Start/cancel conditions: P1 definition `priority=1` start, cancel when `priority!=1`.

## Choosing
| Situation | Retroactive start? |
|---|---|
| Priority changes because the initial triage was wrong | Yes: the customer's impact began at creation |
| Priority changes because the situation worsened later | Debatable; many desks still say yes to avoid gaming |
| Response SLA (assignment/first touch) | Usually yes, from `opened_at` |
| Reassignment-based OLAs (group SLAs) | No: measure from assignment to the group |

Agree it with the service owner and write it into the SLA document; reports change.

## Effects to expect
- Upgraded tickets may attach already breached (`has_breached=true` on creation). That
  fires breach notifications immediately; tell the on-call team this is expected.
- Retroactive pause needs audit history; tickets imported without `sys_audit` history
  calculate as never paused.
- Downgrades: the higher SLA cancels (stage Cancelled) and the lower one attaches with its
  own retroactive start; cancelled SLAs are excluded from attainment by default.

## Gotchas
- Retroactive pause replays using the *current* pause condition, so a later definition
  change alters results only for SLAs attached after the change (or after SLA repair).
- Schedules apply to the retroactive window too (a ticket opened Friday 17:30 on an 8x5
  schedule starts counting Monday 08:00).

## Verify
On a sub-production instance: create P3, hold for 30 min, upgrade to P1; the new task SLA
start equals `opened_at` and business elapsed time excludes the 30-minute hold.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
