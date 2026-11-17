---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budget-setting
name: budget-setting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-budgeting, budget-setting, team-budgets, annual-planning, budget-allocation, growth-allowance, efficiency-targets]
level: practitioner
status: docs-checked
description: "Set cloud budgets per team from forecasts: budget owners, holdback, budgeting cycle, variance thresholds and out-of-cycle exception handling per the FinOps Framework."
sources: ["https://www.finops.org/framework/capabilities/budgeting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting team cloud budgets

The FinOps Framework separates the two documents. Forecasting is a promise by engineering and
product owners to deliver some value for some spend. A budget is the organisation's commitment to
fund those owners at a level, and it should give healthy constraints to work within.

## Steps
1. Create the budgeting strategy: the holdback strategy (levels, percentages, factors) and the
   budgeting cycle (annual, quarterly or other).
2. Base each system's or application's budget on the forecasts from its owners, and decide how
   budgets will in turn inform forecasting.
3. Allocate budgets to budget owners responsible for a defined scope of work; there may be
   several levels of owner. Finance primarily drives budgeting, with the FinOps team
   collaborating on the strategy.
4. Align budgets to the allocation constructs used for reporting and chargeback, so costs land
   on the budget cost centres.
5. Give each budget owner a holdback: money not assigned to a specific purpose, for changes,
   overages and forecasting errors. The page expects holdback to shrink as workloads stabilise,
   and larger holdback or more owner layers for dynamic, high-growth usage.
6. Set acceptable variance thresholds for budget to forecast and budget to actual, and define
   how budgets are altered out of cycle.
7. Write down the resolution path when spend is heading over budget. The page's example:
   threshold report warns engineering, engineering and product investigate and optimise, then
   the budget owner requests holdback, then a higher-level owner or finance, then leadership
   approves or denies the adjustment.

## Notes from the Framework
- Unfavorable to budget means more expense than planned and needs action when detected.
  Strongly favorable is also not ideal, because unused holdback could fund other work.
- Shorter budgeting cycles let organisations adjust more often and release unused holdback.
- Budgets may combine with other resource budgets such as labour, licence cost or
  sustainability goals; public-sector funding rules can add restrictions.
- At higher maturity, a response (alert, approval gate or throttle) is defined before a budget
  line is exceeded, with an owner and response time per threshold.

## Verify
- [ ] Each budget owner has a documented scope, a budget and holdback rules.
- [ ] Variance thresholds and the out-of-cycle process are written down and used.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Budgeting capability page (read through the definition, maturity and KPI sections). The book citation was not available and was dropped. Removed unconfirmed: efficiency-target examples, the flexible-budget formula, specific 5% and 10% overrun thresholds, the AWS/Azure/GCP budget tooling advice, and the gotchas on commitments and reorgs.
