---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.estimate-accuracy
name: estimate-accuracy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, planning-and-estimating, estimate-accuracy, estimate-vs-actual, forecast-accuracy, cost-estimation, lessons-learned]
level: practitioner
status: docs-checked
description: "Review cost estimates against actuals: keep estimates as records with assumptions, revisit at go-live, report variance and feed lessons into the estimating method."
sources: ["https://www.finops.org/framework/capabilities/planning-estimating/", "https://www.finops.org/framework/capabilities/forecasting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimate vs actual review

The FinOps Forecasting page describes "shifting left" as treating a pre-decision estimate as a forecast with its own
accuracy record. At Crawl an estimate is produced once and never revisited; at Walk there is a defined revisit point,
such as go-live, to compare the original estimate with early actuals; at Run the variance is fed back into the estimating
method used at the next prioritisation gate.

## Capture at estimate time
Keep each approved estimate as a record rather than a one-off number. The Planning and Estimating page expects a common
estimating template at Walk, and a lightweight register with an explicit range and confidence level at Run. Record the
scope, the load and usage assumptions, the pricing assumptions (the page expects discount-adjusted, amortised usage
pricing), and shared and platform costs, so that a later variance can be explained.

## Review steps
1. **Choose revisit points** in advance (go-live is the example the framework gives) and when to review again.
2. **Pull actuals** for the same scope and the same cost basis as the estimate.
3. **Compute variance** as a percentage of the estimate, per line and in total. The framework prefers percentage
   variance against a threshold the organisation sets (Finance helps set estimating threshold variances).
4. **Explain the gap**: usage differed from the assumption, the price differed from the assumption, or the design changed.
5. **Feed back**: update the forecast and budget, and improve the estimating template and method. The practice reports
   estimate accuracy trends to stakeholders on a regular cadence at Walk.

## Gotchas
- Without recorded assumptions a variance cannot be split into usage and price effects.
- Check allocation and tagging before comparing, or actuals for the project will be incomplete.

## Verify
- [ ] Each approved estimate above the agreed threshold has a recorded revisit.
- [ ] The estimating template or method has changed as a result of reviews.

## Checked
Confirmed against the FinOps Planning and Estimating and Forecasting capability pages: shifting-left description of
estimates as forecasts with an accuracy record (revisit at go-live, feedback at Run), common template and register with
range and confidence, discount-adjusted amortised pricing, estimate-versus-actual variance within agreed thresholds set
with Finance, regular review of estimate accuracy trends, percentage variance as the primary measure. Removed: the 30 and
90 day review schedule, MAPE, the plus or minus 20 and 10 percent targets, the named missed cost lines (NAT, logs,
cross-AZ, support) and the advice not to punish misses.
Method: docs-checked 2026-11-09 against the FinOps Framework Planning and Estimating and Forecasting pages.
