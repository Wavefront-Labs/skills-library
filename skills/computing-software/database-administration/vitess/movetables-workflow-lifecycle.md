---
id: computing-software.database-administration.vitess.movetables-workflow-lifecycle
name: movetables-workflow-lifecycle
category: computing-software
field: database-administration
product: vitess
tags: [movetables, vreplication, switchtraffic, reversetraffic, cutover, workflow, vertical-sharding]
level: practitioner
status: docs-checked
description: "Run a MoveTables workflow end to end: create, status, VDiff, mirrortraffic, switchtraffic, reversetraffic, cancel and complete, with the caveats of each destructive step."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/movetables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MoveTables` moves tables from an external database or another Vitess keyspace into a Vitess keyspace (unsharded or sharded). Typical uses are adopting Vitess (point a vttablet at existing MySQL) and vertical sharding. Warning from the page: workflows can heavily load source tablets, especially a PRIMARY; limit it with the `--vreplication-copy-phase-max-*` vttablet flags.

Lifecycle:
1. `MoveTables --workflow <workflow> --target-keyspace <target-keyspace> create --source-keyspace <source-keyspace> --tables <tables>`
2. Monitor with `show` or `status` (status reports percent copied then lag, and current traffic state; copy percentages come from `information_schema` and can be off by 50-60%).
3. Verify with VDiff.
4. `switchtraffic` (replica, rdonly and primary can switch in any order; default is all). VTGate buffering can hide the impact.
5. `complete` to remove vreplication artifacts and, by default, drop source tables (destructive; `--keep-data` and `--rename-tables` change this).

Also: `mirrortraffic` (before switchtraffic; mirrors a percentage of traffic, and switchtraffic removes its mirror rules), `reversetraffic` (after a forward switch, for the same cells and tablet types), and `cancel` (only if no traffic was switched; removes artifacts and by default target tables).

SwitchTraffic on primary starts reverse replication by default (`--enable-reverse-replication=true`), in a workflow named `<workflow>_reverse`, which enables rollback. For `_reverse` workflows `--keep-data` defaults to true to protect the original source.

## Checked

2026-11-04. Lifecycle commands, action semantics, warnings and reverse-replication behaviour confirmed on the MoveTables reference page.

Method: documentation only; no commands were run.
