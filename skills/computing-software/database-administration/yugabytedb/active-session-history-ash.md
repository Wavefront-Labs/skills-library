---
id: computing-software.database-administration.yugabytedb.active-session-history-ash
name: active-session-history-ash
category: computing-software
field: database-administration
product: yugabytedb
tags: [ash, active-session-history, wait-events, yb-active-session-history, ysql-yb-enable-ash, query-id, performance]
level: advanced
status: docs-checked
description: "Use Active Session History in YSQL to see what sessions wait on: enable flags, sampling settings, the history and wait-event views, and background-work query ids."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/active-session-history-monitor.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Active Session History (ASH)

ASH samples active sessions and records their wait events so you can answer what the cluster was doing during an incident.

Flags (tserver):
- `ysql_yb_enable_ash` default true; a restart is needed to change it
- `ysql_yb_ash_circular_buffer_size` is the size in KiB of the circular buffer holding samples; the default depends on core count and a restart is needed to change it
- `ysql_yb_ash_sampling_interval_ms` default 1000; no restart needed
- `ysql_yb_ash_sample_size` default 500, the maximum samples taken per interval

Views:
- `yb_active_session_history` holds the samples. Columns include `wait_event_component` (YSQL, YCQL or TServer), `wait_event_class`, `wait_event`, `wait_event_type` (CPU, WaitOnCondition, RPCWait, Disk IO and so on), `wait_event_aux`, `top_level_node_id` and `query_id`.
- `yb_wait_event_desc` gives a description for each wait event code.

Group samples by `wait_event` or `query_id` to find the dominant wait. `query_id` joins to `pg_stat_statements`. For tserver events tied to a tablet, `wait_event_aux` holds only the first 15 characters of the tablet id, so join to `yb_local_tablets` on `SUBSTRING(tablet_id, 1, 15)`.

Background work is recorded under fixed query ids instead of a SQL statement; the page lists them under Constant query identifiers.

To map a sample to a node, join `top_level_node_id` to `yb_servers()`. Each node samples its own sessions; `gv$yb_active_session_history` (see the cluster-wide views skill) reads all nodes at once.

## Checked

2026-11-04. Confirmed against the Active Session History page: the four flags and defaults, restart requirements, view columns and wait_event_component values, wait_event_type examples, the 15-character tablet id in wait_event_aux, the query_id join to pg_stat_statements, and the constant query identifiers section. Removed the unsupported query id range and the closing tip.

Method: documentation only; no commands were run.
