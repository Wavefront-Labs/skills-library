---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.pipeline-hotspotting-and-work-distribution
name: pipeline-hotspotting-and-work-distribution
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [hotspotting, work-distribution-balancing, data-pipelines, data-skew, salting, dynamic-work-rebalancing, spark-aqe]
level: advanced
status: docs-checked
description: "Fix hotspots in data pipelines: skewed keys, hanging chunks and uneven work units, using dynamic work rebalancing, Spark adaptive skew-join handling and emergency skip switches."
sources: ["https://sre.google/workbook/data-processing/", "https://sre.google/sre-book/data-processing-pipelines/", "https://spark.apache.org/docs/latest/sql-performance-tuning.html", "https://docs.cloud.google.com/dataflow/docs/dynamic-work-rebalancing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotspotting and work distribution

Workbook: hotspotting happens when a resource becomes overloaded from excessive access, so operations fail
or are delayed in isolated regions of data. SRE Book: chunks often need uneven resources (for example data
partitioned by customer, where some customers are far larger); if the customer is the point of
indivisibility, end-to-end runtime is capped by the largest customer. A "hanging chunk" blocks the next
stage, because stages often wait for total completion.

## Workbook examples of hotspotting
- Many pipeline workers hitting a single serving task.
- CPU exhaustion from concurrent access to data held on one machine (its example: a Spanner tablet
  overloaded by a problematic section of data).
- Row-level lock contention in a database.
- Concurrent access to a hard drive beyond what the head can seek (it suggests solid state drives).
- A large work unit that needs many resources.

## Fixes the pages state
| Cause | Fix |
|---|---|
| Hotspot on a subset of data | block fine-grained data (individual records) so the rest of the pipeline progresses |
| Work chunk consuming disproportionate resources | the pipeline framework dynamically rebalances by splitting it into smaller pieces |
| Need to stop a problem input fast | build an emergency shutdown into client logic: a flag or pushed config that skips input matching a pattern or problematic user |
| Overloaded access pattern | restructure data or access patterns to spread load evenly; reduce load; reduce lock granularity |
| Skewed sort-merge join in Spark | adaptive query execution: `spark.sql.adaptive.enabled` with `spark.sql.adaptive.skewJoin.enabled` splits (and replicates if needed) skewed partitions |

Spark docs: AQE is enabled by default since Spark 3.2.0; a partition counts as skewed when larger than
`spark.sql.adaptive.skewJoin.skewedPartitionFactor` times the median partition size and also larger than
`spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes`.

Dataflow: Dynamic Work Rebalancing repartitions work when assignments are imbalanced, workers run slower
than expected, or workers finish faster than expected, assigning work to unused or underused workers. It
applies only where data is processed in parallel (source reads, materialised intermediate PCollections,
aggregation results such as GroupByKey), heavy fusion limits it, and it cannot split a single record: one
"hot" record can still delay the job. Custom sources must implement the hooks the page lists (for example
`splitAtFraction` in Java).

## Gotchas
- Killing and restarting a hanging chunk usually restarts all chunks from the beginning, because pipelines
  seldom checkpoint (SRE Book).
- Rebalancing cannot divide a single hot record; handle such records separately.

## Verify
- [ ] The largest work unit finishes well inside the pipeline's freshness target.
- [ ] A tested switch exists to skip a problematic input pattern.

## Checked
2026-11-01. Confirmed against the SRE Workbook data processing chapter (Reduce Hotspotting), the SRE Book
data processing pipelines chapter (uneven work distribution, hanging chunk), the Spark SQL performance
tuning page (AQE, skew join settings) and the Dataflow dynamic work rebalancing page. Removed: salting
recipe and SQL, `spark.speculation`, Kafka and Bigtable key advice, detection queries and tool claims, the
3x ratio threshold and the 1% dry-run reference, none of which those pages state.
Method: documentation only; no commands were run.
