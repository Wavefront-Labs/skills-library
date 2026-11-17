---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.unit-metric-selection
name: unit-metric-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, unit-metric-selection, business-metrics, cost-per-unit]
level: practitioner
status: docs-checked
description: "Choose unit metrics using the Unit Economics capability: resource-efficiency vs business metrics, Crawl instrumentation, and metric review and retirement."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing unit metrics

Unit economics ties technology cost to business outcomes. Metrics can be defined for many aspects of
usage, so the choice depends on the goals of the organisation or product.

## Two categories
- **Resource Efficiency metrics**: for example cost per GB stored, per GB transferred, per vCPU, per seat used, per token. Engineers can implement these as controllable signals within their domain.
- **Business Unit metrics**: for example cost per tenant, per transaction, per customer, per case resolved, cost to serve. These give Leadership and Product owners context for tradeoffs across cost, speed, quality and risk, and often indicate higher maturity.

## Steps
1. Pick the FinOps Scope (product, workload, cohort) and the goal the metric serves. For Generative AI, start with cost per token and grow toward cost per assist, agent action or case deflected.
2. At Crawl, start with resource-efficiency metrics on direct variable cost in one technology category, and plant the data: tag resources and emit a usage counter (the denominator) during development.
3. Document metric definitions and assumptions, and put change control on definitions and cost inclusions (Leadership sponsors this).
4. Use fully loaded costs as you move to Walk and Run, and add business unit metrics as data and trust catch up. Normalise cost and usage data across vendors; FOCUS can simplify this.
5. Surface unit cost where the usage decision is made (design reviews, dev environment).
6. Review regularly: adjust, add or retire metrics, including where comparing dissimilar products causes more confusion than insight.

## Verify
- [ ] Each metric has a documented definition, scope and owner.
- [ ] A trend over time is reported for each metric in scope.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Unit Economics capability page (full text read). The book chapter source was not read and is no longer cited.
Removed as unconfirmed: the denominator table by industry, the four-test list (correlation, controllability, daily availability), the daily metric table design, and the pitfalls list.
