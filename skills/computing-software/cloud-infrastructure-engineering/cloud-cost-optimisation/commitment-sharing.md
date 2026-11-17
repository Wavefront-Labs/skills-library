---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-sharing
name: commitment-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimisation, commitment-sharing, centralised-commitments, ri-sharing, discount-sharing, shared-scope, savings-allocation, rate-optimisation-ownership, commitment-discount-allocation]
level: practitioner
status: docs-checked
description: "Decide who buys commitments and how benefits flow: why the FinOps Framework centralises purchasing, who is involved, and agreeing how discounts are allocated."
sources: ["https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Centralised commitment management

## Default: centralise
The Rate Optimization capability page says the central FinOps team should be the primary driver
coordinating purchases of spend-based and resource-based discounts. Reasons it gives: these
discounts are complex with many parameters, can be bought in ways that cover resources across the
whole estate, and interact with other optimisation (usage optimisation, licensing and SaaS use,
architecture changes, sustainability). The FinOps Principles page says rate, commitment and
discount optimisation are best centralised for economies of scale so engineers can stay focused
on usage. The central team may not make every purchase, but should track all of them.

## Who does what
- FinOps: manages central rate optimisation, including discount purchasing, and supports
  Procurement with past and planned usage.
- Finance: helps set guidelines for the strategy, reporting and allocation of discounts, and
  models prepayment and purchase levels.
- Engineering: shares current and planned resource use and incorporates discounted cost data in
  reporting where the strategy says to.
- Product: uses the pricing metrics the strategy specifies, with or without discounts, when
  budgeting and analysing products.

## Allocating benefits
1. Decide in the rate optimisation strategy whether teams see discounted cost data and how
   discounts are allocated; the Framework leaves the choice to the organisation.
2. Publish the decision so Product and Engineering use the same cost view.
3. Remember that a commitment is like a coupon, not a resource: if no matching resource is
   running you still pay, so unused commitment needs an agreed owner.

## Verify
- [ ] Purchasing authority and the discount allocation method are documented.
- [ ] Teams can see which cost view includes discounts.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Rate Optimization capability page (read through the KPI section) and the FinOps Principles page. The AWS, Azure and Google Cloud sharing-scope sources were not readable and were dropped. Removed unconfirmed: provider sharing mechanics, the claim that pooled usage raises utilisation, the effective-cost-versus-pool allocation options and the financial independence rule for decentralised buying.
