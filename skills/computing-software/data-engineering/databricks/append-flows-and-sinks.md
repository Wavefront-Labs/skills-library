---
id: computing-software.data-engineering.databricks.append-flows-and-sinks
name: append-flows-and-sinks
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt, append-flow, multiple-flows, dlt-sinks, streaming-tables, backfill-flow, lakeflow-declarative-pipelines]
level: advanced
status: docs-checked
description: "Write several sources into one streaming table with append flows in Lakeflow declarative pipelines (DLT), run one-off backfill flows, and send output to external sinks like Kafka."
sources:
  - https://docs.databricks.com/aws/en/ldp/concepts/flows
  - https://docs.databricks.com/aws/en/ldp/concepts/sinks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Append flows and sinks

**Goal:** combine multiple streams into one target without a UNION that forces full refreshes when a source is added, and push pipeline results to systems outside Delta.

## Append flows into one streaming table
```python
import dlt

dlt.create_streaming_table("all_orders")

@dlt.append_flow(target="all_orders", name="orders_eu")
def orders_eu():
    return spark.readStream.table("bronze.orders_eu")

@dlt.append_flow(target="all_orders", name="orders_us")
def orders_us():
    return spark.readStream.table("bronze.orders_us")
```
Multiple append flows can write to one target, which lets you add streaming sources to an existing streaming table without a full refresh and combine sources without a UNION clause. A default flow (created with the target) is an append flow with the same name as the target.

## One-time backfill flow
An append flow can carry the `ONCE` flag: a batch query whose data is inserted into the target only once, unless the target is fully refreshed. Use it to backfill a streaming table with missing historical data. See Databricks' "Backfilling historical data with pipelines" page for the exact syntax.

## Sinks (external targets)
```python
dlt.create_sink(
    name="orders_kafka",
    format="kafka",
    options={"kafka.bootstrap.servers": BS, "topic": "orders-curated",
             "kafka.security.protocol": "SASL_SSL", "kafka.sasl.mechanism": "PLAIN",
             "kafka.sasl.jaas.config": dbutils.secrets.get("kafka", "jaas")})

@dlt.append_flow(target="orders_kafka")
def to_kafka():
    return (spark.readStream.table("LIVE.all_orders")
            .selectExpr("cast(order_id as string) as key", "to_json(struct(*)) as value"))
```
Sink types include Delta (Unity Catalog managed or external tables, by file path or fully qualified name), Apache Kafka, Azure Event Hubs (via the Kafka interface) and Python custom sinks. Documented limits: sinks are Python only (no SQL), streaming queries only, only `append_flow` and `update_flow` can write to them, pipeline expectations are not supported for sinks, and a full refresh does not clean up data already written to a sink.

## Gotchas

## Verify
- [ ] Pipeline graph shows each flow feeding the target.
- [ ] Adding a new flow in a test pipeline does not trigger a full refresh of the target.

## Checked
2026-11-01. Confirmed against the Databricks pages Flows (append flows, ONCE flag, default flows) and Sinks in Lakeflow pipelines (sink types, limitations, create_sink and append_flow). Removed: SQL CREATE FLOW examples, per-flow checkpoint and rename claims, UNION checkpoint claim, the dp import note and the gotchas list.
Method: documentation only; no commands were run.
