---
id: computing-software.cloud-infrastructure-engineering.azure.compute-savings-plan-sizing-and-purchase
name: compute-savings-plan-sizing-and-purchase
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, savings-plan, savings-plan-purchase, hourly-commitment, benefit-recommendations, finops, reservations]
level: practitioner
status: docs-checked
description: "Size and buy an Azure compute savings plan: read benefit recommendations, choose hourly commitment, term and scope, layer with reservations and track utilisation."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/savings-plan/savings-plan-compute-overview", "https://learn.microsoft.com/azure/cost-management-billing/savings-plan/choose-commitment-amount", "https://learn.microsoft.com/azure/cost-management-billing/savings-plan/buy-savings-plan", "https://learn.microsoft.com/azure/cost-management-billing/savings-plan/decide-between-savings-plan-reservation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute savings plan sizing and purchase

**Goal:** commit to an hourly spend that will be fully used every hour, capturing discount
on compute that moves between regions, sizes and services.

## What it covers
Eligible compute includes Virtual Machines, Dedicated Host, App Service, Functions premium plan, Container Instances,
Container Apps and Spring Apps for Enterprise (see the overview page for the current list).
Each hour, eligible usage within the benefit scope is discounted starting with the usage that receives the highest
discount; the discounted cost is deducted from the hourly commitment, and usage beyond the commitment is billed at regular rates.

## Sizing
1. Clean up first: rightsize and delete idle (a commitment locks in waste otherwise).
2. Buy reservations for the stable, predictable core: when fully utilised, a reservation tied to a specific SKU or region can save more than a savings plan.
3. Cost Management **benefit recommendations** are generated per combination of term, benefit scope and lookback period (7, 30 or 60 days) by simulating costs under a plan.
4. Choose a commitment at or **below** the minimum steady hourly compute spend; an unused hourly commitment doesn't roll over.
5. Commitment is a billing-currency amount per hour.

## Purchase
Portal: Savings plans > Add. Choose the billing scope, the scope the benefit applies to, term and billing (up front
or monthly; the total cost is the same). You need the savings plan purchaser role within, or be an owner of, the
subscription you use. Auto-renew is available. Buying several plans over time (tranches) is a reasonable way to
avoid one large commitment.

## After purchase
- Savings plans can't be cancelled or refunded; you can trade in select reservations for a savings plan.
- The savings plan scope can be changed after purchase.
- Review utilisation in Cost Management; use amortized cost for allocation.

## Savings plan vs reservation quick rule
- Stable SKU+region for the term: reservation (can give greater savings when fully utilised).
- Variable usage across SKUs, regions or services: savings plan.

## Gotchas
- The savings figure in recommendations is a simulation that assumes usage matches the lookback.
- Shared scope across the billing account is usually best for utilisation, but chargeback needs amortized cost allocation.

## Verify
- [ ] Utilisation is checked after the first full month.
- [ ] Recommendation is re-checked before buying the next tranche.

## Checked

Method: docs-checked 2026-11-09 against the four cited pages, downloaded and searched for the relevant passages (hourly commitment application, eligible services, lookback periods, purchaser role, payment options, trade-in, no cancellation, decide-between guidance). Dropped unconfirmed claims: the ~65% discount, the worked euro figure, reservations-applied-first ordering, AKS/VMSS listing, specific utilisation targets, alert rules, Spot/dev-test exclusion and the PricingModel verification.
