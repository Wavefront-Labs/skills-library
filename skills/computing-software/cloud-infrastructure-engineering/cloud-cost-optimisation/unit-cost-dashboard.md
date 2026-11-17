---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.unit-cost-dashboard
name: unit-cost-dashboard
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, unit-cost-dashboard, unit-cost, cost-per-customer, kpi-targets, cost-dashboards]
level: practitioner
status: docs-checked
description: "Build a unit cost dashboard: resource-efficiency and business unit metrics, trend within a scope, documented definitions, owners and a review cadence."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit cost dashboard and targets

Unit cost (cost per transaction, per customer, per GB stored) relates technology spend to the value it creates, so a rise
in cost can be read as economies of scale, productivity gain or a runaway cost driver.

## Layout
1. **Two metric families on separate views** (Framework wording):
   - Resource efficiency unit metrics, for example cost per GB stored, cost per GB transferred, cost per vCPU, cost per
     seat used, cost per token. Engineers can implement these as controllable signals.
   - Business unit metrics, for example cost per tenant, cost per transaction, cost to serve, cost per case resolved.
     These give leadership and product owners context for tradeoffs across cost, speed, quality and risk.
2. **Trend over time within one defined FinOps Scope.** The Framework says this is usually the most actionable view,
   rather than forcing comparability across unrelated products.
3. **Show cost and the volume denominator together**, so a change in unit cost can be traced to spend or to usage.
4. **Mark one-off events** that explain a movement.

## Data and definitions
- Document each metric's data sources, correlations, calculation, assumptions and cost inclusions, so every persona
  interprets it the same way.
- Keep direct variable cost distinct from fully loaded or TCO views: the Framework places direct variable cost at
  Crawl and fully loaded costs at Walk and Run.
- Normalise datasets where metrics span vendors or technology categories.

## Targets and governance
1. Agree each metric's definition and owner with product, engineering and finance; assign ownership and change control
   for definitions.
2. Set targets against a baseline captured before the planned change, and tie them to the work expected to move them.
3. Set a cadence for reviewing, adopting, changing and retiring metrics; retire those where cross-product comparison
   causes confusion.

## Gotchas
- A metric nobody trusts causes repeated debate over definitions; stabilise the definition first.
- Unit cost can legitimately rise when proportionally more business value is delivered.

## Verify
- [ ] Each metric has a documented definition, owner and data source.
- [ ] Each priority scope shows unit cost, volume and trend on one view.

## Checked
Confirmed on the FinOps Framework Unit Economics page (read in full): the two metric categories and their examples,
trend within a defined scope, documented definitions and assumptions, governance cadence and retirement, direct variable
cost at Crawl versus fully loaded cost at Walk and Run, normalisation across vendors, cost rising with value. Removed:
the rate, efficiency and mix decomposition, the -10 percent year-on-year example, the 3-6 month baseline, the monthly
table schema, and the AWS Well-Architected source (unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Unit Economics capability page
