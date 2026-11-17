---
id: computing-software.data-engineering.data-warehouse-architecture.data-platform-cost-forecasting-and-capacity-planning
name: data-platform-cost-forecasting-and-capacity-planning
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, cost-forecasting, capacity-planning, finops, unit-economics, commitment-planning, growth-modelling]
level: practitioner
status: draft
description: "Forecast data platform cost and capacity: usage baselines from billing data, drivers and unit costs, growth scenarios, commitment sizing, budgets and alerts, and variance reviews."
sources:
  - https://www.finops.org/framework/capabilities/forecasting/
  - https://docs.snowflake.com/en/user-guide/cost-exploring-overall
  - https://cloud.google.com/bigquery/docs/information-schema-jobs
  - https://docs.databricks.com/en/admin/system-tables/billing.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cost forecasting and capacity planning

## 1. Baseline from actual usage
Pull 6-12 months of daily cost and usage by workload:
```sql
-- Snowflake: credits by warehouse per day
SELECT DATE_TRUNC('day', start_time) d, warehouse_name, SUM(credits_used) credits
FROM snowflake.account_usage.warehouse_metering_history GROUP BY 1, 2;
-- BigQuery: slot-hours / bytes by project and label
SELECT DATE(creation_time) d, project_id, labels, SUM(total_slot_ms)/3.6e6 slot_hours, SUM(total_bytes_billed)/1e12 tb
FROM `region-eu`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION GROUP BY 1, 2, 3;
-- Databricks: system.billing.usage joined to list prices
```
Plus storage (TB by tier), egress and tool licences. Tag/label everything by team, product and environment so cost is attributable.

## 2. Find drivers and unit costs
Relate spend to business or technical drivers:
- Cost per daily pipeline run, per TB ingested, per active BI user, per 1,000 queries, per data product.
- Storage growth per day of retention, per source system.
Unit costs make forecasts explainable: "ingest grows 8%/month, cost per TB ingested is X".

## 3. Forecast scenarios
- Baseline trend (seasonality matters: month-end finance loads, retail peaks).
- Plus known events: new sources onboarded, migration of workloads from legacy, new ML workloads, retention policy changes, price changes.
- Three scenarios (low/expected/high) with assumptions written down.
- Capacity: peak concurrent slots/warehouses/RPUs at p95, storage TB, ingestion throughput; check quota and reservation limits ahead of growth.

## 4. Commitments
Size commitments (Snowflake capacity, BigQuery slot commitments, Databricks commit, cloud savings plans) to the **low** scenario's steady state, cover the rest on demand. Track burn-down monthly; under-consumed commitments are pure waste, over-consumption loses discount.

## 5. Budgets, alerts and reviews
- Budgets per team/environment with alerts at 50/80/100% (cloud budgets, Snowflake resource monitors, BigQuery quotas).
- Monthly variance review: forecast vs actual by driver; explain differences (volume change vs efficiency change vs price).
- Feed back into engineering: top costly queries/pipelines, idle warehouses, unused tables (storage), over-provisioned clusters.

## Verify
- [ ] Forecast within +/-10-15% of actual over a quarter; variances explained by driver.
- [ ] All spend attributable to an owner via tags/labels; commitment utilisation tracked monthly.
