---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.tco-analysis
name: tco-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-estimation, tco-analysis, total-cost-of-ownership, migration-business-case, on-premises-comparison, depreciation, double-running]
level: advanced
status: draft
description: "Build an honest on-prem vs cloud TCO: full on-prem cost stack, right-sized cloud target, migration one-offs and double-running, multi-year cash flow, and sensitivity analysis."
sources: ["https://www.finops.org/framework/capabilities/planning-estimating/", "https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/financial-considerations/", "https://aws.amazon.com/economics/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration TCO comparison

## On-prem side (fully loaded, annualised)
Hardware (servers, storage, network) with refresh cycle and depreciation; data centre (space,
power at PUE, cooling) or colo fees; software licences and support (hypervisor, OS, DB, backup,
monitoring); staff time (FTE share for hardware, DC ops, patching); DR site; maintenance
contracts; capacity headroom you over-buy.

## Cloud side
1. Start from **utilisation data** (CPU p95, memory, IOPS) — right-size, don't map 1:1 from VM specs.
2. Price target services with commitments applied for steady workloads.
3. Include egress, managed service premiums, observability, security tooling, support plan.
4. Licensing: BYOL eligibility vs licence-included pricing (Windows/SQL Server rules differ by
   cloud and date of licence purchase).

## One-offs and transition
Migration labour/partners, tooling, training, **double-running** (both estates for months),
contract exit penalties, early write-off of not-fully-depreciated hardware; offset by provider
migration incentives/credits.

## Model
- 3-5 year cash flow per year, NPV at the company's discount rate.
- Sensitivity: ±20% on cloud usage, commitment level, migration duration, hardware refresh avoided.
- Non-cost value listed separately (time to market, resilience, scaling) — don't bury it in TCO numbers.

## Gotchas
- Comparing a right-sized, discounted cloud estimate to an on-prem figure with no staff costs (or the reverse).
- Assuming staff savings that won't materialise (people are redeployed, not removed).
- Ignoring that on-prem hardware is already paid for until refresh — timing migrations to refresh cycles matters.

## Verify
- [ ] Finance has reviewed and owns the on-prem cost baseline.
- [ ] Sensitivity table shows the decision holds across plausible ranges (or says when it doesn't).
