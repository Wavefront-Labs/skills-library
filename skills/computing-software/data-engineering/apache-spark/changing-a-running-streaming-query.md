---
id: computing-software.data-engineering.apache-spark.changing-a-running-streaming-query
name: changing-a-running-streaming-query
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, structured-streaming, streaming-query-changes, checkpoint-compatibility, state-schema, query-upgrade, restart-semantics]
level: advanced
status: docs-checked
description: "Know which code changes a Structured Streaming query survives on restart from the same checkpoint (sources, sinks, projections, stateful ops) and how to migrate when it does not."
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Changing a running streaming query

**Goal:** deploy a new version of a streaming job without losing exactly-once progress, and recognise changes that require a new checkpoint.

## Change matrix (restart with the same checkpointLocation)
From the Structured Streaming guide, section "Recovery Semantics after Changes in a Streaming Query" ("not allowed" means the restarted query is likely to fail unpredictably):
| Change | Per the guide |
|---|---|
| Number or type of input sources | Not allowed |
| Rate limits on a Kafka source (`maxOffsetsPerTrigger`) | Allowed |
| Subscribed topics or files of a source | Generally not allowed; results are unpredictable |
| File sink to Kafka sink | Allowed (Kafka sees only the new data) |
| Kafka sink to file sink | Not allowed |
| Kafka sink to foreach sink, or back | Allowed |
| Output directory of a file sink | Not allowed |
| Output topic of a Kafka sink | Allowed |

The guide covers further kinds of change; read it before changing anything not in this table.

## Safe deploy procedure
1. Stop the query (or cancel the job) and wait for termination so the last batch commits.
2. Back up the whole checkpoint directory.
3. Deploy the new code with the same `checkpointLocation` and `queryName`.
4. Watch the first batches: `lastProgress`, `numRowsTotal` in stateful operators.

## When you need a new checkpoint
Stateless query: start a new checkpoint at the offsets where the old one stopped.
```python
# read the last committed offsets from the old checkpoint, then:
.option("startingOffsets", '{"orders":{"0":1234567,"1":1239876}}')
```
Make the sink idempotent around the boundary (MERGE by key), since you may reprocess one batch.

Stateful query: either rebuild state by replaying from source retention (needs enough Kafka retention), or read the old state with the State Data Source (marked experimental in the guide) and seed a new pipeline.

## Gotchas
- Test any change on a copy of the checkpoint first; the guide says a restart after a disallowed change is likely to fail unpredictably.

## Verify
- [ ] Restart test on a copy of prod checkpoint succeeds before deploying.
- [ ] No duplicate or missing keys in the sink around the deploy boundary.

## Checked

2026-10-28. Confirmed against: Structured Streaming guide, Recovery Semantics after Changes in a Streaming Query (source and sink change examples), Kafka integration page (startingOffsets, maxOffsetsPerTrigger), guide query-progress output (lastProgress, stateOperators numRowsTotal), State Data Source (experimental). Removed (not confirmable in the fetched pages): projection, foreachBatch, stateful-schema, watermark and shuffle-partition rows, StateSchemaNotCompatible and stateSchemaCheck, offsets/commits/state folder names, statestore format name and version claims, checkpoint concurrency and major-version claims.

Method: documentation only; no commands were run.
