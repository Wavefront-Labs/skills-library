---
id: computing-software.database-administration.vitess.vtgate-query-buffering
name: vtgate-query-buffering
category: computing-software
field: database-administration
product: vitess
tags: [buffering, vtgate, failover, plannedreparentshard, enable-buffer]
level: practitioner
status: docs-checked
description: "Configure VTGate query buffering to reduce errors during planned failovers and traffic switches, with the flags that size it and the errors seen when it is off or exhausted."
sources:
  - https://vitess.io/docs/25.0/reference/features/vtgate-buffering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTGate can buffer queries sent to a shard's `PRIMARY` while a planned operation is in flight, then drain them to the new primary. It was built to reduce, not eliminate, downtime during PlannedReparentShard (PRS), and also applies to MoveTables or Reshard SwitchTraffic and ReverseTraffic. It is not intended for unplanned failovers, and applications must still handle errors.

Flags on VTGate:
- `--enable-buffer` turns it on (off by default); `--enable-buffer-dry-run` only logs when buffering would trigger.
- `--buffer-implementation` defaults to `keyspace_events`; `healthcheck` is the legacy option.
- `--buffer-size` (default 1000) is the number of buffered requests; each paused request takes one slot and memory.
- `--buffer-drain-concurrency` (default 1): raise it proportionally for large buffers.
- `--buffer-keyspace-shards` limits buffering to chosen keyspaces.
- `--buffer-max-failover-duration` (default 20s): after this, stop buffering and return errors.
- `--buffer-window` (default 10s): maximum buffer time per request; keep it no larger than the failover duration.
- `--buffer-min-time-between-failovers` (default 1m): no new buffering if another failover starts sooner.

Only requests to `PRIMARY` tablets are buffered. Client `read_timeout`/`write_timeout` must exceed the buffer window or you see error 2013 "Lost connection to MySQL server during query". The most common error, 1105 "primary is not serving, there is a reparent operation in progress", means buffering is disabled, in dry-run, not configured for the keyspace, the buffer is full, a second event fell inside the minimum interval, or the max failover duration was exceeded.

## Checked

2026-11-04. Flags, defaults, scope (PRIMARY only, PRS and traffic switches) and the 2013/1105 error causes confirmed on the VTGate Buffering page.

Method: documentation only; no commands were run.
