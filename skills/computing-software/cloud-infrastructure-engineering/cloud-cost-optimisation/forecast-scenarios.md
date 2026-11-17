---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.forecast-scenarios
name: forecast-scenarios
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-forecasting, forecast-scenarios, commitment-expiry, price-changes, what-if-analysis, scenario-planning, discount-modelling]
level: advanced
status: docs-checked
description: "Model rate-side changes in forecasts: commitment purchases and expiries, negotiated discounts and renewals as explicit scenarios on top of usage forecasts."
sources: ["https://www.finops.org/framework/capabilities/forecasting/", "https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forecasting commitment and rate changes

A usage forecast supplies volume; finance also needs the rate side. The FinOps Forecasting maturity model expects the
forecast to include rate optimisation and commitment-based discounts, and to be tracked against discount-adjusted,
amortised usage.

## Rate-side events to model explicitly
- **Commitment purchases** (Reserved Instances, Committed Use Discounts, Savings Plans): they change the effective rate
  for covered usage. Under-used commitments lower the effective savings rate, as does usage not covered by discounts.
- **Commitment expiries**: the Rate Optimization page lists notifying stakeholders about expiring commitments with enough
  time to plan a new purchase, and spreading purchases over the year so that some share is always expiring. A forecast
  should show what happens to covered usage if an expiring commitment is not renewed.
- **Negotiated discounts**: commitment analysis is done in the context of the negotiated enterprise discounts the provider
  offers in return for overall spend, so renewals and tier changes belong in the scenarios.
- **Prepayment**: Finance models prepayment, purchase levels and cost centre budget impact; keep cash (billed) and
  amortised views separate.

## Steps
1. Keep an inventory of commitments: identifier, type, scope, amount, term, start and end, renewal plan.
2. Build the forecast as usage at an undiscounted rate, then apply discount layers by date.
3. Define scenarios such as renew all, renew part, or do not renew; show finance the effect on both views.
4. Agree the forecast variance thresholds and review variance against them.

## Verify
- [ ] The next twelve months of commitment expiries are listed with their forecast effect.
- [ ] The forecast shows both the cash and the amortised view for prepaid commitments.

## Checked
Confirmed against the FinOps Forecasting and Rate Optimization pages: forecast inclusive of rate optimisation and
commitment discounts, discount-adjusted amortised usage, expiring commitment notification, spreading purchases over the
year, negotiated enterprise discount context, Finance modelling prepayment and cost centre impact, under-utilisation
lowering Effective Savings Rate. Removed: the plus 20 to 40 percent expiry jump, the cloud provider price-change example
(IPv4 charge dated February 2024), credits ending, currency moves, the 80 percent renewal scenario and the named
discount tier example.
Method: docs-checked 2026-11-09 against the FinOps Framework Forecasting and Rate Optimization pages.
