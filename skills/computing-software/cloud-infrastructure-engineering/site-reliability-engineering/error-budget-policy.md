---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-policy
name: error-budget-policy
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, error-budget, error-budget-policy, slo-governance, feature-freeze, release-freeze, reliability-work, budget-attribution, budget-exhaustion, silver-bullets, exceptions, dependency-outages, planned-maintenance, escalation, product-engineering-agreement, slo-review, burn-down, launch-gating, change-management, sre-engagement-model]
level: advanced
status: docs-checked
description: "Write and run an error-budget policy: thresholds and actions, attributing budget spend, what counts, escalation, and keeping the policy enforced rather than ignored."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/sre-book/embracing-risk/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget policy — the agreement that makes SLOs change behaviour

**Goal:** a short written agreement, signed by product and engineering leadership, that says
in advance what happens at each level of budget consumption — so the reliability-vs-features
argument is settled before the incident, not during it.

The arithmetic of budgets and burn rates is in
`computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets`;
this skill is the governance document and how to run it.

## 1. Thresholds and actions
The Workbook's example policy: at or above SLO, releases proceed per the release policy. If the service has
exceeded its error budget for the preceding four-week window, all changes and releases halt other than P0 issues
or security fixes until the service is back within SLO. A single incident consuming more than 20% of the budget
over four weeks requires a postmortem with at least one P0 action item. Graduated thresholds before exhaustion
are your own addition: agree the numbers with the signatories.

Freezes end when the service is back within SLO, not by negotiation.

## 2. Define what counts
Write rules for:
- **Dependency outages:** the Workbook example lets the team keep doing feature work if the outage was caused by
  a service maintained by another team that has itself frozen releases, or by a company-wide networking problem;
  it requires reliability work if a postmortem reveals an opportunity to soften a hard dependency.
- **Out-of-scope users:** the example lets feature work continue if the budget was consumed by users out of
  scope for the SLO (load tests, penetration testers).
- **Miscategorized errors:** the example covers errors that consume budget with no user impact, and errors that
  fail to consume budget that should have been spent; correct the data and note it.

## 3. Attribute the spend
Weekly, list budget consumers: incidents (by postmortem), deploys (correlate SLI dips with
release markers), dependencies, background error rate. This tells you *which* reliability
work to do: if most spend is deploy-related, invest in canaries and rollback, not redundancy.

## 4. Escalation
- Disagreement on the budget calculation or the actions it defines → escalate to a named role; the Workbook
  example names the CTO.
- Business-critical launch during a freeze: if you allow exceptions, make each one require leadership approval
  and a written risk acceptance, and count and publish them.

## 5. Keep it alive
- Revisit on a set date (the Workbook example carries one): was the policy invoked? If budget never runs low, the SLO may be too loose; if it is always exhausted, the target or the investment is wrong.
- Publish a regular budget report to the audience that approved the policy.
- Keep the policy in the repo or wiki with version history.

## Template (one page)
Service and SLOs covered → thresholds and actions table → counting rules and exclusions →
attribution process → escalation path → silver-bullet allowance → signatories and review date.

## Gotchas
- A policy written by SRE alone and never signed by product is ignored at the first deadline.
- "Freeze all changes" blocks the fixes too — always exempt reliability, security and rollback changes.
- Budgets on very low-traffic services swing wildly; require a minimum event count before thresholds trigger actions.
- Teams game exclusions; every exclusion must be logged with a reason.
- Calendar windows reset to "healthy" despite ongoing problems; the Workbook example uses a preceding four-week window.

## Verify
- [ ] Policy has graduated thresholds with concrete actions, signed by product and engineering.
- [ ] Counting rules cover dependencies, maintenance, bad data and experiments.
- [ ] A weekly attribution of budget spend exists.
- [ ] Freeze exit is automatic on return to SLO.
- [ ] Exceptions are counted and published.
- [ ] Policy reviewed in the last quarter.

## Checked

2026-11-01. Confirmed against the Workbook page Example Error Budget Policy (four-week freeze rule with P0 and
security exemption, the 20% postmortem clause, the reliability-required and feature-work-allowed cases, CTO
escalation, revisit date) and the SRE Book chapter Embracing Risk. Removed: the graduated threshold table, the
30-day window, the 2 business day deadline, the 70% example and the unread Hidalgo citation.
Method: documentation only; no commands were run.
