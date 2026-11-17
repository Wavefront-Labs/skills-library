---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.data-warehouse-cost
name: data-warehouse-cost
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, architecting-for-cost, data-warehouse-cost, snowflake, bigquery, redshift, databricks, query-optimisation]
level: practitioner
status: docs-checked
description: "Control data warehouse and analytics cost: auto-suspend and sizing, resource monitors and quotas, partitioning and clustering, slot editions, and finding expensive queries."
sources: ["https://docs.snowflake.com/en/user-guide/cost-controlling", "https://docs.snowflake.com/en/sql-reference/sql/create-resource-monitor", "https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse", "https://docs.snowflake.com/en/sql-reference/account-usage/query_attribution_history", "https://cloud.google.com/bigquery/docs/best-practices-costs", "https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-billing.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html", "https://docs.databricks.com/aws/en/admin/clusters/policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data warehouse and analytics cost control

Warehouse cost is query compute (credits, slots, RPUs, DBUs) plus storage. Most savings come from
idle compute and scanning less data.

## Snowflake
```sql
ALTER WAREHOUSE bi_wh SET AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
CREATE RESOURCE MONITOR bi_rm WITH CREDIT_QUOTA = 500 FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE bi_wh SET RESOURCE_MONITOR = bi_rm;
ALTER WAREHOUSE bi_wh SET STATEMENT_TIMEOUT_IN_SECONDS = 3600;
```
Find expensive queries in `ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY` / `QUERY_HISTORY`; right-size
warehouses (bigger is not always costlier if queries finish proportionally faster); use
multi-cluster scaling for concurrency instead of oversizing.

## BigQuery
- On-demand: partition and cluster tables, avoid `SELECT *`, set `maximum_bytes_billed` per
  query and custom quotas to cap daily usage.
- Capacity pricing: use reservations (editions) for predictable workloads; see the BigQuery
  reservations docs.
- Find spend: `INFORMATION_SCHEMA.JOBS` ordered by `total_bytes_billed` or `total_slot_ms`.
- Storage: tables not modified for 90 consecutive days move to long-term storage pricing; compare
  logical and physical storage billing models.

## Redshift
Serverless: set the base RPU and maximum RPU capacity deliberately; both affect billing.

## Databricks
Use compute policies to restrict what users can create (see the Databricks compute policy docs).

## Steps
1. Top 20 queries/jobs by cost per week to owners; fix the worst (missing partition filter,
   repeated full refresh).
2. Incremental models in dbt instead of full refreshes.
3. Dashboard refresh schedules aligned to data freshness.

## Verify
- [ ] Every warehouse/cluster has auto-suspend and a spend limit or monitor.
- [ ] Weekly top-cost query report goes to owners.

## Checked
2026-11-01. Confirmed in the Snowflake ALTER WAREHOUSE, CREATE RESOURCE MONITOR and QUERY_ATTRIBUTION_HISTORY pages,
the BigQuery cost best-practices page (maximum_bytes_billed, custom quota, JOBS columns, 90-day long-term storage,
physical billing) and the Redshift Serverless capacity and billing pages (base and maximum RPU). Removed: the
require_partition_filter syntax, slot baseline and commitment details, Redshift provisioned-cluster features,
Databricks specifics (auto-termination, spot, job compute; the cited policy page returned 404 and was replaced), and the
cache and background-credit gotchas.
Method: documentation only; no commands were run.
