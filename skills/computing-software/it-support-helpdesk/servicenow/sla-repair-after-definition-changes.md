---
id: computing-software.it-support-helpdesk.servicenow.sla-repair-after-definition-changes
name: sla-repair-after-definition-changes
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla-repair, task-sla, sla-definition, recalculation, service-level-management, reporting-accuracy]
level: advanced
status: gated
description: "Use ServiceNow SLA repair to recalculate task SLAs after changing definitions or schedules: scoping the run, audit dependency, side effects on notifications and reports."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/sla-repair.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/task/t_RepairSLAs.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/reference/r_SLAProperties.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sla-repair-after-definition-changes

Editing an SLA definition, schedule or pause condition only affects SLAs that attach
afterwards. Existing `task_sla` records keep the old maths. SLA repair replays task history
against current definitions and rebuilds them.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## When to run it
- Pause/stop condition fixed (e.g. Awaiting Vendor wrongly paused).
- Schedule or holiday calendar corrected (missing bank holiday).
- Definition created late and you need it on open tickets.
- Data fix that changed `opened_at` or priority history.

## Running it
1. Enable: property `com.snc.sla.repair.enabled` = true; role `sla_admin` (or admin).
2. Scope: from the SLA definition record use **Repair SLAs** (all tasks with that
   definition), or from a task list select records > **Repair SLAs**, or a filter on the
   repair page. Start narrow: one week, one group.
3. Preview the count; large runs go in batches and execute as a background job. Track
   progress in the SLA Repair log (`sla_repair_log`).
4. Repair deletes and recreates task SLAs for the scoped tasks using `sys_audit` history.

## Side effects
- Breach and warning notifications/flows can refire unless suppressed. Check
  `com.snc.sla.repair.audit` style options and disable SLA workflows/flows for the run
  window if your instance triggers emails from task SLA events.
- Historical reports and Performance Analytics scores computed earlier don't change until
  you re-collect the PA job for that period.
- Closed tickets are included if in scope; month-end SLA reports already sent to customers
  will no longer match. Document the run (date, scope, reason).

## Gotchas
- Tasks without audit history (imports, `setWorkflow(false)` updates, audit disabled on
  the table) repair inaccurately.
- Very old tickets: audit may be archived or rotated; repair them only if necessary.
- Don't repair during business hours on large tables; it is heavy on `sys_audit`.

## Verify
Pick 5 tasks across states, note business elapsed and breach before repair, run repair,
and confirm values now follow the new definition (check the timeline on the task SLA).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
