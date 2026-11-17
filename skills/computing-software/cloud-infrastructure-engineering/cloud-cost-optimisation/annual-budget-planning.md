---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.annual-budget-planning
name: annual-budget-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, budgeting, annual-budget-planning, cloud-budget, fp-and-a, planning-cycle, forecasting]
level: practitioner
status: docs-checked
description: "Plan the annual cloud budget with finance: baseline run-rate, growth drivers, new initiatives, optimisation and commitment savings, price changes and holdback, per BU."
sources: ["https://www.finops.org/framework/capabilities/budgeting/", "https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/domains/quantify-business-value/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annual cloud budget planning

The annual budget is built bottom-up with teams and reconciled top-down with finance. Build it as a
bridge from current run-rate so each component can be challenged.

## The bridge
```text
next-year budget =
    current run-rate x 12           (discount-adjusted, amortised; one-offs removed)
  + organic growth                  (business driver growth x unit cost)
  + new initiatives                 (estimates with ramp curves)
  - planned decommissions / migrations out
  - optimisation savings            (identified, with owners and dates)
  - rate savings                    (new commitments, renegotiated discounts)
  +/- price and FX changes
  + holdback                        (size set by your holdback strategy)
```
The bridge is a working method, not a FinOps Foundation formula. The Foundation pages say budgets are
typically based on forecasts, that forecasts include rate optimisation and commitment discounts and use
discount-adjusted, amortised data, and that a holdback is money not tied to a purpose, for changes,
overages and forecasting errors. They give no percentage; dynamic or high-growth organisations may need more.

## Timeline (illustrative only; the Foundation does not prescribe months)
- Aug: FinOps publishes run-rate and drivers per BU; template sent to teams.
- Sep: teams submit growth, initiatives and savings; FinOps challenges unit costs.
- Oct: finance consolidates; top-down target set; gaps negotiated.
- Nov: final budget loaded into budgets hierarchy and native budgets; commitments plan aligned.
- Dec/Jan: monthly phasing confirmed (seasonality, launches).

## Steps
1. Produce the baseline: recent months of amortised cost (choose the window yourself), minus one-offs, by BU/team.
2. Collect drivers from product/finance (users, transactions, data growth); apply current unit
   costs.
3. Collect initiatives with estimates and launch months.
4. Agree savings commitments with owners; put them in the budget so they are tracked.
5. Phase monthly, not 1/12 per month: growth and launches make later months bigger.
6. Align vendor commitments to the budget: the Budgeting capability says to monitor budget vs actuals where
   exceeding budgets would affect commitments or vendor agreements.
7. Decide the cycle: annual is Crawl; shorter or rolling quarterly cycles with out-of-cycle adjustment
   rules suit dynamic spend (Walk and Run).

## Gotchas
- Flat "last year + 10%" budgets ignore launches and savings and fail by Q2.
- Savings counted in the budget but not owned never happen; budget overruns follow.
- Budgets in billed cost spike in purchase months; the Foundation points to discount-adjusted, amortised
  data for budgeting; track cash separately.
- Strongly favourable variance is also a problem: unused holdback could fund other work, so reclaim it.

## Verify
- [ ] Budget bridge per BU from run-rate to target is documented.
- [ ] Monthly phasing loaded and visible in budget-vs-actual reports.

## Checked
Date: 2026-11-08. Confirmed against the FinOps Budgeting and Forecasting capability pages (holdback, cycle length,
amortised data, commitments). The Quantify Business Value domain page was read but supports only the general
framing. Removed the invented 5-10 percent contingency and the EDP/MACC claim; the month-by-month timeline and the
bridge are marked as practice, not Foundation guidance.
Method: documentation only; no commands were run.
