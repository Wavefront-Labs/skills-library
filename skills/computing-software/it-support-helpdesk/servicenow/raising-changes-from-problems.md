---
id: computing-software.it-support-helpdesk.servicenow.raising-changes-from-problems
name: raising-changes-from-problems
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-to-change, problem-management, change-request, fix-in-progress, error-control, known-error]
level: practitioner
status: gated
description: "Move a ServiceNow problem from root cause to deployed fix: creating the linked change, problem states during fix, closing linked incidents, and verifying the fix held."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/problem-management/concept/problem-management-states.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/problem-management/task/create-change-from-problem.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-problem-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raising-changes-from-problems

ITIL 4 calls this error control: the root cause is known, now the fix has to go through
change enablement and the linked incidents need closing properly.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Problem states (base Problem Management, newer state model)
New -> Assess -> Root Cause Analysis -> Fix in Progress -> Resolved -> Closed. A problem
can be marked Known error at any point a workaround or cause is documented.

## Raise the change
1. On the problem: **Create Change** (or Related links > Create normal/standard change).
   The change is linked through `rfc` on the problem and the problem appears in the
   change's related list.
2. Copy into the change: affected CIs, the root cause summary, and the fix design. Risk
   and impact come from the CI, not the urgency of the problem.
3. Pick the change model: standard if the fix matches a pre-approved template (e.g. patch
   deployment), normal otherwise. Don't use emergency just because the problem is old.
4. Set the problem to Fix in Progress; note the change number in work notes.

## While the change is pending
- Incidents recurring meanwhile: link them to the problem (Problem field on incident) and
  apply the known-error workaround. Put incidents on hold "Awaiting Problem" only if your
  desk agrees that pattern.
- Communicate the target date to the affected service owner.

## After implementation
1. Change closed successful: set the problem to Resolved with resolution code (Fix
   applied) and fix notes.
2. Linked incidents: base system offers resolving linked incidents when the problem is
   resolved (the "Resolve related incidents" behaviour). Check it is on, and that the
   resolution comment it posts makes sense to users.
3. Monitoring period (e.g. 2-4 weeks): watch for new incidents with the same symptom/CI.
   Only then Close the problem; retire or update the KB workaround article.

## Gotchas
- Failed or backed-out change: return the problem to Fix in Progress or RCA, don't close it.
- One problem may need several changes (config + vendor patch); link all, close the problem
  after the last.
- A change raised from a problem without a test plan is how fixes cause new incidents.

## Verify
Problem shows the linked change(s) closed successful, linked incidents resolved with a
clear comment, no recurrence in the monitoring window, KB updated.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
