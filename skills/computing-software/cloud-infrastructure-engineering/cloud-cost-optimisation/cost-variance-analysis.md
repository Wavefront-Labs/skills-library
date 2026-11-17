---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-variance-analysis
name: cost-variance-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-reporting, cost-variance-analysis, month-over-month, price-volume-mix, variance-explanation, cost-drivers, waterfall-chart]
level: practitioner
status: docs-checked
description: "Explain why cloud cost changed against budget or forecast: split into usage and rate effects, attribute to owners, and report against agreed variance thresholds."
sources: ["https://www.finops.org/framework/capabilities/reporting-analytics/", "https://www.finops.org/framework/capabilities/budgeting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost trend and variance explanation

The FinOps Budgeting and Reporting and Analytics capabilities expect reporting on budgets against actuals against forecast,
with variance compared to agreed thresholds, and notifications when a threshold is exceeded or overspend is at risk.

## Procedure
1. **Set the comparison**: use the same cost metric and scope on both sides. Compare like periods, for example daily
   averages when months have different lengths.
2. **Compare against the agreed thresholds**: budget to forecast and budget to actual variance thresholds are set by the
   practice (the Budgeting page gives the maximum acceptable budget variance as 20 percent at Crawl, 15 percent at Walk
   and 12 percent at Run).
3. **Break the change down** for each large mover into a usage effect and a rate effect using quantity Q and effective
   unit price P for the two periods: usage effect = (Q2 - Q1) x P1, rate effect = (P2 - P1) x Q2. Whatever remains after
   splitting by service, SKU or region is mix. This is arithmetic, not a framework rule.
4. **Attribute** each mover to an owner, using the allocation data, and to a cause such as a launch, growth in demand, a
   commitment purchase or expiry, or a price change.
5. **Classify** each variance as planned (already in the forecast) or unplanned, and as one-off or run-rate. Feed run-rate
   changes into the next forecast.

## Gotchas
- Use the cost basis the Budgeting Strategy names; the Budgeting and Forecasting pages describe leveraging
  discount-adjusted, amortized usage data, so compare on that basis rather than mixing it with billed cost.

## Verify
- [ ] Every large variance has an owner and a stated cause.
- [ ] Run-rate changes appear in the next forecast.

## Checked
Confirmed against the FinOps Budgeting and Reporting and Analytics pages: budget versus actual versus forecast reporting,
variance thresholds and notifications, the 20, 15 and 12 percent maximum budget variance by maturity, and variance
analysis done manually at lower maturity. The usage and rate decomposition is arithmetic offered as a technique. Removed:
the 10 percent February versus March figure, the top 10 waterfall claim, the example commentary with dollar amounts and a
named purchase date, the 90 percent attribution target and the credits and restatement gotchas.
Method: docs-checked 2026-11-09 against the FinOps Framework Budgeting and Reporting and Analytics pages.
