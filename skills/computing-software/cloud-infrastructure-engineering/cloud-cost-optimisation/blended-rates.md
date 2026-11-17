---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.blended-rates
name: blended-rates
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-billing, blended-rates, unblended-cost, blended-cost, net-unblended, aws-billing-terms]
level: practitioner
status: draft
description: "Explain blended vs unblended vs net costs in AWS consolidated billing (and equivalents elsewhere), why blended rates mislead teams, and which to use for allocation."
sources: ["https://docs.aws.amazon.com/cur/latest/userguide/con-blended-rates.html", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-advanced.html", "https://focus.finops.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blended vs unblended rates

## Definitions (AWS)
- **Unblended cost**: usage x the actual rate charged for that line (on-demand, RI-discounted, tier
  price) in the account where usage happened.
- **Blended cost**: usage x the **blended rate** - an average across the consolidated billing
  family for a usage type (mixing on-demand, RI and tiered rates), redistributed to accounts.
- **Net unblended / net amortized**: after discounts such as EDP/private pricing credits.
- **Amortized**: upfront commitment fees spread over the term plus recurring fees, attributed to the
  usage that consumed them.

## Why blended misleads
An account that used no RIs still gets a "discounted" blended rate because of another account's
RIs; teams can't see their own efficiency, and optimisation in one account shifts cost to others.

## What to use
| Purpose | Metric |
|---|---|
| Matching the invoice | Unblended (cash basis) |
| Team showback/chargeback | Net amortized (commitments spread to consumers) |
| Optimisation analysis | Unblended for rates, amortized for effective cost |
| FOCUS | `BilledCost` (invoice), `EffectiveCost` (amortized, after discounts), `ListCost`, `ContractedCost` |

## Gotchas
- Mixing metrics across reports gives totals that don't reconcile; label every chart.
- Azure and Google have no "blended" concept but do have actual vs amortized views.

## Verify
- [ ] Every report states its cost metric; showback uses amortized net cost.
