---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-spend-attribution
name: error-budget-spend-attribution
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [budget-attribution-report, budget-spend-attribution, error-budget, slo-report, incident-tagging]
level: practitioner
status: docs-checked
description: "Attribute error budget spend to incidents and causes using the share of budget each consumed, with outage tagging, per the Google SRE Workbook and SRE Book."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/error-budget-policy/", "https://sre.google/sre-book/tracking-outages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error budget spend attribution

Knowing how much budget is gone is less useful than knowing what spent it. The Workbook says error budgets can quantify events ("this outage consumed 30% of my quarterly error budget") and rank them ("the top three incidents this quarter, ordered by how much error budget they consumed"), and that you can scale an incident by the proportion of budget it consumed to find those worth closer investigation.

## Worked method from the Workbook
Count the errors an incident caused (from raw logs or estimated from historical traffic), divide by the period's budget. With a 97% SLO the Workbook's budget is 109,897 errors; a bad release causing 14,066 errors used 13% of it, and a 20-hour database failure estimated at 72,000 errors used 65%. Weight by frequency: two or three bad releases a year versus one server failure in five years means bad pushes cost about twice the budget of database failures, so fixing releases pays more. Treat these as the Workbook's example numbers, not benchmarks.

## Tagging incidents
The SRE Book's Outalator chapter describes free-form tags with colons as semantic separators (for example `cause:network`, `cause:network:switch`, `bug:76543`, `bogus` for false positives), suggested prefixes "cause" and "action", and says tags let teams see a service's pain points even without formal analysis. It also warns that "most incidents caused" can be an artefact of over-sensitive monitoring and says the incident count alone gives no indication of difficulty or severity.

For budget attribution, record per incident: the budget share consumed and a cause tag. Choose your own category list; the sources do not prescribe one.

## Checking the SLO against reality
The Workbook suggests comparing support tickets per day against budget lost per day; outliers (many tickets with no budget loss, or large loss with few tickets) warrant investigation and indicate SLO coverage gaps.

## Reporting
The Workbook recommends dashboards showing error budget and SLI trends, to spot a higher-than-usual burn rate. The SRE Book describes a report mode that expands important annotations for the weekly production review. A short per-service report can list: SLO, window, budget remaining, top incidents with budget share, exceptions used, and actions with owners.

## Gotchas
- Footnote in the Workbook: an error budget is an approximation of user satisfaction, so a four-hour outage and four one-hour outages cost the same.
- Tag at postmortem time; the Workbook and SRE Book give no tagging deadline, but late tagging relies on memory.

## Verify
- [ ] Every incident in the window has a budget share and a cause tag.
- [ ] The report is reviewed with actions assigned.

## Checked
Confirmed against the Workbook "Implementing SLOs" (decision making section, dashboards, ticket correlation, footnote 8), "Example Error Budget Policy" (20% outage clause, budget formula) and SRE Book "Tracking Outages" (tagging, analysis, report mode, footnote 85). Removed: the PromQL query and metric names (not in the sources), the ~20% background and ~10% unknown thresholds, and the fixed category list.
Method: docs-only read of cited pages, 2026-11-08
