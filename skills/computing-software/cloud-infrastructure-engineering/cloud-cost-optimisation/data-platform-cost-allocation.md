---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.data-platform-cost-allocation
name: data-platform-cost-allocation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, allocation, data-platform-cost-allocation, snowflake, bigquery, databricks, query-attribution, shared-cost-allocation]
level: practitioner
status: draft
description: "Allocate shared data platform cost (Snowflake, BigQuery, Databricks) to teams: per-query attribution, query tags and labels, warehouse ownership, storage by schema and idle share."
sources: ["https://docs.snowflake.com/en/sql-reference/account-usage/query_attribution_history", "https://cloud.google.com/bigquery/docs/information-schema-jobs", "https://docs.databricks.com/aws/en/admin/system-tables/billing", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Allocating shared data platform costs

Data platforms are often the biggest shared bill and the hardest to split, because many teams
query one account. Allocate compute by consumption and storage by ownership.

## Snowflake
- Compute: `SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY` gives
  `credits_attributed_compute` per query (excludes warehouse idle time). Group by `query_tag`,
  user or role.
  ```sql
  SELECT COALESCE(NULLIF(query_tag,''),'untagged') tag, SUM(credits_attributed_compute) credits
  FROM snowflake.account_usage.query_attribution_history
  WHERE start_time >= DATEADD(day,-30,CURRENT_TIMESTAMP()) GROUP BY 1 ORDER BY 2 DESC;
  ```
- Idle: `WAREHOUSE_METERING_HISTORY.credits_used_compute` minus attributed credits; give it to the
  warehouse owner. Dedicated warehouses per team make this simple.
- Set `ALTER SESSION SET QUERY_TAG = '{"team":"risk","job":"daily_pnl"}'` in tools and dbt
  (`query_tag` config).
- Storage: `DATABASE_STORAGE_USAGE_HISTORY` / `TABLE_STORAGE_METRICS` by database or schema owner;
  serverless features (Snowpipe, auto-clustering, materialised views) from their own history views.

## BigQuery
- On-demand: `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` / `JOBS` `total_bytes_billed` x price,
  grouped by `project_id`, `user_email` or job `labels`.
- Editions (slots): allocate reservation cost by `total_slot_ms` share per project/label; idle slots
  to the reservation owner.
- Storage: `TABLE_STORAGE` by dataset; billing labels on datasets flow into the billing export.

## Databricks
- `system.billing.usage` with `custom_tags`, `usage_metadata.job_id`, `cluster_id`,
  `warehouse_id`; join `system.billing.list_prices` for cost. Enforce tags with cluster policies.
- Cloud infrastructure (VMs, storage) bills separately in the cloud account; tag clusters so the
  cloud bill carries the same team tag.

## Steps
1. Decide ownership per object: warehouse/reservation/workspace owner, dataset/schema owner.
2. Mandate attribution metadata (query tags, labels, cluster tags) via platform config.
3. Daily job computes per-team compute + storage + idle share; publish alongside cloud costs.
4. Reconcile to the platform invoice monthly.

## Gotchas
- Shared BI service accounts hide the real consumer; tag queries with the dashboard or team.
- Per-query attribution excludes idle and cloud services credits; allocate the remainder explicitly.

## Verify
- [ ] Attributed + idle + storage = platform invoice for the month.
- [ ] Untagged compute share is tracked and falling.
