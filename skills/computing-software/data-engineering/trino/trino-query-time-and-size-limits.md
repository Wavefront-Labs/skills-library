---
id: computing-software.data-engineering.trino.trino-query-time-and-size-limits
name: trino-query-time-and-size-limits
category: computing-software
field: data-engineering
product: trino
tags: [query-max-execution-time, query-max-run-time, query-max-planning-time, query-max-length, query-limits]
level: practitioner
status: docs-checked
description: "The Trino query management limits on runtime, planning time, text length, plan nodes, stages, scan and write bytes, and what errors they raise."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/properties-query-management.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino query time and size limits

These coordinator properties cap how much a single query may consume. Most have a session property too.

Time limits:
- `query.max-execution-time` (default `100d`, session `query_max_execution_time`): active execution only, excluding analysis, planning and queue time.
- `query.max-run-time` (default `100d`, `query_max_run_time`): total lifetime since creation, including planning and queueing.
- `query.max-planning-time` (default `10m`, `query_max_planning_time`): best-effort stop; some planning steps cannot be cancelled at once.
- `query.client.timeout` (default `5m`): abandon a query when the client such as the CLI is silent this long.
- `query.remote-task.max-error-duration` (default `1m`): a remote task silent this long is treated as failed.

Size limits:
- `query.max-length` (default `1,000,000`, max `1,000,000,000`): longer text fails with `QUERY_TEXT_TOO_LARGE`.
- `query.max-initial-plan-nodes` (default `100000`): every view or `WITH` reference expands into its own plan copy, so repeated nested views can grow exponentially and exhaust coordinator memory; exceeding the limit gives `QUERY_PLAN_TOO_LARGE`.
- `query.max-stage-count` (default `150`): error `QUERY_HAS_TOO_MANY_STAGES`; a high value can destabilise the cluster and kill unrelated queries with `REMOTE_TASK_ERROR`.
- `query.max-scan-physical-bytes`, `query.max-write-physical-size`, `query.max-output-data-size`: no default; the query is terminated when exceeded.

History: `query.max-history` (default `100`) and `query.min-expire-age` (default `15m`) govern what the Web UI can show; use an event listener to keep more. `query.info-url-template` redirects clients to another query page and must contain `${QUERY_ID}`.

## Checked

2026-11-04. Read against the Trino docs page `admin/properties-query-management.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
