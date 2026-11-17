---
id: computing-software.data-engineering.data-modelling.schema-deprecation-process
name: schema-deprecation-process
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-deprecation, change-management, data-contracts, communication]
level: advanced
status: draft
description: "Deprecate tables and columns without breaking consumers: usage discovery, announcement and timelines, compatibility views, deprecation metadata, and final removal."
sources:
  - https://docs.getdbt.com/docs/collaborate/govern/model-versions
  - https://docs.getdbt.com/reference/resource-properties/deprecation_date
  - https://docs.snowflake.com/en/user-guide/access-history
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schema deprecation and communication

**Goal:** remove or replace data assets on a predictable timeline, with every consumer migrated first.

## 1. Find consumers
- Warehouse access history (Snowflake `ACCESS_HISTORY`, BigQuery `INFORMATION_SCHEMA.JOBS` referenced tables, Databricks lineage tables) over 90 days: users, service accounts, query counts.
- BI tool metadata (dashboards using the table/column), dbt exposures, reverse ETL syncs, downstream dbt projects.

## 2. Announce
- Owner, what changes, replacement, reason, timeline (e.g. announce T, warnings T+2w, removal T+8w), migration guide with column mapping.
- Channels: data catalog banner, release notes, direct messages to top consumers found in step 1.

## 3. Mark it in metadata
```yaml
models:
  - name: dim_customer
    latest_version: 2
    deprecation_date: 2026-12-31
    versions:
      - v: 1
      - v: 2
```
dbt warns when anything refs a model past its deprecation date. Add comments/tags in the warehouse (`COMMENT ON TABLE ... IS 'DEPRECATED: use dim_customer_v2 by 2026-12-31'`).

## 4. Keep compatibility during the window
- Compatibility view with the old name/columns on top of the new model.
- For column renames: expose both names for the window.

## 5. Track and remove
- Weekly usage report of the old asset; contact remaining users.
- Brown-out (revoke access for an hour/day) before final removal to surface hidden consumers.
- Remove; keep a backup/clone for a period.

## Gotchas
- Service accounts shared by many jobs hide real consumers: map them to owners.
- Removing without a brown-out often finds a monthly finance job the day after month-end.

## Verify
Usage of the deprecated asset is zero for a full business cycle (including month-end) before removal.
