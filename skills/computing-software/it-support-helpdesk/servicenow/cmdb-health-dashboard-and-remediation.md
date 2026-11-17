---
id: computing-software.it-support-helpdesk.servicenow.cmdb-health-dashboard-and-remediation
name: cmdb-health-dashboard-and-remediation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb, configuration-item, cmdb-health, completeness, correctness, compliance, stale-ci, itil-4]
level: practitioner
status: gated
description: "Keep the CMDB trustworthy using ServiceNow CMDB Health: completeness, correctness (duplicates, orphans, staleness) and compliance scores, with remediation tasks and owners."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cmdb-health-dashboard-and-remediation
Goal: agents trust what the CMDB says about a device or service, because
its quality is measured and someone fixes what drops.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## The three KPIs (CMDB Health dashboard)
- **Completeness**: required and recommended fields populated per class
  (e.g. computer needs serial, assigned_to, model, location).
- **Correctness**: duplicates, orphans (CIs missing a required
  relationship, e.g. an app server with no host), and staleness (not
  updated by any source within the staleness rule, default 60 days).
- **Compliance**: CIs match audit templates (certification filters,
  e.g. all production servers have support group set).

## Setting it up
1. Enable CMDB Health jobs (scheduled jobs for each metric); they are
   inactive in many instances.
2. Define **required/recommended fields** per class in CI Class Manager >
   Health; start with the classes support uses most (computer, server,
   business application, service).
3. Set **staleness rules** per class to match the discovery cadence
   (laptops imported daily: 14 days; servers weekly: 30 days).
4. Turn on **Remediation tasks** so failures create tasks assigned to the
   CI's managed-by group.

## Ownership
Every class has a data owner; every CI has a support group or managed-by
group. Without owners, health tasks pile up unassigned.

## Routine
- Weekly: review duplicates and stale CIs (see ci-reconciliation).
- Monthly: health score trend per class to the configuration manager;
  target, e.g. > 90% completeness for computers.
- On retirement: set `install_status` = Retired (not delete) so history and
  linked incidents remain.

## Agent-side signals of a sick CMDB
- Incidents logged against "Unknown" CI or a generic CI.
- Assigned user on CI wrong after a laptop swap.
- Impact analysis showing nothing for a known critical server.
Feed these back as CMDB correction tasks, not just ticket notes.

## Gotchas
- Chasing 100% on every field wastes effort; pick the fields that drive
  routing, impact and asset decisions.
- Deleting stale CIs breaks history; retire them.

## Verify
Health dashboard shows scores per class, remediation tasks are assigned
to real groups, and stale CI counts fall month on month.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
