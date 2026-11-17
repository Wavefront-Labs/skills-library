---
id: computing-software.data-engineering.etl-pipeline-design.batch-vs-streaming-tradeoffs
name: batch-vs-streaming-tradeoffs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, batch-processing, micro-batch, streaming, latency-requirements, operational-complexity, lambda-architecture, trigger-availablenow, cost-of-streaming, architecture-decision]
level: practitioner
status: docs-checked
description: "Decide batch vs micro-batch vs continuous streaming by the consumer's freshness need, with Spark Structured Streaming trigger modes as the worked example."
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch vs streaming: decide by latency requirement

**Goal:** avoid both mistakes: an always-on streaming pipeline for a dashboard checked once a day, and a brittle batch job for something that needs fresh data.

## 1. Start from the consumer requirement
Ask what decision or action depends on this data and how stale it can be before that decision is wrong or too late. Write the actual freshness number down (seconds, minutes, hours, next business morning) before picking an architecture. "Real-time" is a proxy for something more specific.

## 2. Trigger modes in Spark Structured Streaming (worked example)
The trigger settings define the timing of processing: a micro-batch query with a fixed batch interval, or a continuous processing query. The documented options:
- **Fixed interval micro-batches**: micro-batches start at the interval you specify.
- **Available-now micro-batch** (`Trigger.AvailableNow`): processes all available data, then the query stops on its own. The documentation says the older one-time trigger is deprecated and recommends this one, for better processing guarantees, finer-grained batches and better watermark handling.
- **Continuous with fixed checkpoint interval**: a low-latency continuous processing mode, marked experimental in the docs. `foreachBatch` does not work in continuous mode; use `foreach` instead.

So a scheduled run of an available-now query gives batch-style operation on a streaming engine, with the interval trigger as the next step towards freshness. Check what your engine documents before assuming it offers the same choices.

## 3. The backfill test, before committing to streaming
Ask: "If we found a bug in this pipeline today, how do we reprocess the last 30 days?" Write down the answer for the chosen architecture. If nobody has designed and tested the reprocessing path, flag that gap before production. Stateful designs (windowed aggregations, joins) need an explicit plan to avoid double counting against data already processed.

## 4. One tier per pipeline
Choose the tier per pipeline from its own consumer's requirement, not platform-wide.

## Verify
- [ ] The freshness requirement is a written number from the real consuming decision.
- [ ] Micro-batch (including an available-now run on a schedule) was considered, with a stated reason if rejected.
- [ ] A backfill plan exists and was tried on a non-trivial historical range before launch.
- [ ] Each pipeline's tier was a deliberate choice for its own consumer.

## Checked
2026-11-01. Confirmed from the Apache Spark Structured Streaming programming guide (`sources`): trigger types, available-now behaviour and the one-time trigger deprecation note, continuous mode marked experimental, `foreachBatch` not working in continuous mode. Removed (no page read): cost and operational claims for batch versus Flink, Kafka Streams and Spark continuous, the Lambda and Kappa architecture descriptions, example latency figures and the claim about how often "streaming" requests need less.
Method: documentation only; no commands were run.
