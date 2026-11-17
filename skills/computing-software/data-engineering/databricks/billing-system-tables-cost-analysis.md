---
id: computing-software.data-engineering.databricks.billing-system-tables-cost-analysis
name: billing-system-tables-cost-analysis
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, system-tables, billable-usage, system-billing-usage, list-prices, cost-attribution, finops, budget-policies, custom-tags]
level: practitioner
status: docs-checked
description: "Analyse Databricks spend from system.billing.usage and list_prices: cost by job, product and tag, serverless attribution, budgets, anomaly checks."
sources:
  - https://docs.databricks.com/aws/en/admin/system-tables/billing
  - https://docs.databricks.com/aws/en/admin/system-tables/pricing
  - https://docs.databricks.com/aws/en/admin/usage/system-tables
  - https://docs.databricks.com/aws/en/admin/account-settings/budgets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing system tables cost analysis

**Goal:** answer "what costs what, who owns it, and what changed" from SQL, so cost reviews target the biggest movers.

## 1. The tables
- `system.billing.usage` — one row per usage record: `usage_date`, `workspace_id`, `sku_name`, `usage_quantity` (DBUs, or other units), `usage_unit`, `billing_origin_product` (JOBS, SQL, DLT, MODEL_SERVING, ...), `usage_metadata` (struct: `job_id`, `job_run_id`, `cluster_id`, `warehouse_id`, `dlt_pipeline_id`, `notebook_id`, ...), `identity_metadata.run_as`, `custom_tags`, `product_features` (e.g. serverless, Photon).
- `system.billing.list_prices` — list price per `sku_name` over time (`price_start_time`, `price_end_time`, `pricing.default`). Your negotiated discount is not included; apply it as a factor.
Users need permission to access system table data; grant it to the FinOps group.

## 2. Cost in currency
```sql
CREATE OR REPLACE VIEW ops.usage_cost AS
SELECT u.*, u.usage_quantity * p.pricing.default AS list_cost
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON u.sku_name = p.sku_name AND u.cloud = p.cloud AND u.usage_unit = p.usage_unit
 AND u.usage_end_time >= p.price_start_time
 AND (p.price_end_time IS NULL OR u.usage_end_time < p.price_end_time);
```

## 3. Standard questions
```sql
-- top jobs last 30 days, with names
WITH c AS (
  SELECT workspace_id, usage_metadata.job_id AS job_id, sum(list_cost) AS cost
  FROM ops.usage_cost WHERE usage_date >= current_date() - 30 AND usage_metadata.job_id IS NOT NULL
  GROUP BY 1, 2),
j AS (
  SELECT workspace_id, job_id, name FROM system.lakeflow.jobs
  QUALIFY row_number() OVER (PARTITION BY workspace_id, job_id ORDER BY change_time DESC) = 1)
SELECT j.name, c.job_id, c.cost FROM c LEFT JOIN j USING (workspace_id, job_id)
ORDER BY c.cost DESC LIMIT 20;
-- by product and by team tag
SELECT billing_origin_product, custom_tags['team'] AS team, sum(list_cost) FROM ops.usage_cost
WHERE usage_date >= date_trunc('month', current_date()) GROUP BY ALL;
-- week-over-week movers by SKU
SELECT sku_name, sum(CASE WHEN usage_date >= current_date()-7 THEN list_cost END) AS this_wk,
                 sum(CASE WHEN usage_date <  current_date()-7 THEN list_cost END) AS last_wk
FROM ops.usage_cost WHERE usage_date >= current_date()-14 GROUP BY 1 ORDER BY this_wk - last_wk DESC;
```
`system.lakeflow.jobs` is an SCD-style table — take the latest row per job.

## 4. Attribution that works
- Tag everything: cluster policies enforce `custom_tags.team` / `cost_center`; jobs carry `tags`; SQL warehouses have tags.
- Serverless compute has no cluster to tag — use **serverless usage policies**: their tags are added to `custom_tags`, and usage rows carry `usage_metadata.usage_policy_id` (`budget_policy_id` is deprecated).
- `identity_metadata.run_as` shows who ran serverless/job usage when tags are missing.
- All-purpose clusters used by many people are hard to attribute — another reason to move scheduled work to job compute.

## 5. Guardrails
- Account console budgets scoped by product, workspace or custom tags, with email alerts when spending exceeds a threshold.
- A daily SQL alert when yesterday's cost > 1.5x the trailing 14-day average.
- Review: idle all-purpose clusters (long auto-termination), jobs on all-purpose compute, oversized warehouses, DLT continuous pipelines that could be triggered.

## Verify
- [ ] Cost view total for a past month is within the expected discount factor of the invoice.
- [ ] Nearly all spend has a team tag or usage policy (set your own target).
- [ ] Anomaly alert fires on a synthetic spike (test with a lowered threshold).

## Checked

2026-11-09. Confirmed on the Databricks billing system table, pricing system table, billing usage and budgets pages: system.billing.usage columns (usage_date, usage_end_time, sku_name, usage_quantity, usage_unit, cloud, billing_origin_product, usage_metadata fields, identity_metadata, custom_tags), list_prices price_start_time, price_end_time and the pricing struct with default and effective_list keys, serverless usage policy tags landing in custom_tags, budget_policy_id deprecated in favour of usage_policy_id, budgets scoped by product, workspace and tags with email alerts. Removed: the schema-enable step and the 90% coverage figure (not on the pages read). The 1.5x anomaly threshold is a suggested heuristic, not a documented figure.

Method: documentation only; no commands were run.

