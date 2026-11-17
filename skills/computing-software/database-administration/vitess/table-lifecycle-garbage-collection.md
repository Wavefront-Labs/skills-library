---
id: computing-software.database-administration.vitess.table-lifecycle-garbage-collection
name: table-lifecycle-garbage-collection
category: computing-software
field: database-administration
product: vitess
tags: [table-lifecycle, drop-table, table-gc-lifecycle, online-ddl, innodb, adaptive-hash-index]
level: advanced
status: docs-checked
description: "Configure Vitess table garbage collection (hold, purge, evac, drop) with --table-gc-lifecycle, understand fast drops on MySQL 8.0.23+, and decode the _vt_hld_ table-name hints."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/table-lifecycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A direct `DROP TABLE` on a busy server can lock it for seconds to minutes (buffer pool purge, removal of the `.ibd` file). Vitess replaces it with a lifecycle: in use, then `hold` (renamed away but intact and reinstatable), `purge` (rows deleted a few at a time with throttling and binary logging disabled, so not replicated), `evac` (hard-coded 72 hours for buffer pool pages to age out), `drop`, removed.

Configure with the vttablet flag `--table-gc-lifecycle`, default `"hold,purge,evac,drop"`. Any subset works (`"purge,drop"`, `"hold,drop"`, `"hold,evac,drop"`, `"drop"`); order is always hold, purge, evac, drop, and every subset ends in drop even if omitted.

MySQL 8.0.23 and later no longer lock the buffer pool on drop, but because of a MySQL bug this holds only with the Adaptive Hash Index disabled (AHI is on by default in 8.0, off by default in 8.4+). Vitess detects version and AHI and, when fast drops are supported, implicitly skips `purge` and `evac`. On 8.0 with AHI enabled the full lifecycle runs unless you removed stages.

The process is stateless; the state is encoded in table names, for example `_vt_hld_<uuid>_20210915120000_` (held until that time), `_vt_prg_...` (being purged), `_vt_evc_...` (evacuating until a time), `_vt_drp_...` (eligible to drop at a time).

Online DDL uses this for its artifact and leftover tables, which move to `hold` immediately. With an online ddl_strategy a user `DROP TABLE` becomes a `RENAME TABLE` into a hold name; a multi-table DROP is split into single-table renames.

## Checked

2026-11-04. Lifecycle stages, flag default, version-aware skipping, naming hints and Online DDL integration confirmed on the Table Lifecycle page.

Method: documentation only; no commands were run.
