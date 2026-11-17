---
id: computing-software.data-engineering.trino.trino-resource-group-limits-scheduling
name: trino-resource-group-limits-scheduling
category: computing-software
field: data-engineering
product: trino
tags: [resource-group-properties, scheduling-policy, scheduling-weight, hard-concurrency-limit, soft-memory-limit]
level: advanced
status: docs-checked
description: "The resource group limits Trino supports (concurrency, memory, CPU, scan) and how fair, weighted_fair, weighted and query_priority scheduling pick the next query."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/resource-groups.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino resource group limits scheduling

Each resource group has these properties:
- `name` (required; may be a template such as `pipeline_${USER}`), `maxQueued` (required; new queries are rejected beyond it) and `hardConcurrencyLimit` (required; maximum running queries).
- `softConcurrencyLimit`: above this, new queries run only if all peer groups below their soft limits are ineligible or all eligible peers are above theirs.
- `softMemoryLimit`: distributed memory before new queries queue; absolute (`1GB`) or a percentage (`10%`) of cluster memory.
- `softCpuLimit` with `hardCpuLimit`: CPU time per `cpuQuotaPeriod`; passing the soft limit applies a penalty to the running-query maximum.
- `hardPhysicalDataScanLimit`: absolute data scanned per period before queries queue; period set by the global `physicalDataScanQuotaPeriod`.
- `jmxExport` (default `false`) exports group statistics to JMX; `subGroups` lists children.

`schedulingPolicy` controls which queued query or sub-group goes next:
- `fair` (default): FIFO, with sub-groups taking turns.
- `weighted_fair`: pick the sub-group with the least concurrency relative to its share computed from `schedulingWeight` (default `1`).
- `weighted`: queued queries chosen stochastically in proportion to the `query_priority` session property; sub-groups in proportion to `schedulingWeight`.
- `query_priority`: strictly by query priority; every sub-group must also use `query_priority`.

Weight example: pipeline sub-group `350` versus adhoc `150` gives roughly 70% and 30% of queries; both set to `1` splits 50/50.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
