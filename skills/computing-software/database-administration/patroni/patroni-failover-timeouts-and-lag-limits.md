---
id: computing-software.database-administration.patroni.patroni-failover-timeouts-and-lag-limits
name: patroni-failover-timeouts-and-lag-limits
category: computing-software
field: database-administration
product: patroni
tags: [patroni, primary-start-timeout, maximum-lag, durability, failover]
level: practitioner
status: docs-checked
description: "Dynamic settings that bound failover speed and data loss: primary_start_timeout, primary_stop_timeout, maximum_lag_on_failover."
sources:
  - https://patroni.readthedocs.io/en/latest/dynamic_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: trade durability against availability using documented dynamic settings.

- `maximum_lag_on_failover`: maximum bytes a follower may lag and still participate in leader election (default shown in patronictl examples: 1048576).
- `primary_start_timeout`: how long a primary may recover from failure before failover is triggered. Default 300 seconds. At 0, failover happens immediately after a crash is detected if possible. Worst-case failover time for primary failure is `loop_wait + primary_start_timeout + loop_wait`, or just `loop_wait` when it is zero. With asynchronous replication a failover can lose transactions.
- `primary_stop_timeout`: seconds Patroni waits when stopping Postgres, effective only when `synchronous_mode` is enabled. If greater than 0, Patroni sends SIGKILL to the postmaster when stopping takes longer. If unset or <= 0 it does not apply.
- `max_timelines_history`: number of timeline history items kept in DCS. Default 0, which keeps the full history.
- `check_timeline`: when true, a node whose timeline differs from the former primary cannot become the new leader; by default Patroni ignores replica timelines in elections.

In asynchronous mode, lost data on failover is bounded in the worst case by `maximum_lag_on_failover` bytes plus what was written in the last `ttl` seconds (about `loop_wait/2` seconds on average), because the primary WAL position is not sampled in real time. Typical steady-state replication delay is well under a second.

## Checked

2026-11-03. Confirmed against Dynamic Configuration (maximum_lag_on_failover, primary_start_timeout, primary_stop_timeout, max_timelines_history, check_timeline) and the replication modes page for the failover-time arithmetic.

Method: documentation only; no commands were run.
