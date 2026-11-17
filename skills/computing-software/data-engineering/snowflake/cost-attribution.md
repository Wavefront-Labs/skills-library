---
id: computing-software.data-engineering.snowflake.cost-attribution
name: cost-attribution
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, cost-attribution, query-attribution-history, object-tagging, query-tag, warehouse-metering-history, chargeback, showback, finops, account-usage]
level: advanced
status: docs-checked
description: "Attribute Snowflake spend to teams: object tags on warehouses and users, QUERY_ATTRIBUTION_HISTORY per query, query tags, and idle-time allocation."
sources:
  - https://docs.snowflake.com/en/user-guide/cost-attributing
  - https://docs.snowflake.com/en/sql-reference/account-usage/query_attribution_history
  - https://docs.snowflake.com/en/sql-reference/account-usage/metering_history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake cost attribution

**Goal:** answer "who spent what on which workload" well enough for showback/chargeback and to target optimisation. Snowflake's recommended approach: object tags to associate resources and users with departments or projects, and query tags when one application runs queries on behalf of users from several departments.

## Three scenarios
1. Resources used by one department: tag the warehouses, attribute their whole cost.
2. Warehouse shared by departments: tag each user; attribute per-query cost to users, then group by the user tag.
3. Application issuing queries for many departments: set a `QUERY_TAG` per session (for example `ALTER SESSION SET QUERY_TAG = 'COST_CENTER=finance'`) and group by it.

## Set up tags
Create the tag in a database and schema you choose (a dedicated one, or the organization account if resources span accounts; replicate the tag database to other accounts with a replication group). A tag can restrict values with `ALLOWED_VALUES`.
```sql
create database cost_management;
create schema cost_management.tags;
create tag cost_management.tags.cost_center allowed_values 'finance', 'marketing', 'engineering', 'product';
alter warehouse warehouse1 set tag cost_management.tags.cost_center = 'SALES';
alter user finance_user set tag cost_management.tags.cost_center = 'FINANCE';
```
Tip from the docs: automate tagging when resources and users are created. Users provisioned through a SCIM identity provider can carry tags through the `snowflakeTags` custom attribute.

## Dedicated warehouses: join tags to metering
Join `TAG_REFERENCES` to `WAREHOUSE_METERING_HISTORY` on `warehouse_id = object_id` with `domain = 'WAREHOUSE'`:
```sql
select coalesce(t.tag_value, 'untagged') as tag_value, sum(m.credits_used_compute) as credits
from snowflake.account_usage.warehouse_metering_history m
left join snowflake.account_usage.tag_references t
  on m.warehouse_id = t.object_id and t.domain = 'WAREHOUSE'
where m.start_time >= dateadd(month, -1, date_trunc('month', current_date))
  and m.start_time < date_trunc('month', current_date)
group by 1 order by 2 desc;
```
In the organization account, the same query works over `ORGANIZATION_USAGE` views; `TAG_REFERENCES` there exists only in the organization account.

## Shared warehouses: per-query attribution
`QUERY_ATTRIBUTION_HISTORY` (ACCOUNT_USAGE only, no organization-wide equivalent) gives `credits_attributed_compute` per query for the last 365 days; full data starts mid-August 2024. It carries `user_name`, `query_tag`, `warehouse_name`, `query_hash`, `query_parameterized_hash` and `credits_used_query_acceleration` itself, so no join to `QUERY_HISTORY` is needed.
```sql
select coalesce(nullif(query_tag, ''), 'untagged') as tag,
       sum(credits_attributed_compute) as credits
from snowflake.account_usage.query_attribution_history
where start_time >= dateadd(month, -1, current_date)
group by 1 order by 2 desc;
```
For users, join `TAG_REFERENCES` with `domain = 'USER'` on `object_name = user_name`.

What the per-query cost excludes: warehouse idle time, data transfer, storage, cloud services, serverless features and AI token costs. Queries of about 100 ms or less are too short and are not in the view. Latency is up to eight hours. Adaptive warehouse jobs are not in this view (use `QUERY_METERING_HISTORY`). Concurrent queries share warehouse cost by weighted resource consumption.

## Idle time
Allocate idle time proportionally: scale each owner's attributed credits by `sum(warehouse_metering credits_used_compute)` for the period divided by the total attributed credits (the page has worked CTE examples for users and for query tags).

## Stored procedures and repeat queries
Sum a procedure's cost via `root_query_id` (find it in `ACCESS_HISTORY`); find expensive recurring queries by grouping on `query_parameterized_hash`.

## Verify
- [ ] Untagged credits are small and tracked: query for users or warehouses with no tag.
- [ ] Per-owner totals including allocated idle time reconcile with warehouse metering for the period.
- [ ] Tags can be filtered in Snowsight: Admin, Cost management, Consumption, Tags drop-down.

## Checked
2026-11-09. Confirmed on the "Attributing cost" and QUERY_ATTRIBUTION_HISTORY pages: recommended approach, three scenarios, tag creation and replication, SCIM snowflakeTags, join keys and columns (credits_used_compute, warehouse_id/object_id), view columns, exclusions, 365 days, mid-August 2024, 8-hour latency, 100 ms threshold, adaptive warehouse note, root_query_id procedure, Snowsight path. Corrected the original join (it used warehouse_name and credits_used) and removed the QUERY_HISTORY join. Removed: the storage view names, serverless layer list, dbt/Airflow tag conventions, JSON query tag parsing, the 90% target and METERING_DAILY_HISTORY reconciliation, none of which the pages state.
Method: documentation only; no commands were run.
