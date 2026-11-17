---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-informed-pricing
name: cost-informed-pricing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, cost-informed-pricing, pricing-decisions, cost-to-serve]
level: advanced
status: docs-checked
description: "Feed unit economics into pricing and packaging decisions per the Unit Economics capability: cost to serve, contribution margin and shift-left."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost-informed pricing

The Unit Economics capability says unit metrics help product owners understand direct and indirect
costs driven by customer or employee usage, enabling workload placement, packaging, pricing and
roadmap tradeoffs.

## Steps
1. Define business unit metrics such as cost per customer, cost to serve and cost per transaction for the product (see unit-metric-selection).
2. Compare them with the revenue or value each unit generates to see contribution margin, product sustainability and pricing tradeoffs. Where revenue attribution is hard, use outcome value proxies.
3. Use industry-specific views where they fit, such as cost of service delivery as a percent of revenue.
4. Shift left: at Run, unit economics are considered early enough to shape build vs buy, architecture, workload placement, migration, sourcing and pricing decisions, rather than reported after the bill lands.
5. Procurement and Leadership use the metrics to inform vendor selection, renewals and commercial model choices, including commitments, entitlements and consumption exposure.
6. Review the results on a consistent cadence, for example in operating reviews.

## Verify
- [ ] Cost to serve is documented with its definition and cost inclusions.
- [ ] Pricing or packaging decisions reference the unit metric.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Unit Economics capability page (full text read). The Quantify Business Value domain page was not read and is no longer cited.
Removed as unconfirmed: the percentile distribution advice and the 10-100x heavy-user claim, the gross margin and price floor formulas with worked example, free tier sizing, the Pro plan example, and the gotchas.
