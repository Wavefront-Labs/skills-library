---
id: computing-software.database-administration.clickhouse.too-many-parts-diagnosis
name: too-many-parts-diagnosis
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, too-many-parts, systemparts, small-inserts, batching]
level: practitioner
status: docs-checked
description: "Diagnose ClickHouse 'too many parts' errors by counting active parts per table in system.parts and judging part size."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/tips-and-tricks/too-many-parts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# too many parts diagnosis
ClickHouse throws a "Too many parts" error to prevent severe performance degradation. Many small parts cost query performance (more files read and merged), memory (each part needs metadata in memory), compression efficiency, I/O (more file handles and seeks) and give the background merge scheduler more work. Check part counts per table:
```sql
SELECT database, table, count() AS total_parts, sum(rows) AS total_rows,
       round(avg(rows), 0) AS avg_rows_per_part
FROM system.parts
WHERE active = 1
  AND database NOT IN ('system', 'information_schema')
GROUP BY database, table
ORDER BY total_parts DESC;
```
The guide's own traffic-light thresholds, to be adjusted for your system: over 100 parts is a caution, over 500 a warning, over 1000 critical. For part size it rates average rows per part below 1000 as poor, below 10000 fair, below 100000 good, and above that excellent.

The guide points to batching inserts and async inserts as the remedy (its linked talks cover async inserts and real-world batching strategies); see the insert-strategy skills for detail.

## Checked
2026-11-03. Confirmed against the "Lessons - too many parts problem" page: the error's purpose, the listed costs of small parts, the system.parts query shape, and the 100/500/1000 and 1000/10000/100000 thresholds. Removed: the ordered fix list (partition granularity, merge starvation), the part-limit-settings gotcha and the invented Verify step, none of which are on the page.
Method: documentation only; no commands were run.
