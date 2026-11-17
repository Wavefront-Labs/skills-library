---
id: computing-software.database-administration.vitess.online-ddl-strategies
name: online-ddl-strategies
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, ddl-strategy, vitess-strategy, applyschema, schema-changes, vreplication]
level: practitioner
status: docs-checked
description: "Pick and set a Vitess DDL strategy (vitess, mysql, direct): where to set ddl_strategy, what vitess provides, the comparison table, gh-ost and pt-osc unsupported."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/ddl-strategies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess runs schema changes in one of three strategies:
- `vitess` (formerly `online`): built on VReplication; the preferred strategy.
- `mysql`: scheduled by the Online DDL scheduler but run as a normal MySQL statement, so blocking depends on the statement.
- `direct`: unmanaged direct apply.
The page states `gh-ost` and `pt-osc` strategies are not supported as of v22.

Set the strategy per command with `vtctldclient ApplySchema --ddl-strategy "vitess" --sql "ALTER TABLE demo MODIFY id bigint UNSIGNED; ..." commerce` (returns a migration UUID per statement), globally with `vtgate --ddl-strategy="vitess"`, or per session with `set @@ddl_strategy="vitess --postpone-completion --allow-concurrent";` which overrides the VTGate flag.

The `vitess` strategy: integrates with the throttler; is visible via VReplication status; resumes after planned or unplanned failovers; is revertible; handles different keys pre and post migration (so a PRIMARY KEY can change without an extra unique key, unlike gh-ost); backs off cut-over retries up to 30 minutes apart; supports forced cut-over; supports INSTANT DDL where applicable (no shadow table, not revertible); runs RANGE partition ADD and DROP directly on MySQL; cuts over atomically with brief query blocking plus a buffering layer; supports foreign keys only on a custom MySQL build with experimental `--unsafe-allow-foreign-keys`.

Comparison: managed - vitess yes, mysql yes, direct no. Declarative - vitess and mysql yes. Revertible - vitess for CREATE, DROP and ALTER; managed strategies for CREATE and DROP. Recoverable and backoff - vitess only. Trackable (state, plus progress percent and ETA for vitess) - vitess and mysql. Plain MySQL `INPLACE` is non-blocking on the primary but serialised on replicas, causing lag.

## Checked

2026-11-04. Strategy list, ways to set it, vitess strategy features and the comparison table confirmed on the DDL Strategies page.

Method: documentation only; no commands were run.
