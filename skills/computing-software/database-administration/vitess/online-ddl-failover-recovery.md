---
id: computing-software.database-administration.vitess.online-ddl-failover-recovery
name: online-ddl-failover-recovery
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, recoverable-migrations, failover, reparent, vreplication, scheduler]
level: advanced
status: docs-checked
description: "How vitess-strategy migrations survive planned, emergency and external reparents: the 10 minute stale limit, scheduler takeover and 1-2 minute delay."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/recoverable-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Unlike gh-ost, pt-online-schema-change or plain direct DDL, which must finish on the server where they began, `vitess` strategy migrations are failover agnostic because VReplication persists transfer state transactionally with the data transfer. A migration may start on one primary tablet and finish on another.

It auto-survives a PlannedReparentShard, an EmergencyReparentShard and an unexpected external reparent, provided no more than 10 minutes pass between the failure or demotion of the old primary and the promotion of the new one. There is no limit on how many failovers a migration can survive.

Mechanics:
1. The VReplication stream is interrupted mid-copy or mid-apply.
2. Any replica holds a consistent migration state, even if it lags.
3. The promoted replica notices the stream that should be running and re-establishes connections; some retries happen as it re-evaluates its data source.
4. The Online DDL Scheduler detects the running stream as created by a different tablet, takes ownership, and follows it to completion.
5. If the stream is more than 10 minutes stale, the scheduler marks the migration failed.

No user action is needed. Right after promotion the migration will look stuck; expect progress within 1 or 2 minutes.

## Checked

2026-11-08. Read in full: Recoverable, failover agnostic migrations page (vitess.io docs 25.0, via the website repo markdown). Confirmed: failover scenarios, the 10 minute rule, no limit on failovers, scheduler ownership takeover and the 1 to 2 minute delay. Removed the exactly-once automatic retry sentence, which came from a page not cited or read.

Method: documentation only; no commands were run.
