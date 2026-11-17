---
id: computing-software.database-administration.vitess.ddl-strategy-flags-reference
name: ddl-strategy-flags-reference
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, ddl-strategy, cut-over-threshold, force-cut-over-after, singleton, in-order-completion, prefer-instant-ddl]
level: advanced
status: docs-checked
description: "Reference for ddl_strategy flags: allow-concurrent, cut-over-threshold range, force-cut-over-after, in-order-completion, postpone flags, prefer-instant-ddl and singleton."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/ddl-strategy-flags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ddl_strategy` takes command-line style flags; unrecognised ones are passed to the underlying tools. Combine them freely unless noted.

- `--allow-concurrent`: do not queue sequentially (restrictions apply).
- `--allow-zero-in-date`: permit zero dates in the schema despite strict `sql_mode`.
- `--analyze-table`: run `ANALYZE NO_WRITE_TO_BINLOG TABLE` before an ALTER in the vitess strategy for better row estimates.
- `--cut-over-threshold=<duration>`: default `10s`, allowed `5s..30s` (outside the range errors; `0` resets to the default). The migration will not cut over if vstream or replication lag exceeds it, and table locks time out at the same value. Override later with `ALTER VITESS_MIGRATION '...' CUTOVER_THRESHOLD '...'`.
- `--declarative`: supply desired CREATE or DROP state.
- `--fast-range-rotation`: run a single ADD or DROP PARTITION directly on MySQL (not revertible).
- `--force-cut-over-after=<duration>`: vitess ALTER on MySQL 8.0; after that long since the first cut-over attempt, `KILL` queries and transactions using the table. Must exceed zero; 1ms or less means from the first attempt. Also applies before `ALGORITHM=INSTANT`.
- `--in-order-completion`: complete only after earlier pending migrations in the same migration context; a failure or cancel marks later ones failed; `in_order_completion_pending_count` shows blockers.
- `--postpone-completion`, `--postpone-launch`.
- `--prefer-instant-ddl`.
- `--retain-artifacts=<duration>`: overrides `vttablet --retain-online-ddl-tables`.
- `--singleton`, `--singleton-context`, `--singleton-table`: reject new submissions while a matching one is pending; do not combine the first two.

`--vreplication-test-suite` is for internal CI and must not be used in production.

## Checked

2026-11-04. Each flag, default and range confirmed on the DDL Strategy Flags page.

Method: documentation only; no commands were run.
