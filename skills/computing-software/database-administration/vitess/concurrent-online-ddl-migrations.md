---
id: computing-software.database-administration.vitess.concurrent-online-ddl-migrations
name: concurrent-online-ddl-migrations
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, concurrent-migrations, allow-concurrent, scheduler, copy-phase, tailing-phase]
level: advanced
status: docs-checked
description: "Decide when to run Vitess migrations concurrently with --allow-concurrent: why sequential is default, phases, eligible types and scheduling limits."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/concurrent-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess schedules migrations sequentially by default. Long ALTERs copy large data and compete with production, and running several together usually raises resource competition and total wall-clock time. Opt in per migration with `--allow-concurrent`, for example `set @@ddl_strategy='vitess --allow-concurrent';` or `vtctldclient ApplySchema --ddl-strategy "vitess --allow-concurrent" --sql "REVERT VITESS_MIGRATION '<uuid>'"`.

A vitess ALTER has a copy phase (heavy, greedy but throttled) and a tailing phase (the binlog applied to the shadow table; load depends on traffic). Two concurrent copy phases interfere; concurrent tailing phases can be light. Vitess ensures only one copy phase runs at a time, while tail phases may run together up to a limit in the dozens, which pairs well with postponed migrations.

Scenarios the page supports:
- A CREATE or DROP while a long ALTER runs.
- An urgent revert of one or more migrations during another migration.
- Two vitess migrations overlapping as described.

Restrictions:
- `--allow-concurrent` must be supplied.
- Any CREATE, DROP or REVERT is eligible.
- At most one non-concurrent migration runs at a time, plus any number of concurrent ones.
- Never two migrations on the same table at once.

Scheduling: several migrations can be `ready`; the scheduler checks them one by one; they become `running` one at a time a few seconds apart; a migration blocked by a same-table runner does not block later migrations that have no conflict.

## Checked

2026-11-08. Read in full: Concurrent migration execution page (vitess.io docs 25.0, via the website repo markdown). Confirmed: sequential default and rationale, copy and tailing phases, eligible scenarios, the restrictions and scheduling notes. Fixed: the tail-phase limit is stated on the page only as 'some limit, in the dozens'.

Method: documentation only; no commands were run.
