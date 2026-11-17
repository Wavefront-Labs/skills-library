---
id: computing-software.data-engineering.apache-spark.runtime-bloom-filters
name: runtime-bloom-filters
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-sql, runtime-bloom-filter, runtime-filter, join-filter-pushdown, semi-join-reduction, spark-performance]
level: advanced
status: docs-checked
description: "Use Spark 3.3+ runtime bloom filters to shrink the large side of a shuffle join before the shuffle, with the thresholds that decide when Spark injects one."
sources:
  - https://issues.apache.org/jira/browse/SPARK-32268
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime bloom filters (join filter pushdown)

**Problem:** a sort-merge join between a huge fact table and a moderately large, filtered table (too big to broadcast) shuffles the whole fact table, even though most rows will not match.

**Runtime filter (SPARK-32268, added in Spark 3.3.0; `spark.sql.optimizer.runtime.bloomFilter.enabled` defaults to true in the current source):** Spark builds a bloom filter on the join keys of the selective side and applies it to the large side **before** its shuffle, so far fewer rows are shuffled. It is the non-partition-column cousin of dynamic partition pruning.

## Config
```properties
spark.sql.optimizer.runtime.bloomFilter.enabled=true                  # default true
spark.sql.optimizer.runtime.bloomFilter.creationSideThreshold=10MB    # default; estimated size of the creation-side plan must be under it
spark.sql.optimizer.runtime.bloomFilter.applicationSideScanSizeThreshold=10GB  # default; application-side scan must be over it
spark.sql.optimizer.runtime.bloomFilter.expectedNumItems=1000000      # default
spark.sql.optimizer.runtime.bloomFilter.maxNumBits=67108864          # default
spark.sql.optimizer.runtime.bloomFilter.numBits=8388608              # default
```
- Spark attempts the filter when one side of a **shuffle join** has a selective predicate (or is a fully materialized, repeatable cache with evidence that pruning helps); the bloom filter is inserted on the other side to reduce shuffle data.
- The estimated creation-side size must be under `creationSideThreshold` (unless that side is fully materialized with accurate statistics), so raising it lets the filter fire for bigger creation sides.
- The application side's aggregated scan size must exceed `applicationSideScanSizeThreshold`.

## Confirm in the plan
`explain("formatted")` should show a bloom-filter membership predicate on the large-side scan. In the SQL tab, compare the rows output by the large-side Filter with its scan rows.

## When it hurts
Low selectivity (most fact rows match anyway): building and probing the filter is wasted work. If a query regresses with a bloom-filter predicate in the plan, test with the flag off for that query.

## Verify
- [ ] Shuffle write bytes on the big side drop compared with the flag disabled.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in SQLConf.scala: bloomFilter.enabled (since 3.3.0, default true, shuffle join with a selective predicate on one side), creationSideThreshold 10MB, applicationSideScanSizeThreshold 10GB, expectedNumItems 1000000, maxNumBits 67108864, numBits 8388608. Wrong claim fixed: runtimeFilter.semiJoinReduction.enabled is a RemovedConfig since 4.0.0 (runtime filter can no longer be an IN subquery). Removed the unconfirmed '3.4 default' history and exact plan text.

Method: documentation only; no commands were run.
