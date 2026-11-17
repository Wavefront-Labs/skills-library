---
id: computing-software.data-engineering.trino.trino-query-execution-and-memory-policies
name: trino-query-execution-and-memory-policies
category: computing-software
field: data-engineering
product: trino
tags: [execution-policy, low-memory-killer, hash-partition-count, max-writer-task-count, remote-task]
level: advanced
status: docs-checked
description: "Trino query execution policy (phased vs all-at-once), partition counts, low-memory killer policies for queries and tasks, and adaptive remote task request sizing."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/properties-query-management.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino query execution and memory policies

Execution policy: `query.execution-policy` (default `phased`, session `execution_policy`). `phased` sequences stages to avoid inter-stage blockages, maximising utilisation and giving the lowest wall time. `all-at-once` starts all stages together; utilisation is initially high but dependencies cause longer queues and higher wall time.

Partitioning for distributed joins, aggregations and partitioned windows:
- `query.max-hash-partition-count` (default `100`, session `max_hash_partition_count`)
- `query.min-hash-partition-count` (default `4`)
- `query.min-hash-partition-count-for-write` (default `50`)
- `query.determine-partition-count-for-write-enabled` (default `false`): pick the write partition count from data read and processed.
- `query.max-writer-task-count` (default `100`): tasks writing in INSERT, CTAS and EXECUTE; applies only when `redistribute-writes` or `scale-writers` is enabled.

Low-memory killers:
- `query.low-memory-killer.policy` (default `total-reservation-on-blocked-nodes`): `none`, `total-reservation` (kill the biggest query) or `total-reservation-on-blocked-nodes` (biggest on nodes now out of memory). Applies when `retry-policy` is `NONE` or `QUERY`.
- `task.low-memory-killer.policy` (same default): `none`, `total-reservation-on-blocked-nodes`, or `least-waste`, which spares tasks that have run a long time. Applies only with `retry-policy=TASK`.

Adaptive remote task requests (advanced, for extremely large tables): `query.remote-task.enable-adaptive-request-size` (`true`) splits large task update requests to avoid out-of-memory errors; related `guaranteed-splits-per-task` (`3`), `max-request-size` (`8MB`), `request-size-headroom` (`2MB`).

`retry-policy` itself accepts `NONE`, `TASK` or `QUERY`.

## Checked

2026-11-04. Read against the Trino docs page `admin/properties-query-management.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
