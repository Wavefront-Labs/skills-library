---
id: computing-software.data-engineering.snowflake.gen2-and-adaptive-warehouses
name: gen2-and-adaptive-warehouses
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, gen2-warehouse, warehouses, resource-constraint, adaptive-compute]
level: advanced
status: docs-checked
description: "Evaluate and switch Snowflake standard warehouses to Gen2 (GENERATION, RESOURCE_CONSTRAINT), compare cost per query, and note adaptive warehouses."
sources:
  - https://docs.snowflake.com/en/user-guide/warehouses-gen2
  - https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gen2 and adaptive warehouses

**Goal:** decide per workload whether next-generation compute lowers cost per query, and switch safely.

## Gen2 standard warehouses
Gen2 runs on faster hardware with engine optimisations (notably for delete, update and merge operations and table scans). The docs say to test how much it improves cost, performance, or both, so the win must be measured per workload. Credit rates for Gen2 are in the Snowflake Service Consumption Table; read it for your size before switching.
```sql
CREATE WAREHOUSE transform_g2 WAREHOUSE_SIZE = MEDIUM GENERATION = '2'
  AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
ALTER WAREHOUSE transform_wh SET GENERATION = '2';   -- in-place switch
SHOW WAREHOUSES LIKE 'TRANSFORM%';     -- resource_constraint column
```
`GENERATION = '1' | '2'` is the recommended clause; `RESOURCE_CONSTRAINT = STANDARD_GEN_1 | STANDARD_GEN_2` is equivalent, and a mismatch when both are given is an error. Neither is available in Snowsight; use SQL.

- Not available for sizes X5LARGE and X6LARGE; applies to standard warehouses only, not Snowpark-optimized.
- If you create a standard warehouse without GENERATION it defaults to `'2'` unless Gen2 is not available in your region.
- New Gen2 warehouses get Query Acceleration Service enabled by default (max scale factor 8); altering a Gen1 warehouse to Gen2 leaves QAS as it was.
- Gen2 is on AWS, Azure and GCP in all regions with a few documented exceptions. With account replication, secondary regions must support Gen2 or the warehouse may not resume after failover.

## Evaluate properly
1. Clone the workload: run the same dbt job / query set on a Gen1 and a Gen2 warehouse of the same size.
2. Compare `credits_used` (from `WAREHOUSE_METERING_HISTORY`) per job and runtime from `QUERY_HISTORY`, not runtime alone.
3. Try one size **smaller** on Gen2 and compare again.
```sql
select warehouse_name, sum(credits_used) from snowflake.account_usage.warehouse_metering_history
where start_time >= dateadd('day', -7, current_timestamp()) group by 1;
```

## Adaptive warehouses
`ALTER WAREHOUSE` documents `WAREHOUSE_TYPE = ADAPTIVE` with its own enable/disable setting and properties. Treat it as a separate feature: read the Adaptive Warehouse pages for current availability, properties and billing, pilot on a non-critical workload, and keep resource monitors/budgets on it.

## Gotchas
- Changing the generation (or any `RESOURCE_CONSTRAINT`) while the warehouse runs: queries already running finish on the old resources, new queries use the new ones, and you are billed for both sets until the old queries finish; the warehouse does not auto-suspend meanwhile. Convert while suspended to avoid the double charge.
- Snowpark-optimized warehouses use the memory `RESOURCE_CONSTRAINT` values (MEMORY_1X and so on); `GENERATION` cannot be used with them. Snowpark-optimized warehouses are not available as Gen2.
- The setting shows in the `resource_constraint` column of `SHOW WAREHOUSES`, not in INFORMATION_SCHEMA views.

## Verify
After a week on Gen2, credits per job for the switched workload are lower than the Gen1 baseline; otherwise switch back.

## Checked
2026-11-09. Confirmed against the Snowflake docs pages "Snowflake generation 2 standard warehouses" and "ALTER WAREHOUSE": GENERATION and RESOURCE_CONSTRAINT values and equivalence, not in Snowsight, X5LARGE/X6LARGE exclusion, default generation, QAS default and scale factor 8, region/replication caveat, conversion billing behaviour, SHOW WAREHOUSES column, WAREHOUSE_TYPE = ADAPTIVE. Removed: the claim that Gen2 credits per hour are higher than Gen1 (the rate table PDF could not be read for Gen2 rows), "restarts the warehouse / queue briefly", and the "heavy MERGE benefits most" claim. Adaptive warehouse behaviour is not described beyond the ALTER WAREHOUSE syntax.
Method: documentation only; no commands were run.
