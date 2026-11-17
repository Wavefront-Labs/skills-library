---
id: computing-software.database-administration.vitess.vtorc-ui-api-and-metrics
name: vtorc-ui-api-and-metrics
category: computing-software
field: database-administration
product: vitess
tags: [vtorc, api, metrics, debug-status, errant-gtid, disable-global-recoveries]
level: practitioner
status: docs-checked
description: "Use VTOrc's /debug/status UI, HTTP APIs (problems, errant-gtids, global recovery toggles) and exported metrics to monitor and pause recovery."
sources:
  - https://vitess.io/docs/25.0/reference/vtorc/ui_api_metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTOrc's UI needs the `--port` flag; `/debug/status` then lists recent recoveries.

APIs:
- `/api/problems`: instances with problems (replication not running through errant GTIDs), filterable by keyspace and shard.
- `/api/disable-global-recoveries` and `/api/enable-global-recoveries`: stop or resume all repairs VTOrc would make.
- `/debug/health` and `/debug/liveness`: process health and liveness.
- `/api/detection-analysis`: JSON detection analysis.
- `/api/errant-gtids`: JSON tablets with errant GTIDs, filterable by keyspace and shard.
- `/api/database-state`: VTOrc's internal database state, for debugging VTOrc.
- `/api/shard-tablet-health-quorum`: read-only live per-shard quorum state for quorum-confirmed emergency reparenting.

Metrics on `/debug/vars`:
- `PendingRecoveries`: recoveries in progress.
- `RecoveriesCount`, `SuccessfulRecoveries`, `FailedRecoveries`: subdivided by recovery type.
- `ErrantGtidTabletCount`: tablets with errant GTIDs.
- `DetectedProblems`: binary gauge of active problems by TabletAlias, Keyspace and Shard.
- `planned_reparent_counts`, `emergency_reparent_counts`: by keyspace, shard and result.
- `reparent_shard_operation_timings`: timings by operation type.

The page asks for feature requests in the #feat-vtorc Slack channel.

## Checked

2026-11-08. Read in full: VTOrc UI, API and Metrics page (vitess.io docs 25.0, via the website repo markdown). Confirmed: the --port requirement, /debug/status, every listed API and metric with its description, and the feature-request channel. Removed: the 'useful before manual maintenance' remark and the alerting suggestion, which the page does not state.

Method: documentation only; no commands were run.
