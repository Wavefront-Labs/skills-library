---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-policy-threshold-actions
name: error-budget-policy-threshold-actions
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [policy-thresholds, budget-freeze-actions, error-budget-policy, release-freeze, slo, sre]
level: practitioner
status: docs-checked
description: "Write the SLO-miss section of an error budget policy: the freeze trigger, what still ships, when reliability work is required, and when the freeze lifts."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget policy: threshold-to-action table

The Workbook's example policy is binary. At or above SLO, releases proceed per the release policy. If the
service has exceeded its error budget for the preceding four-week window, all changes and releases halt other than
P0 issues or security fixes until the service is back within its SLO. If you want graduated thresholds that act
before the budget is gone, that is your own design: write them as a table an on-call engineer can apply without
debate, with numbers agreed by the signatories.

## When reliability work is required (Workbook example)
The team must work on reliability if a code bug or procedural error caused the budget miss, if a postmortem
reveals an opportunity to soften a hard dependency, or if miscategorized errors failed to consume budget that
would have caused an SLO miss. The team may keep doing feature work if the outage was a company-wide networking
problem, was caused by another team's service that has itself frozen releases, was caused by users out of scope
for the SLO (load tests, penetration testers), or came from miscategorized errors that consumed budget with no user impact.

## Unfreeze rule
Lift the freeze when the service is back within SLO, not on a calendar date. Write it explicitly or the freeze will drift.

## Automating it
- Expose remaining budget as a metric (see `forming-the-error-budget`).
- Gate the deploy pipeline on it, and allow an audited override for P0 and security fixes.

## Policy document sections (Workbook)
Service overview, goals, non-goals, SLO miss policy, outage policy, escalation policy and background; the
example's header records status, author, reviewers, approvers and a revisit date. Its escalation policy sends
disagreements about the budget calculation or actions to the CTO.

## Gotchas
- "Freeze" must name what is still allowed, or teams freeze security patches too.
- Decide in advance which causes allow feature work to continue (see the Workbook list above) and log each use.

## Checked

2026-11-01. Confirmed against the Workbook page Example Error Budget Policy (binary SLO miss rule over four
weeks, P0 and security exemption, the reliability-required and feature-work-allowed lists, section names, header
fields, CTO escalation). Removed: the 50%/25%/0% table, the two-windows escalation, the 28d window, the shell gate
script and the sign-off roles (illustrative, not from the page).
Method: documentation only; no commands were run.

## Verify
- [ ] Policy approved by the people it binds, with a revisit date.
- [ ] Pipeline gate tested with a forced low value.
- [ ] Freeze and unfreeze events recorded with dates.
