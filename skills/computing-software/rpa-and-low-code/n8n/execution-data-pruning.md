---
id: computing-software.rpa-and-low-code.n8n.execution-data-pruning
name: execution-data-pruning
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, execution-data, pruning, sqlite-vacuum, database-size, save-settings]
level: practitioner
status: docs-checked
description: "Keep the n8n database from filling up: choose which executions to save, enable pruning by age or count, know what is never pruned and reclaim SQLite space."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/manage-execution-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop execution history exhausting storage. The same options can be set per workflow in workflow settings.

## Save less
```sh
export EXECUTIONS_DATA_SAVE_ON_ERROR=all
export EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
export EXECUTIONS_DATA_SAVE_ON_PROGRESS=false
export EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=false
```
In Docker pass each with `-e`; in Compose list them under the n8n service `environment`.

## Pruning
On by default. It first marks executions for deletion and removes them permanently later. An execution is pruned when either:
- it finished more than `EXECUTIONS_DATA_MAX_AGE` hours ago (default 336 = 14 days), or
- the total exceeds `EXECUTIONS_DATA_PRUNE_MAX_COUNT` (default 10,000), deleting oldest first. It may not prune back down to exactly the max; 0 means unlimited.
```sh
export EXECUTIONS_DATA_PRUNE=true
export EXECUTIONS_DATA_MAX_AGE=168
export EXECUTIONS_DATA_PRUNE_MAX_COUNT=50000
```
Never pruned: executions in `new`, `running` or `waiting` status, and annotated executions (tags or ratings). A safety buffer `EXECUTIONS_DATA_HARD_DELETE_BUFFER` (1 h) keeps recent data available while building a workflow.

## SQLite gotcha
Pruned space on SQLite is reused, not returned to the disk. Set `DB_SQLITE_VACUUM_ON_STARTUP` or run SQLite `VACUUM` manually to shrink the file.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/manage-execution-data

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
