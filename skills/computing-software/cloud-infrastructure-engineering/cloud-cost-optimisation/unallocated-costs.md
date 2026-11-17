---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.unallocated-costs
name: unallocated-costs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-allocation, unallocated-costs, untaggable-costs, support-charges, platform-overhead, allocation-residual]
level: practitioner
status: docs-checked
description: "Handle costs that cannot be tagged (support, tax, shared platform) with a shared cost strategy: central budget, fixed, proportional or proxy-metric splits."
sources: ["https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling unallocatable and shared costs

## Why they exist
The FinOps Allocation capability notes that some costs cannot be tagged in some environments.
Its examples of shared costs are support costs that benefit all users, centralised networking
services, and shared environments such as platforms and containers.

## Approach
1. **Write a shared cost strategy**: define which subsets of cost are shared among allocation
   targets, and the mechanism for each shared cost item. Finance determines the percentages for
   shared items.
2. **Choose an allocation policy per item.** Many early practices use "informed ignore": an
   explicit business decision to budget the item centrally rather than from each cost centre.
   Most organisations mix central funding with allocation to cost centre budgets.
3. **Pick a split method**: fixed allocation, proportional allocation, or a proxy metric that
   gives a variable proportion. Finer shared-cost allocation can draw on the CMDB,
   observability or utilisation data.
4. **Spread discounts** proportionally across teams' spend; the page lists this at Walk maturity,
   and at Run it expects shared cost recovery to reflect commercial and commitment discounts.
5. **Make shared costs visible**: distinguish shared from dedicated costs, and let shared
   platform owners show back what internal customers generate.
6. **Document the apportionment** and how new cost centres onboard at a "fair share".
7. **Track allocation KPIs** and investigate unallocated, untagged or unidentified cost.

## Notes
- Complete consistency is hard to reach. The page says to aim for the level of allocation that
  gives enough information to make good decisions at your maturity.
- Without a shared cost process, product and engineering teams manage to direct costs only,
  which the page says reduces forecast and budget accuracy.

## Verify
- [ ] Each shared cost item has a documented treatment and owner.
- [ ] Teams can see the basis of their share.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Allocation capability page (read through the functional activities). The AWS split-charge and FOCUS sources were not read. Removed unconfirmed: the per-cost-type treatment table (tax, credits, unused commitments), FOCUS ChargeCategory identification, AWS cost category split rules, and the gotchas.
