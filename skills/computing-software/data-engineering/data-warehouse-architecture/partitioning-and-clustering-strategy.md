---
id: computing-software.data-engineering.data-warehouse-architecture.partitioning-and-clustering-strategy
name: partitioning-and-clustering-strategy
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, partitioning, clustering, partition-pruning, bigquery, snowflake, databricks, delta-lake, z-order, liquid-clustering, partition-key-design, small-file-problem, cost-control]
level: practitioner
status: docs-checked
description: "Partition and cluster warehouse tables correctly for prune-friendly queries and cost control, across Snowflake/BigQuery/Databricks."
sources:
  - https://cloud.google.com/bigquery/docs/partitioned-tables
  - https://cloud.google.com/bigquery/quotas
  - https://cloud.google.com/bigquery/docs/clustered-tables
  - https://docs.snowflake.com/en/user-guide/table-considerations
  - https://docs.snowflake.com/en/user-guide/tables-clustering-keys
  - https://docs.databricks.com/aws/en/delta/clustering
  - https://docs.databricks.com/aws/en/delta/optimize
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Partitioning and clustering — the one change that controls your bill

**Goal:** make the warehouse scan only the bytes a query needs, because in every major cloud warehouse, cost and latency scale with bytes scanned, not rows returned.

## 1. Partition key choice — the decision that's hardest to undo
Pick the column(s) most queries filter on, almost always a date/timestamp for time-series fact tables. The failure mode isn't picking a bad key — it's picking one with the wrong **cardinality**: too few partitions (a single `year` partition on a 5-year table) means pruning barely helps; too many means metadata overhead and tiny partitions dominate (and on Delta, the small-file problem below). BigQuery documents hard limits: each partitioned table can have up to 10,000 partitions (if you exceed that, consider clustering in addition to or instead of partitioning), and a single query or load job can modify at most 4,000 partitions, so a large backfill across many daily partitions must be split into several jobs. Check the current BigQuery quotas page before choosing a grain.
- Changing a table's partition key after the fact usually means a rebuild (CTAS/rewrite) on most engines. Get this right before the table is load-bearing, or budget for a planned migration. (Databricks liquid clustering can be enabled on an existing unpartitioned table; it is not compatible with partitioning or ZORDER, and a partitioned Delta table converts with `ALTER TABLE ... REPLACE PARTITIONED BY WITH CLUSTER BY` on Databricks Runtime 18.1 and above.)

## 2. Partition pruning only works when the query plan can prove it
A filter on the literal partition column (`WHERE order_date = '2026-01-01'`) is the form to aim for. A filter that wraps the partition column in a function or cast may not prune, so verify with the query plan or the warehouse's query profile (bytes scanned vs. table size) that pruning actually happened; don't assume a logically-correct filter prunes.
- Filtering a large fact table's partitions based on a small dimension table's values at join time is engine-specific; check whether your engine prunes this way before relying on it like a WHERE clause.

## 3. Clustering — the second-order fix for columns that aren't the partition key
- **Snowflake**: a clustering key reorganizes micro-partitions; after you define one, rows are not necessarily updated immediately, and Snowflake performs automated maintenance (Automatic Clustering) only if the table would benefit. Snowflake's guidance is that clustering is best for tables that hold a large number of micro-partitions (typically multiple terabytes), where queries are selective or sort on the key, and where most queries share the same few key columns. Small or medium tables rarely need explicit clustering keys; check the Automatic Clustering cost documentation before applying it.
- **BigQuery**: clustering takes up to four clustering columns and sorts data within each partition. BigQuery performs automatic reclustering in the background as data is added, and it is among the free operations (no effect on query capacity). If you alter an existing non-clustered table to be clustered, existing data is not automatically clustered. STRING clustering columns use only the first 1,024 characters.
- **Databricks/Delta**: `OPTIMIZE` compacts files, and on tables without liquid clustering can take a `ZORDER BY` clause. Databricks recommends liquid clustering (`CLUSTER BY`) instead of partitions, ZORDER or other layout approaches for new tables, and says it replaces partitioning and ZORDER; `OPTIMIZE` then incrementally clusters the data. Check the runtime requirements for your Databricks Runtime version.

## 4. The small-file problem
Over-partitioning (too fine a grain, or partitioning by a high-cardinality column) combined with frequent small incremental loads produces many tiny files per partition, which can hurt scan performance. On Delta, `OPTIMIZE` rewrites data files to improve layout (file compaction happens within partitions on partitioned tables), and Databricks also offers auto compaction for small files. Size partitions so each one holds a reasonable number of reasonably-sized files, not one partition per load.

## Verify
- [ ] The partition key matches what the majority of production queries actually filter on (checked against real query logs, not assumed).
- [ ] `EXPLAIN`/query profile confirms pruning is active on the most common query pattern — no function-wrapped predicate defeating it.
- [ ] Partition count is checked against the warehouse's documented limits before the table grows into the problem.
- [ ] A compaction/optimize job runs on a schedule matching the table's ingestion frequency — not left to accumulate small files indefinitely.

## Checked
Date: 2026-11-09. Confirmed from the BigQuery quotas and clustered-tables pages (10,000 partitions per table, 4,000 per job, four clustering columns, automatic reclustering, 1,024-character STRING limit), the Snowflake clustering-keys page (multi-TB guidance, maintenance only if the table benefits, credits consumed) and the Databricks clustering and OPTIMIZE pages (liquid clustering recommendation, ZORDER on non-clustered Delta tables, REPLACE PARTITIONED BY on Runtime 18.1+). The BigQuery partitioned-tables page was not re-read for the grain-specific claims; the earlier claims about the 4,000-partition limit implying year or month ranges, Snowflake credit comparisons, dynamic partition pruning and function-wrapped predicates were removed or made generic.
Method: documentation only; no commands were run.
