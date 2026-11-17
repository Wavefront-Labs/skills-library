---
id: computing-software.data-engineering.trino.trino-table-statistics
name: trino-table-statistics
category: computing-software
field: data-engineering
product: trino
tags: [table-statistics, analyze, show-stats, row-count, distinct-value-count]
level: practitioner
status: docs-checked
description: "Which table and column statistics Trino's planner uses, how to see them with SHOW STATS and refresh them with ANALYZE."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/statistics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino table statistics

Statistics-based optimisations need statistical information about the tables in a query. Connectors provide these estimates to the planner.

Available statistics:
- Per table: row count.
- Per column: data size (what must be read), nulls fraction, distinct value count, low value and high value.

Which ones exist depends on the connector and can vary by table; for example, the Hive connector does not currently provide data size statistics.

View them with `SHOW STATS`. Depending on the connector, Trino updates statistics while executing data management statements such as `INSERT`, `UPDATE` or `DELETE`; the Delta Lake, Hive and Iceberg connectors all support statistics management from Trino.

Run `ANALYZE` to initialise statistics collection. It is needed when other systems change the data without Trino, so the tracked statistics are stale. Other connectors rely on the underlying data source to maintain statistics, or do not support statistics at all.

The statistics page itself says only that statistics-based optimisations need them; it does not list which optimisations or claim effects of stale data.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Removed an unsupported closing claim about stale statistics; rest unchanged.
