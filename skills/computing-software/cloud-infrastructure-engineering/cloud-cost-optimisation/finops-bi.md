---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-bi
name: finops-bi
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, reporting-and-analytics, finops-bi, focus-specification, power-bi, looker, quicksight, cost-dashboards, semantic-model]
level: practitioner
status: draft
description: "Build BI dashboards over FOCUS cost data: a semantic model with measures for billed, effective and list cost, savings, coverage and unit cost, plus row-level security per team."
sources: ["https://focus.finops.org/", "https://learn.microsoft.com/cloud-computing/finops/toolkit/power-bi/reports", "https://catalog.workshops.aws/awscid/en-US", "https://www.finops.org/framework/capabilities/reporting-analytics/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BI dashboards over FOCUS data

FOCUS gives every provider the same columns, so one semantic model serves all clouds. Build the
model once; dashboards become thin.

## Semantic model
- **Fact**: FOCUS rows at daily grain (aggregate hourly first): ChargePeriodStart (date),
  BillingPeriodStart, ProviderName, BillingAccountId, SubAccountId, ServiceCategory, ServiceName,
  RegionId, ResourceId (optional, large), ChargeCategory, CommitmentDiscountStatus, Tags (flattened
  owner/app/env), BilledCost, EffectiveCost, ListCost, ContractedCost, ConsumedQuantity.
- **Dimensions**: date, owner registry (team -> BU -> cost centre), service map, budgets, business
  metrics (for unit cost).
- **Measures** (DAX-style shown):
  ```text
  Effective Cost   = SUM(EffectiveCost)
  Billed Cost      = SUM(BilledCost)
  Savings          = SUM(ListCost) - SUM(EffectiveCost)
  ESR              = DIVIDE([Savings], SUM(ListCost))
  Unused Commit    = CALCULATE([Effective Cost], CommitmentDiscountStatus = "Unused")
  Unit Cost        = DIVIDE([Effective Cost], SUM(metrics[units]))
  MoM %            = DIVIDE([Effective Cost] - [Effective Cost PM], [Effective Cost PM])
  ```

## Steps
1. Land FOCUS data from each provider; union into one table with a `ProviderName` column.
2. Build daily aggregate tables (by team, service, region) for speed; keep resource-level for
   drill-through only.
3. Row-level security: team members see their teams; finance and FinOps see all.
4. Standard pages: overview, trend, by team, by service, commitments, anomalies, unit cost,
   recommendations. Each page shows the as-of date and cost basis.
5. Starting points: Microsoft FinOps toolkit Power BI reports (FOCUS-based), AWS Cloud Intelligence
   Dashboards (QuickSight), Looker Studio templates for the GCP export.

## Gotchas
- Resource-level daily data is large; import mode hits size limits. Use aggregations or DirectQuery
  on the warehouse.
- Tag columns explode as JSON; flatten the few enforced keys in the pipeline, not in the BI tool.
- Different FOCUS versions per provider: pin versions and map missing columns to null.

## Verify
- [ ] Dashboard totals equal the warehouse totals for the same filter.
- [ ] RLS tested with a team user account.
