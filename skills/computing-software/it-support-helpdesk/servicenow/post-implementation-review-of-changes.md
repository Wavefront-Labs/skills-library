---
id: computing-software.it-support-helpdesk.servicenow.post-implementation-review-of-changes
name: post-implementation-review-of-changes
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, change-management, change-enablement, post-implementation-review, pir, change-success-rate, itil-4, failed-change]
level: practitioner
status: draft
description: "Run post-implementation reviews: which changes get a PIR, close codes, measuring change success and change-caused incidents, and feeding lessons back into models and templates."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://dora.dev/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# post-implementation-review-of-changes
Goal: every change is closed with an honest outcome, failed and
incident-causing changes are reviewed, and the lessons change how the next
change is done.

## Closing every change
In ServiceNow set **Close code** (Successful / Successful with issues /
Unsuccessful) and close notes stating what was verified. Do not let
implementers close "Successful" before the test plan ran.

## Which changes get a full PIR
- Unsuccessful or backed-out changes.
- Changes linked to an incident within ~72 hours (use the
  `caused_by` field on incident; see change-correlation skill).
- Emergency changes (was emergency justified?).
- First run of a new standard change template.
- Large/high-risk changes, even when successful.

## PIR agenda (30 minutes, blameless)
1. Objective met? Evidence.
2. Timeline: planned vs actual per step.
3. What surprised us (unknown dependency, wrong CI data, test gap).
4. User impact: incidents, calls to the desk, comms quality.
5. Was the risk assessment right? If a "low" change failed, the
   questionnaire needs tuning.
6. Actions with owners and dates: update template, add test, fix CMDB.

## Metrics to report monthly
- Change success rate (successful / closed).
- Change failure rate (changes causing incident or rollback) — the DORA
  metric; high performers stay well under 15%.
- Emergency change ratio and unauthorised changes detected.
- Standard change share (rising is good: more automation, less CAB).

## Feeding back
- Repeated success of a normal change type → propose it as a standard
  change (pre-approved template).
- Repeated failure → add mandatory test steps or raise its risk score.
- CMDB errors found → raise a CMDB correction task.

## Gotchas
- PIRs that become blame sessions stop people reporting "successful with
  issues"; keep them about the system.
- Actions that never close; track them as problem tasks or change tasks.

## Verify
All changes in the period have a close code; every failed change has a
PIR record with at least one completed action.
