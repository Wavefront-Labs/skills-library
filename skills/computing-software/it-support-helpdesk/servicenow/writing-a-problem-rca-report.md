---
id: computing-software.it-support-helpdesk.servicenow.writing-a-problem-rca-report
name: writing-a-problem-rca-report
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, rca-report, problem-management, root-cause, contributing-factors, corrective-actions, known-error]
level: advanced
status: gated
description: "Write the root cause analysis report for a problem record: timeline, impact, root cause vs contributing factors, evidence, corrective actions with owners, and review sign-off."
sources:
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-problem-management"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/problem-management/concept/c_ProblemManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/problem-management/task/root-cause-analysis-problem.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# writing-a-problem-rca-report

The RCA report is what management, the customer and auditors read. It must stand alone,
be factual, and end in actions that will actually stop recurrence.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Structure
1. **Summary** (5 lines): what failed, when, who was affected, root cause in one sentence,
   status of the fix.
2. **Impact**: services/CIs, users or sites affected, duration (start of impact to full
   restoration, not ticket times), incidents linked (count + major incident number),
   SLA breaches, financial/regulatory impact if known.
3. **Timeline** in UTC (or one stated zone): detection, escalation, key decisions,
   workaround, restoration, fix. Source each line (monitoring alert, ticket, chat log).
4. **Root cause**: the specific technical or process condition that, if removed, prevents
   recurrence. Show the evidence (log lines, config diff, vendor confirmation).
5. **Contributing factors**: things that made it worse or slower (no alert, runbook
   missing, single engineer on call). Keep them separate from root cause.
6. **Why it was not caught earlier**: testing, monitoring, change review gaps.
7. **Corrective and preventive actions**: each with owner, due date, and the record that
   tracks it (change, problem task, story). "Be more careful" is not an action.
8. **Workaround/known error** status and KB article number.

## In ServiceNow
- Fill the problem's Cause notes and Fix notes fields concisely; attach the full report.
- Root cause analysis state / "Fix in progress" moves; mark Known error and publish the
  KB article when a workaround exists.
- Problem tasks (type Root cause analysis) for investigation threads, each with findings.
- Link the change that delivers the fix in the problem's related changes.

## Writing rules
- Blameless: describe actions and conditions, not individuals' failings.
- Distinguish fact, inference and unknown ("not determined; logs rotated").
- Numbers over adjectives: "1,240 users for 47 minutes", not "significant".
- Draft within 5 business days of a P1; publish after the problem review board.

## Gotchas
- Stopping at the proximate cause ("disk filled up") without asking why the disk filled
  and why nobody was alerted.
- Actions with no owner or date never close; track them in a report on problem tasks.

## Verify
A reader outside the team can answer: what happened, why, what prevents it next time, and
who owns each action by when.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
