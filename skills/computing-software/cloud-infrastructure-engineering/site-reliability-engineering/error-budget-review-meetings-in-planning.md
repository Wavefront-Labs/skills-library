---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-review-meetings-in-planning
name: error-budget-review-meetings-in-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [error-budget, planning, slo-review, sre, prioritisation]
level: practitioner
status: docs-checked
description: "Feed error budget status into planning using the Google SRE Workbook: weekly and quarterly summaries, budget dashboards, ranking incidents by budget used, and policy actions."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/error-budget-policy/", "https://sre.google/sre-book/embracing-risk/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget reviews in planning

**Goal:** error budget status changes what the team builds next, routinely, not only in crises.

## Cadence the Workbook describes
The Workbook found a four-week rolling window a good general-purpose interval, complemented "with weekly summaries for task prioritization and quarterly summarized reports for project planning". It says shorter windows allow quicker decisions and longer ones suit strategic decisions, such as choosing among large reliability projects. Meeting length and format are your choice.

## Inputs
- Error budget and SLI trend dashboards; the Workbook says these show whether you are consuming budget at a higher-than-usual rate.
- Incidents ranked by budget consumed ("these are the top three incidents this quarter, ordered by how much error budget they consumed").
- Support tickets versus budget loss; outliers (many tickets with no loss, or large loss with few tickets) deserve investigation.
- Postmortem action items. The example policy requires at least one P0 action item for any single incident that consumes more than 20% of the budget over four weeks, and a P0 item in quarterly planning for any outage class that consumes more than 20% over a quarter.

## Decisions it supports
- Prioritising projects: the Workbook compares automating rollbacks versus a replicated data store by estimated impact on the error budget, weighting by how often each failure occurs.
- Budget exhausted: the policy applies. Common policies per the Workbook include stopping feature launches until within SLO or devoting some or all engineering time to reliability bugs.
- Budget never used or SLO too tight for development: the SRE Book says the team may loosen the SLO (raising the budget) to increase innovation. The Workbook notes SLIs and SLOs should be refined over time and that uncovered outages or ticket spikes signal poor SLO coverage.

## Agenda suggestion (illustrative)
Status per SLO; top budget consumers and whether fixes are planned; decide proceed, rebalance or invoke policy; check the SLIs still reflect user experience; record decisions and owners.

## Verify
- [ ] Notes show a decision per SLO, and reliability backlog items link to top budget consumers.
- [ ] Quarterly planning references SLO data.

## Checked
Confirmed against the Workbook "Implementing SLOs" (time window, dashboards, decision making, SLO refinement), "Example Error Budget Policy" (outage policy) and the SRE Book "Embracing Risk" (loosening the SLO). Removed: 15-30 minute meeting length, green/amber/red thresholds, the 20% rebalancing example and the decision table, which the sources do not give.
Method: docs-only read of cited pages, 2026-11-08
