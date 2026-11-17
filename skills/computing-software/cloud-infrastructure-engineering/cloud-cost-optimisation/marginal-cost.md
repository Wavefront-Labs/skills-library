---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.marginal-cost
name: marginal-cost
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, marginal-cost, economies-of-scale, pricing-decisions]
level: advanced
status: docs-checked
description: "Use marginal cost and marginal revenue from the Unit Economics capability to find break-even, contribution margin and pricing tradeoffs."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marginal cost in unit economics

The Unit Economics capability says the discipline is often discussed in terms of marginal cost
(unit cost metrics) and, where feasible, marginal revenue (unit revenue metrics). Comparing the two
can highlight break-even points and profitability dynamics.

## Steps
1. Define the unit cost metric for the FinOps Scope and document the metric definition and its cost inclusions and assumptions.
2. Where revenue can be attributed, define the matching unit revenue metric. Where it cannot, use an outcome value proxy such as demand, throughput, customer experience, risk reduction or service levels.
3. Compare unit cost with unit revenue or value to see break-even and contribution margin, and use that in product sustainability and pricing tradeoff discussions.
4. Read spend changes against the unit metric: they may be economies of scale, productivity gains or runaway cost drivers. Rising cost is not always negative if proportionally more value is delivered.
5. Follow the trend over time within the defined scope; the Framework notes this is usually more actionable than forcing comparison across unrelated products.
6. Crawl uses direct variable cost; Walk and Run move to fully loaded costs (shared costs, TCO).

## Verify
- [ ] Metric definition and cost inclusions are documented and owned.
- [ ] Cost and revenue (or value proxy) are compared on the same unit and scope.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Unit Economics capability page (full text read).
Removed as unconfirmed: the daily cost regression with fixed and marginal terms, step-cost procedure, free-tier and big-deal formulas, the pricing floor rule, and the commitment and retention gotchas.
