---
id: computing-software.data-engineering.apache-flink.mini-batch-and-two-phase-aggregation
name: mini-batch-and-two-phase-aggregation
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, mini-batch-aggregation, local-global-aggregation, split-distinct, data-skew, performance-tuning]
level: advanced
status: docs-checked
description: "Speed up Flink SQL streaming aggregations with mini-batch, local-global (two-phase) aggregation and split distinct aggregation, and their latency and state trade-offs."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/tuning/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mini-batch and two-phase aggregation tuning

MiniBatch is disabled by default for group aggregation, so the aggregation accesses state per input record. MiniBatch buffers input records to reduce state access.

## Mini-batch
Buffer input rows and process them per key in batches: one state access per key per batch.
```sql
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '2 s';   -- maximum buffering latency
SET 'table.exec.mini-batch.size' = '5000';           -- maximum number of buffered records
```
Trade-off: up to `allow-latency` added latency, in exchange for fewer state accesses. MiniBatch is triggered by the latency interval or when the record limit is reached, works only for non-windowed aggregations, and is always on for window TVF aggregations.

## Local-global (two-phase) aggregation
Requires mini-batch (the number of inputs accumulated per local aggregation is based on the mini-batch interval). It splits an aggregation into a local stage upstream and a global stage downstream, like Combine + Reduce, which targets data skew and reduces shuffle and state access.
```sql
SET 'table.optimizer.agg-phase-strategy' = 'TWO_PHASE';   -- AUTO (default) lets the optimizer choose by cost; TWO_PHASE forces local-global
```
Effective for general aggregates such as `SUM`, `COUNT`, `MAX`, `MIN`, `AVG`; UDAFs need `merge` for two-phase aggregation. Use `EXPLAIN` to confirm the plan.

## Split distinct aggregation
Local-global does little for distinct aggregation when the distinct key is sparse, because the accumulators still hold almost all raw records. Split distinct aggregation rewrites `COUNT(DISTINCT col)` into two levels: the first is shuffled by the group key plus a bucket key `HASH_CODE(distinct_key) % BUCKET_NUM`, the second sums the per-bucket counts:
```sql
SET 'table.optimizer.distinct-agg.split.enabled' = 'true';
SET 'table.optimizer.distinct-agg.split.bucket-num' = '1024';   -- default 1024
```
Use for skewed distinct counts. Prefer `COUNT(DISTINCT ...) FILTER (WHERE ...)` over `CASE WHEN` duplicates so several distinct aggregates share state.

## Related settings
- `table.exec.state.ttl` bounds state for unbounded GROUP BYs.
- `table.exec.sink.upsert-materialize` (default AUTO) adds an upsert-materialize operator before an upsert sink to restore global upsert order; check `EXPLAIN CHANGELOG_MODE`.
- MiniBatch optimization is always enabled for window TVF aggregations regardless of these options, so the settings mainly matter for non-windowed GROUP BY.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Performance Tuning page (MiniBatch, local-global, split distinct aggregation, FILTER modifier, window TVF always mini-batched) and the generated configuration tables (`table.exec.mini-batch.enabled` false, `allow-latency` 0 ms, `size` -1, `table.optimizer.agg-phase-strategy` AUTO/TWO_PHASE/ONE_PHASE, `distinct-agg.split.enabled` false, `bucket-num` 1024, `table.exec.sink.upsert-materialize` AUTO, `table.exec.state.ttl` 0 ms). Corrected the AUTO strategy description; removed unconfirmed plan node names and the checkpoint-flush claim.

Method: documentation only; no commands were run.

## Verify
- [ ] `EXPLAIN` shows the expected mini-batch and local/global aggregation nodes.
- [ ] Busy time and backpressure on the aggregate drop; output update rate drops; latency within the configured bound.
