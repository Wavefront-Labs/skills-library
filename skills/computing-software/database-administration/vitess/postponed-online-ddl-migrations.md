---
id: computing-software.database-administration.vitess.postponed-online-ddl-migrations
name: postponed-online-ddl-migrations
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, postpone-launch, postpone-completion, alter-vitess-migration, single-shard-experiment, cutover-control]
level: practitioner
status: docs-checked
description: "Delay an online migration's start or cut-over with --postpone-launch and --postpone-completion, then release it with ALTER VITESS_MIGRATION."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/postponed-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Normally migrations launch and complete automatically. Two flags give you control:

- `--postpone-launch`: the migration stays `queued` until you launch it (column `postpone_launch`). Supported for all migrations. Use it in multi-shard environments to try a migration on one shard first, to see how long it takes and its impact, while it stays queued elsewhere. Warning: finishing on a subset of shards leaves shards with different schemas, so do not add or remove columns that way; the page suggests it suits experimenting with (preferably non-unique) indexes.
- `--postpone-completion`: an ALTER in the vitess strategy still runs, copies data and tails changes, but stalls when cut-over would be acceptable (ready to complete) until you complete it. A declarative migration with this flag stays `queued` until completed.

Commands:

```sql
alter vitess_migration '9e8a9249_3976_11ed_9442_0a43f95f28a3' launch;
alter vitess_migration '9e8a9249_3976_11ed_9442_0a43f95f28a3' launch vitess_shards '-40,40-80';
alter vitess_migration launch all;
alter vitess_migration '<uuid>' complete;
alter vitess_migration complete all;
```

`vitess_shards` takes a comma-separated shard list; an empty list means all shards. The equivalents via client are `vtctldclient OnlineDDL launch commerce <uuid>`, `vtctldclient OnlineDDL launch commerce all` and `vtctldclient OnlineDDL complete commerce <uuid|all>`; the output shows `rows_affected_by_shard`.

Track state with `show vitess_migrations like '<uuid>'` (look at `migration_status` and `ready_to_complete`).

## Checked

2026-11-08. Read in full: Postponed migrations page (vitess.io docs 25.0, via the website repo markdown). Confirmed: both flags, the single-shard use case and schema-divergence warning, launch and complete statements, vitess_shards list, vtctldclient OnlineDDL launch and complete forms, and the declarative-migration note. Nothing removed.

Method: documentation only; no commands were run.
