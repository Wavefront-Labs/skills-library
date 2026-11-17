---
id: computing-software.data-engineering.etl-pipeline-design.write-audit-publish
name: write-audit-publish
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, wap-pattern, write-audit-publish, iceberg-branching, zero-copy-clone, swap-tables, data-quality-gate, blue-green]
level: advanced
status: gated
description: "Implement write-audit-publish so consumers never see bad data: write to staging/branch, run checks, publish atomically via table swap, Iceberg branches, Delta clones or views."
sources:
  - https://iceberg.apache.org/docs/latest/branching/
  - https://docs.snowflake.com/en/sql-reference/sql/alter-table#swap-with
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Write-audit-publish (WAP)

**Goal:** a failed quality check means consumers keep yesterday's good data, instead of today's broken data plus an alert.

Not run here: Snowflake, Iceberg/Spark, Databricks and BigQuery have no runner in this environment, so every engine-specific statement below is unconfirmed (gated: unconfirmed, source is paywalled or blocked); the pattern itself (stage, audit, publish by atomic swap or repoint) is engine-neutral.

## The three steps
1. **Write** the new data somewhere consumers do not read.
2. **Audit**: run tests (row counts vs baseline, uniqueness, not-null, reconciliation, business rules).
3. **Publish** atomically only if audits pass; otherwise leave production untouched and alert.

## Implementations
**Snowflake: build + swap**
```sql
create or replace table analytics.fct_orders__staging clone analytics.fct_orders;  -- optional for incremental
-- build into __staging ...
-- audit queries on __staging ...
alter table analytics.fct_orders swap with analytics.fct_orders__staging;           -- atomic metadata swap
```
Grants: use `copy grants` on creation or grant via database roles/future grants so the swapped table keeps access.

**Iceberg: branches (Spark)**
```sql
ALTER TABLE db.orders CREATE BRANCH audit_20261017;
SET spark.wap.branch = audit_20261017;            -- writes go to the branch
INSERT INTO db.orders SELECT ...;
-- audit: SELECT ... FROM db.orders VERSION AS OF 'audit_20261017'
CALL catalog.system.fast_forward('db.orders', 'main', 'audit_20261017');   -- publish
ALTER TABLE db.orders DROP BRANCH audit_20261017;
```
(Table needs `write.wap.enabled=true` for the `spark.wap.id`/branch session mechanism.)

**Delta / Databricks**: write to a staging table (or shallow clone of prod), audit, then `INSERT OVERWRITE`/`MERGE` into prod in one transaction, or `CREATE OR REPLACE TABLE prod ... DEEP CLONE staging`. Lakeflow pipelines: expectations with `expect_or_fail` stop the update before publishing.

**BigQuery**: write to `orders_staging`, audit, then `CREATE OR REPLACE TABLE orders COPY orders_staging` or a table snapshot/clone; or swap a view definition.

**View pointer (any warehouse)**
```sql
create or replace view analytics.orders as select * from analytics.orders_v20261017;
```
Consumers query the view; publishing = repointing it. Keep N previous versions for instant rollback.

**dbt**: build into a CI/staging schema, run `dbt test`, then `dbt clone` or swap schemas (blue/green) into prod.

## Audits worth gating on
- Row count within +-X% of trailing average; not zero.
- Primary key unique, required columns not null.
- Totals reconcile with source control totals.
- No future dates / negative amounts beyond tolerance.
Warn-only checks should not block publishing; distinguish severity.

## Gotchas
- Swaps and view repoints are atomic, but downstream incremental models that already read the staging table can leak unaudited data: only publish targets should be read.
- Streaming tables cannot easily WAP; gate at the next batch layer.
- Storage doubles during the audit window; clean staging/branches after publish.

## Verify
- [ ] Inject a failing check in staging: prod table unchanged, alert fired.
- [ ] Rollback procedure (swap back / repoint view) tested.
