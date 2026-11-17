---
id: computing-software.data-engineering.etl-pipeline-design.warehouse-migration-planning-and-parallel-run
name: warehouse-migration-planning-and-parallel-run
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-migration, warehouse-migration, parallel-run, cutover, inventory, wave-planning, decommission, rollback-plan]
level: advanced
status: draft
description: "Plan a warehouse migration: inventory and usage-based triage, wave planning, lift-and-shift vs refactor, parallel run with reconciliation gates, cutover and decommission."
sources:
  - https://cloud.google.com/bigquery/docs/migration/migration-overview
  - https://docs.snowflake.com/en/migrations/README
  - https://docs.databricks.com/aws/en/migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warehouse migration planning and parallel run

**Goal:** move pipelines, data and consumers from an old warehouse to a new one without a day when the numbers are wrong and nobody can go back.

## 1. Inventory from usage, not from memory
- Pull query history for 90 days (Snowflake `ACCOUNT_USAGE.QUERY_HISTORY`, BigQuery `INFORMATION_SCHEMA.JOBS`, Redshift `SYS_QUERY_HISTORY`, Teradata DBQL, SQL Server Query Store).
- Build a table: object, owner, readers (users/BI tools), last read, write job, query count.
- Triage: **unused 90 days → archive, don't migrate** (typically 30-50% of objects). Duplicates → consolidate. The rest is the real scope.
- Map lineage source → staging → mart → dashboard so waves move whole chains.

## 2. Choose approach per workload
| Approach | When | Risk |
|---|---|---|
| Lift-and-shift (translate SQL as-is) | many stable jobs, tight deadline | carries old debt over |
| Refactor (e.g. stored procs → dbt) | jobs being rewritten anyway | longer, harder to compare |
| Retire | unused or replaced | must confirm with owners |
Default: lift-and-shift first, refactor after cutover, so reconciliation compares like with like.

## 3. Wave plan
1. Foundation: networking, identity/SSO, RBAC model, landing zone, CI/CD, monitoring.
2. Historical data bulk load (see bulk-transfer skill); freeze format and partitioning.
3. Waves of 1 domain each (e.g. finance marts), smallest-but-real first as a pilot.
4. Each wave: translate → load history → dual-run ingestion → reconcile → switch consumers → freeze old.

## 4. Parallel run
- Feed both warehouses from the same sources for each wave (dual-write ingestion, or replicate old → new).
- Run reconciliation daily (counts, sums, checksums per partition) with a pass threshold agreed with the business owner — e.g. 100% row count, financial sums to the cent, 10 consecutive green days.
- Point a copy of each critical dashboard at the new warehouse; owners sign off side-by-side.
- Track compute cost in both — parallel run doubles spend; budget for it and time-box it (2-6 weeks per wave).

## 5. Cutover and rollback
- Cutover checklist: consumers repointed (BI connections, service accounts, extracts), old jobs disabled not deleted, old warehouse set read-only.
- Rollback plan: old warehouse stays loaded or loadable for N weeks; consumers can be repointed back by config.
- Decommission only after a full business cycle (month-end/quarter-end close) runs on the new platform.

## Verify
- [ ] Every migrated object has an owner sign-off and a reconciliation record.
- [ ] No consumer still queries the old warehouse (check its query history after cutover).
- [ ] A month-end close completed on the new platform before decommission.
