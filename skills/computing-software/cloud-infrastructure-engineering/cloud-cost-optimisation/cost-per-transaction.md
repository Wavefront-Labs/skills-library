---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-per-transaction
name: cost-per-transaction
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, cost-per-transaction, cost-per-request, unit-cost-calculation, business-metrics-join]
level: practitioner
status: docs-checked
description: "Define and track cost per transaction as a FinOps business unit metric: document the unit, cost inclusions and data sources, and read the trend within a scope."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cost per transaction / request

The FinOps Framework lists cost per transaction as a Business Unit Metric, alongside cost per
tenant, cost to serve and cost per case resolved. Cost per request or per API call sits on the
technical side, nearer the resource efficiency metrics (cost per GB, per vCPU, per token).

## Steps
1. **Define the unit** in business terms and document the metric definition, assumptions and cost
   inclusions so every persona reads it the same way. Clarify the business data source and the
   unit definition up front to reduce debate.
2. **Plant the denominator early.** Tag resources and emit a usage counter during development so
   the count exists later; the framework calls this the cheapest, highest-leverage move at Crawl.
3. **Choose the cost scope for your maturity.** Crawl-level unit metrics use direct variable cost
   in one technology category (usually public cloud). Walk adds fully loaded costs and costs outside
   direct technology use; Run applies fully loaded costs across all applicable categories.
4. **Join cost to volume** from the business system of record, using normalised cost and usage data
   (FOCUS where possible) when the metric spans vendors or technology categories.
5. **Track the trend over time within a defined FinOps Scope** rather than forcing comparison
   across unrelated products. Pairing spend with value lets a rising total be read as economies of
   scale, productivity gains or a runaway cost driver.
6. **Review on a cadence**: adjust, add or retire metrics, including ones that compare dissimilar
   products and create more confusion than insight.

## Interpreting
- Rising cost is not always bad if proportionally more business value is delivered.
- Unit economics is often framed as marginal cost (and marginal revenue where feasible) to show
  break-even points; where revenue attribution is hard, use outcome value proxies such as demand,
  throughput or service levels.

## Verify
- [ ] Metric definition, cost inclusions and data sources are documented and owned.
- [ ] The series is reviewed on a set cadence within a stated scope.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Unit Economics capability page (read in full).
Removed as unconfirmed: the step-by-step warehouse join recipe, amortised-cost requirement, alert on N days over a threshold, per-product targets, fixed versus variable cost separation, health-check and retry counting gotcha, and the AWS Well-Architected source (host unreadable).
