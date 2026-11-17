---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cloud-cogs
name: cloud-cogs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, cloud-cogs, cost-of-goods-sold, gross-margin, r-and-d-vs-cogs, saas-metrics, cost-classification]
level: advanced
status: draft
description: "Split cloud cost into COGS vs R&D/opex for gross margin: classification rules by environment and workload, shared-cost treatment, and the reporting finance and investors expect."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/", "https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud cost in COGS and gross margin

For SaaS and digital businesses, the cost of running production for customers is usually Cost of
Goods Sold (COGS); development and internal tooling is R&D or G&A. Gross margin = (revenue − COGS)
/ revenue — a headline metric for SaaS valuation.

## Classification rules (agree with finance)
| Cost | Typical class |
|---|---|
| Production environments serving customers | COGS |
| Customer-facing support tooling, customer data storage/backups | COGS |
| Dev, test, staging, CI | R&D |
| Internal analytics, corporate IT workloads | G&A / R&D |
| Shared platform (networking, observability, security) | split by usage share of prod vs non-prod |
| Commitment discounts / unused commitments | follow the usage they cover; unused → finance policy (often COGS) |

## Steps
1. Make environment a mandatory dimension (account structure or tag) — classification depends on it.
2. Map each allocation group to a P&L class in the enrichment table with effective dates.
3. Monthly: report COGS cloud cost, COGS per unit, and cloud COGS as % of revenue.
4. Track trend as the business scales — cloud COGS % should fall with scale; if not, investigate.

## Gotchas
- Prod used for demos/testing inflates COGS; non-prod resources in prod accounts the reverse.
- Reclassifications change historic margins — freeze closed periods.

## Verify
- [ ] Classification table reviewed by finance and auditors.
- [ ] Cloud COGS % of revenue reported monthly.
