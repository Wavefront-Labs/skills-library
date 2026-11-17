---
id: computing-software.data-engineering.trino.trino-fault-tolerant-execution-task-tuning
name: trino-fault-tolerant-execution-task-tuning
category: computing-software
field: data-engineering
product: trino
tags: [task-sizing, node-allocation, fault-tolerant-execution-task-memory, partition-count, split-size]
level: sme
status: docs-checked
description: "Advanced FTE tuning for TASK retry policy in Trino: split and task target sizes, node memory allocation, partition counts and task descriptor memory."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/fault-tolerant-execution.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino fault tolerant execution task tuning

These properties apply only with `retry-policy=TASK` and are mainly for testing or troubleshooting; the defaults suit most deployments. Tasks that are too small waste effort on coordination; tasks too large may not fit on any node.

Task sizing:
- `fault-tolerant-execution-standard-split-size` (`64MB`): split data size per source-reading task, adjusted by split weight.
- `fault-tolerant-execution-max-task-split-count` (`2048`): hard cap on splits per task, guarding against wrong split weights.
- Arbitrary-distribution compute tasks start at `...compute-task-target-size-min` (`512MB`), grow by `...growth-factor` (`1.26`) every `...growth-period` (`64` tasks) up to `...target-size-max` (`50GB`).
- Writer tasks: min `4GB`, max `50GB`, same growth settings.
- Hash distribution: compute target `512MB`, write target `4GB`, soft maximum of `2000` writer tasks.

Node allocation: nodes are bin-packed using memory estimates. A task that fails by exceeding node memory restarts requesting a whole node. The initial estimate is `fault-tolerant-execution-task-memory` (`5GB`, session `fault_tolerant_execution_task_memory`).

Other tuning:
- `fault-tolerant-execution-task-descriptor-storage-max-memory`: coordinator memory for task descriptors, default JVM heap * 0.15.
- `fault-tolerant-execution-max-partition-count` (`50`; raising it is not recommended), `-min-partition-count` (`4`) and `-min-partition-count-for-write` (`50`) for joins and aggregations.
- `max-tasks-waiting-for-node-per-query` (`50`): pause scheduling more tasks once this many wait for a node.

## Checked

2026-11-04. Read against the Trino docs page `admin/fault-tolerant-execution.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
