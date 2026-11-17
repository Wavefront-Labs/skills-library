---
id: computing-software.data-engineering.databricks.shallow-and-deep-clone
name: shallow-and-deep-clone
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-lake, deep-clone, shallow-clone, table-clone, incremental-clone, backup, test-environments]
level: practitioner
status: docs-checked
description: "Use Delta SHALLOW and DEEP CLONE for test copies, backups, migrations and incremental replication, with their dependency on source files, VACUUM and Unity Catalog rules."
sources:
  - https://docs.databricks.com/en/delta/clone.html
  - https://docs.databricks.com/en/delta/clone-unity-catalog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SHALLOW and DEEP CLONE

**Goal:** copy Delta tables cheaply for dev/test or durably for backup/migration, knowing what each clone depends on.

## Syntax
```sql
CREATE OR REPLACE TABLE dev.sales.orders SHALLOW CLONE prod.sales.orders;
CREATE OR REPLACE TABLE backup.sales.orders DEEP CLONE prod.sales.orders;
CREATE TABLE dev.sales.orders_oct SHALLOW CLONE prod.sales.orders VERSION AS OF 412;
CREATE TABLE dev.sales.orders_ts DEEP CLONE prod.sales.orders TIMESTAMP AS OF '2026-10-17 06:00';
```

## Differences
| | Shallow | Deep |
|---|---|---|
| Copies data files | no (references source files) | yes |
| Creation cost | metadata only, seconds | full copy |
| Independent of source | no: source VACUUM can delete referenced files -> clone breaks (`FileNotFoundException`) | yes |
| Writes to clone | new files in clone location, source untouched | same |
| Copies table properties, constraints, CDF settings | yes | yes |
| Copies stream checkpoints / history | no (clone history starts fresh) | no |

## Incremental deep clone
Re-running `CREATE OR REPLACE TABLE backup DEEP CLONE source` copies only files added since the last clone (and records removals). Cheap periodic backup/replication to another region or storage account:
```sql
CREATE OR REPLACE TABLE dr.sales.orders DEEP CLONE prod.sales.orders;   -- schedule daily
```
Restore by deep cloning back, or `RESTORE` if within Time Travel.

## Use cases
- **Test against prod data:** shallow clone into a dev schema, run the job, compare, drop. Keep source VACUUM retention longer than the test lifetime.
- **ML/experiment snapshot:** deep clone at a version for reproducibility.
- **Migration:** deep clone from Hive metastore table to UC (`CREATE TABLE main.s.t DEEP CLONE hive_metastore.s.t`), or between storage locations.
- **Schema change rehearsal:** shallow clone, apply ALTERs, run downstream tests.

## Unity Catalog rules
- Shallow clones of UC managed tables must be managed tables in UC (same metastore); reading requires access to the source too.
- Cross-workspace/metastore: use deep clone or Delta Sharing.

## Gotchas
- `CREATE OR REPLACE ... SHALLOW CLONE` on an existing clone resets it to the source; local changes lost.
- Dropping a managed shallow clone does not affect the source; dropping the source (and purge after UC retention) breaks shallow clones.

## Verify
- [ ] `DESCRIBE HISTORY clone` shows `CLONE` with expected source version.
- [ ] Shallow clone read works after a scheduled VACUUM on the source (retention not too short).

## Checked

2026-10-28. Confirmed: clone syntax and unity-catalog clone rules on the clone pages. Removed: unconfirmed metric names and a grants claim.

Method: documentation only; no commands were run.
