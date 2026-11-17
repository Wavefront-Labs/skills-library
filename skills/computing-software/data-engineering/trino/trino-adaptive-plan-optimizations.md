---
id: computing-software.data-engineering.trino.trino-adaptive-plan-optimizations
name: trino-adaptive-plan-optimizations
category: computing-software
field: data-engineering
product: trino
tags: [adaptive-plan-optimizations, adaptive-join-reordering, fault-tolerant-execution-adaptive-query-planning-enabled, runtime-statistics]
level: advanced
status: docs-checked
description: "Trino adaptive plan optimizations that reorder partitioned joins from runtime sizes, available only with fault-tolerant execution, and how to turn them off."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/adaptive-plan-optimizations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino adaptive plan optimizations

Adaptive plan optimizations change a query's execution plan while it runs, using runtime statistics. They are available only when fault-tolerant execution is enabled.

Master switch: set `fault-tolerant-execution-adaptive-query-planning-enabled` to `false` to deactivate all of them. The session equivalent is `fault_tolerant_execution_adaptive_query_planning_enabled`.

Adaptive reordering of partitioned joins is enabled by default. Trino dynamically reorders the join inputs based on the actual size of the build and probe sides observed during execution. This is most useful when table statistics are not available beforehand, because the engine can still make efficient join-order decisions from runtime information instead of estimates.

To deactivate only this optimisation, set `fault-tolerant-execution-adaptive-join-reordering-enabled` to `false`; the session property is `fault_tolerant_execution_adaptive_join_reordering_enabled`.

The page does not say how to enable fault-tolerant execution; it only links to the fault-tolerant execution documentation.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Removed an unsupported retry-policy aside and practical notes; rest matches the page.
