---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.executive-cost-report
name: executive-cost-report
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-reporting, executive-cost-report, cloud-spend-summary, unit-cost-trend, board-reporting]
level: practitioner
status: docs-checked
description: "Produce an executive cloud cost report: spend against budget and forecast, unit cost trends, commitment status, risks and decisions needed, in consistent terms."
sources: ["https://www.finops.org/framework/capabilities/reporting-analytics/", "https://www.finops.org/framework/capabilities/unit-economics/", "https://www.finops.org/framework/capabilities/benchmarking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Executive cost reporting

Executive reporting is one of the persona-specific reports the Framework's Reporting and Analytics capability calls
for: curated for the Leadership persona, with common terminology defined precisely.

## Suggested structure
1. **Headline**: spend against budget and forecast, with a one-sentence explanation of why.
2. **Trend**: spend over time with the forecast and budget lines.
3. **Unit economics**: unit cost trend for the products leadership cares about. The Framework says the most
   actionable view is usually a trend over time within a defined scope, and that rising cost is not always negative if
   proportionally more business value is delivered.
4. **Optimisation and rates**: effective savings rate, commitment utilisation, and key dates for commitment, marketplace,
   BYOL and SaaS renewals and expiries (the Framework lists reporting on these dates as a measure of success).
5. **Variances**: forecast-versus-budget variance against the agreed threshold, with an owner for each.
6. **Risks and decisions** for leadership.

## Rules
- Define terminology once and use it consistently; say whether figures are amortised and discount-adjusted.
- Keep one layout so readers can compare periods.
- Translate technology efficiency KPIs into a narrative for strategic decisions (Benchmarking page, Leadership).
- Where a decision carried a documented estimate, show projected against actual (Reporting and Analytics Walk stage).

## Steps
1. Automate the data feed so the report is produced from the same dataset the other personas see.
2. The FinOps team writes the narrative with input from the owners of the largest variances.
3. Review with Finance before distribution.

## Gotchas
- Dashboards with dozens of charts sent to executives go unread.
- Total cost shown without unit costs hides growth context.

## Verify
- [ ] Terms and cost basis are stated in the report.
- [ ] Decisions requested are recorded with an outcome.

## Checked
Confirmed on the FinOps Framework Reporting and Analytics page (persona-specific reporting, common terminology, Walk
projected-versus-actual view, renewal and expiry date reporting, forecasts with variance thresholds), the Unit
Economics page (trend over time within a scope, rising cost with proportionate value) and the KPIs and Benchmarking
page (translating KPIs into executive narratives). Removed: 13-month window, N-business-day delivery, FOCUS-and-BI
automation claim, the exact one-page limit, and the personas page (not read).
Method: docs-checked 2026-11-09 against finops.org Framework Reporting and Analytics, Unit Economics and KPIs and Benchmarking capability pages
