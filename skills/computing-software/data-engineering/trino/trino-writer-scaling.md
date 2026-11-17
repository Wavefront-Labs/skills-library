---
id: computing-software.data-engineering.trino.trino-writer-scaling
name: trino-writer-scaling
category: computing-software
field: data-engineering
product: trino
tags: [writer-scaling, scale-writers, task-scale-writers, writer-scaling-min-data-processed]
level: advanced
status: docs-checked
description: "Reduce small files on writes by letting Trino add writer tasks only when a query is bottlenecked on writing; the four properties and defaults."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/properties-writer-scaling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino writer scaling

Writer scaling lets Trino dynamically scale the number of writer tasks instead of allocating a fixed number. New writers are added when the average physical data per writer is above a minimum threshold, and only if the query is bottlenecked on writing. It helps connectors like Hive that produce one or more files per writer: fewer writers means larger average files. The cost is a small hit on wall time while writer count ramps up.

Properties:
- `scale-writers` (boolean, default `true`, session `scale_writers`): scale out writer tasks across the cluster.
- `task.scale-writers.enabled` (boolean, default `true`, session `task_scale_writers_enabled`): scale concurrent writers within a task, up to the task max writer count. Writers are added only when average uncompressed data per writer exceeds `writer-scaling-min-data-processed` and the query is bottlenecked on writing.
- `task.scale-writers.max-writer-memory-percentage` (double, default `70`, session `task_scale_writers_max_writer_memory_percentage`): percentage of node memory concurrent writers may use before scaling pauses, to prevent out-of-memory errors. Must be between 0.0 and 100.0.
- `writer-scaling-min-data-processed` (data size, default `120MB`, session `writer_scaling_min_data_processed`): minimum uncompressed data a writer must process before another writer is added.

## Checked

2026-11-04. Read against the Trino docs page `admin/properties-writer-scaling.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
