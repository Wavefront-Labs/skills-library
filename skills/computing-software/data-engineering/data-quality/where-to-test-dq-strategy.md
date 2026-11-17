---
id: computing-software.data-engineering.data-quality.where-to-test-dq-strategy
name: where-to-test-dq-strategy
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-test-strategy, testing-strategy, shift-left, test-placement]
level: advanced
status: draft
description: "Decide where data quality tests belong across source, ingestion, transformation and serving layers, which test types run where, and how to avoid duplicate noisy tests."
sources:
  - https://docs.getdbt.com/best-practices/writing-custom-generic-tests
  - https://www.getdbt.com/blog/building-a-data-quality-framework-with-dbt-and-dbt-cloud
  - https://docs.soda.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Where to test: source, transform, serve

**Goal:** catch each kind of problem at the cheapest point, once, with clear ownership.

## Layered strategy
| Layer | Test types | Owner | On failure |
|---|---|---|---|
| Source / producer | schema contracts, required fields, enum values, referential checks at entry | producing team | reject at source, alert producer |
| Ingestion (raw/bronze) | freshness, volume vs expected, schema drift, duplicates on load keys, file completeness | data platform | stop downstream (circuit breaker), alert |
| Staging | primary key unique/not null, type casts succeeded, accepted values | data engineering | fail build of dependents |
| Transformation (intermediate/marts) | business rules, relationships, reconciliation to source totals, metric sanity ranges | analytics engineering | fail or warn per severity |
| Serving (BI, reverse ETL, ML) | final metric anomaly checks, row counts in exports, freshness at consumption | data product owner | hold publish, notify consumers |

## Principles
- **Shift left**: the earlier a defect is caught, the smaller the blast radius. Push checks to producers through contracts.
- **Test once**: if staging enforces uniqueness of `order_id`, do not retest it on every mart that passes it through; test what the mart changes (its own grain, its joins).
- **Test the grain** of every model: uniqueness of its declared key catches most join fan-out bugs.
- **Reconcile at boundaries**: counts/sums from source to warehouse and from staging to marts.
- **Monitor what you cannot rule-test**: anomaly detection for distributions and volumes complements explicit rules.

## Blocking vs non-blocking
Block publication for tests where wrong data is worse than late data (finance, customer-facing); warn for exploratory datasets. Write-audit-publish patterns implement blocking cleanly.

## Coverage review
Map tests to critical data elements and to past incidents: every incident should have produced a test at the right layer.

## Verify
Each critical model has a grain test and at least one business rule test; each source has freshness and volume checks; incidents last quarter map to new tests.
