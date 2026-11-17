---
id: computing-software.data-engineering.data-quality.validation-in-streaming-pipelines
name: validation-in-streaming-pipelines
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, streaming-validation, schema-validation, dead-letter-queue, real-time-dq]
level: advanced
status: docs-checked
description: "Validate data quality in streaming pipelines: schema enforcement at the broker, per-record checks with dead-letter routing, windowed metrics checks and alerting."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/index.html
  - https://docs.databricks.com/aws/en/dlt/expectations
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/side_output/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validation in streaming pipelines

**Goal:** bad events are caught within seconds, isolated without stopping the stream, and aggregate quality drifts are detected.

## Layer 1: schema at the edge
- Schema Registry with compatibility rules and producer serializers that fail on invalid schemas; check the Confluent docs for broker-side schema validation and data contract rules.

## Layer 2: per-record checks with dead-letter routing
```python
# Spark Structured Streaming
# flag each record once, then split into the main sink and a quarantine sink
flagged = parsed.withColumn("dq_ok", F.expr("order_id IS NOT NULL AND amount >= 0"))
flagged.where("dq_ok").writeStream...      # main sink
flagged.where("NOT dq_ok").writeStream...  # quarantine table / DLQ topic
```
- Flink: side outputs (`ctx.output(invalidTag, event)`) to a DLQ sink.
- Kafka Connect: use its error-handling and dead-letter queue settings (see the Connect docs).
- Lakeflow pipelines: `expect_or_drop` plus a quarantine table.
Keep the original payload, error reason and timestamp in the DLQ.

## Layer 3: windowed metrics
Per window (1-5 min): event count, null rates, distinct keys, late-event share. Compare to rolling baselines; alert on anomalies (volume drop to zero is the most common real incident).

## Operations
- DLQ volume alert (absolute and as % of traffic).
- Replay tool to reprocess DLQ records after fixes.
- Do not block the stream on soft rules; block (fail) only when continuing would corrupt state.

## Gotchas
- Validating by joining to reference data in-stream needs the reference data loaded/broadcast and refreshed.
- Expensive checks (regex on big payloads) add latency; measure.

## Verify
Inject invalid events: they appear in the DLQ with reasons, valid flow continues, and the DLQ alert fires above threshold.

## Checked

2026-10-28. Confirmed: Databricks expectations page (`expect_or_drop` drops invalid records before they reach the target) and the Flink side output page (side outputs for routing records). Removed: `confluent.value.schema.validation`, Confluent data contract rules with CEL, the Kafka Connect `errors.*` property names and the Spark `subtract` remark (not found in the fetched pages).

Method: documentation only; no commands were run.
