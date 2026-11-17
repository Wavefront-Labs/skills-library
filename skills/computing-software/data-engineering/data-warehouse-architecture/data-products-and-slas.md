---
id: computing-software.data-engineering.data-warehouse-architecture.data-products-and-slas
name: data-products-and-slas
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-governance, data-products, data-mesh, output-ports, slo, sla, product-thinking, data-product-specification]
level: advanced
status: draft
description: "Define and run data products: what qualifies, the product spec (owner, output ports, contract, SLOs), measuring SLAs from data, versioning, consumer onboarding and lifecycle."
sources:
  - https://martinfowler.com/articles/data-mesh-principles.html
  - https://martinfowler.com/articles/designing-data-products.html
  - https://bitol-io.github.io/open-data-product-standard/latest/
  - https://sre.google/sre-book/service-level-objectives/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data products and SLAs

**Goal:** datasets that other teams can discover, trust and build on without talking to the producer every time — because they are owned, documented and held to explicit service levels.

## 1. What makes a dataset a product
A table becomes a data product when it has: a named owning team, intended consumers, a stable interface (output ports), a contract, service levels, documentation and a support channel. Data mesh describes the qualities as discoverable, addressable, understandable, trustworthy, natively accessible, interoperable, secure and valuable on its own.
Not everything should be a product — staging tables and one-off analyses aren't.

## 2. Product specification
```yaml
name: sales-orders
domain: sales
owner: team-sales-data          # on-call + roadmap owner
description: Confirmed customer orders, one row per order line, for revenue and fulfilment analytics.
output_ports:
  - name: orders_table
    type: table
    location: gold.sales.order_lines
    contract: contracts/order_lines.yaml      # schema, semantics, quality (ODCS)
  - name: orders_daily_extract
    type: file
    location: s3://<products-bucket>/sales/orders/daily/
slos:
  freshness: "data for day D available by 06:00 UTC D+1, 99% of days"
  completeness: "row count within 0.5% of source system control totals"
  availability: "queryable 99.9% monthly"
support: {channel: "#sales-data", response: "business hours, P1 24/7"}
lifecycle: {status: active, version: 2, deprecations: [{version: 1, sunset: 2026-12-31}]}
consumers: [finance-revenue-reporting, marketing-attribution]
```
The Open Data Product Standard (Bitol) and the Data Product Descriptor Specification provide formal schemas for this; any consistent YAML in Git with catalog sync works.

## 3. SLOs measured from the data
- Freshness: `max(loaded_at)` / readiness table per partition vs deadline.
- Completeness: reconciliation against source control totals.
- Quality: % of contract checks passing per run.
- Availability: successful probe queries.
Store daily SLI results; compute monthly attainment; publish on the product page. SLA = SLO with consequences agreed with consumers (e.g. incident review, credits for external products).

## 4. Versioning and change
- Semantic versions on the output-port contract; breaking changes ship as a new version alongside the old one with a sunset date communicated to registered consumers.
- Additive changes in place with changelog entries.

## 5. Consumers and lifecycle
- Consumers register (catalog subscription / access request) so the owner knows impact and can notify them.
- Usage metrics (queries, distinct users, downstream assets) decide investment and retirement.
- Retire products with no consumers after a notice period; keep the spec with status `retired`.

## Verify
- [ ] Each product has owner, contract, SLOs and support channel in its spec.
- [ ] SLO attainment is computed automatically and visible to consumers.
- [ ] Breaking changes go through versioning with consumer notification.
