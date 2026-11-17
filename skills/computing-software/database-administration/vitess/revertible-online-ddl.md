---
id: computing-software.database-administration.vitess.revertible-online-ddl
name: revertible-online-ddl
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, revert, revertible-migrations, vitess-migration, rollback, table-lifecycle]
level: advanced
status: docs-checked
description: "Revert a completed Vitess online migration with REVERT VITESS_MIGRATION: what is revertible, the 24h limit, why reverts fail, and how they work."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/revertible-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Managed migrations offer lossless revert. Supported targets: `CREATE TABLE` (revert uncreates), `DROP TABLE` (revert reinstates the table with its data), `ALTER TABLE` in the `vitess` strategy only (reapplies the previous schema keeping data written since), and a previous revert, which can itself be reverted.

Syntax: `REVERT VITESS_MIGRATION '69b17887_8a62_11eb_badd_f875a4d24e90';` through vtgate, or `vtctldclient ApplySchema --ddl-strategy "vitess" --sql "revert vitess_migration '<uuid>'" commerce`. `vtctl OnlineDDL revert` is deprecated since Vitess 12. A revert is its own migration with its own UUID that you track.

Limits:
- Only within 24 hours of completion.
- Only the last successful migration on a given table can be reverted; several tables can be reverted at once.
- Only a migration in `complete` state; a failed migration gives "can only revert a migration in a 'complete' state".
- A no-op DDL (`CREATE TABLE IF NOT EXISTS` of an existing table, `DROP TABLE IF EXISTS` of a missing one) has a no-op revert.
- An ALTER revert can fail: widening `int` to `bigint` then inserting a larger value, or removing a UNIQUE KEY then inserting duplicates. Vitess cannot know in advance.

Implementation: reverting CREATE renames the table into a table-lifecycle name, so a second revert can restore it with data. Online DDL DROP only renames the table away, so its revert is a RENAME back. ALTER revert uses VReplication, copying the final GTID position of the original migration and applying only binlog changes for that table since cut-over, with no data copy, so it is efficient.

## Checked

2026-11-08. Read in full: Revertible migrations page (vitess.io docs 25.0, via the website repo markdown). Confirmed: supported statements, the 24h and last-successful-migration limits, no-op reverts, failing-ALTER examples, SQL and ApplySchema syntax, Vitess 12 deprecation of vtctl OnlineDDL revert, the complete-state error and the implementation notes. Nothing removed.

Method: documentation only; no commands were run.
