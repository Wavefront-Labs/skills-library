---
id: computing-software.data-engineering.snowflake.snowpipe-streams-and-tasks
name: snowpipe-streams-and-tasks
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpipe, snowpipe-streaming, streams, tasks, change-tracking, task-dag, serverless-tasks, continuous-ingestion, stream-offset, cdc-snowflake]
level: practitioner
status: docs-checked
description: "Build continuous Snowflake ingestion and transformation pipelines with Snowpipe/Snowpipe Streaming, Streams for CDC, and Tasks for scheduling."
sources:
  - https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro
  - https://docs.snowflake.com/en/user-guide/streams-intro
  - https://docs.snowflake.com/en/user-guide/tasks-intro
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Snowpipe, Streams and Tasks — Snowflake's native pipeline primitives

**Goal:** build continuous ingestion-to-transformation pipelines using Snowflake's own primitives instead of reaching for an external orchestrator for work Snowflake already does natively.

## 1. Snowpipe vs Snowpipe Streaming — different ingestion shapes
- **Snowpipe** (file-based, `COPY INTO` auto-triggered by cloud storage event notifications, e.g. S3 event → SQS → Snowpipe): ingests files as they land, with per-file overhead — good for batched file drops (every few minutes to hourly), not built for continuous row-by-row ingestion. Snowpipe loads files on serverless compute and new data is typically available within minutes; the docs recommend compressed files of roughly 100 to 250 MB, and say staging smaller files more often does not guarantee lower latency.
- **Snowpipe Streaming** (SDK-based, rows pushed directly without staging files first): built for genuinely low-latency, high-frequency ingestion for rows or events needed within seconds, with no intermediate file/stage step — the right choice when the file-based Snowpipe's per-file overhead or latency floor doesn't meet requirements.
- Don't default to Snowpipe Streaming for "it's newer/faster" reasons alone — if hourly/15-minute file-based ingestion already satisfies the actual latency requirement (see computing-software.data-engineering.etl-pipeline-design.batch-vs-streaming-tradeoffs), the simpler file-based Snowpipe is less to operate.

## 2. Streams — native, metadata-only CDC on a table
`CREATE STREAM my_stream ON TABLE orders;` creates a change-tracking object that records inserts/updates/deletes on the source table since the stream was last consumed, exposed via `METADATA$ACTION`/`METADATA$ISUPDATE`/`METADATA$ROW_ID` columns when queried — no polling, no triggers, no separate CDC tool needed for intra-Snowflake change capture. A stream stores an offset for the source object. Give each stream exactly one consuming Task or pipeline rather than sharing it ad hoc across independent consumers.
- Streams have a staleness limit — if the stream isn't consumed before the underlying table's data retention period elapses (the source table's data retention period, which can be extended up to `MAX_DATA_EXTENSION_TIME_IN_DAYS`; calling `SYSTEM$STREAM_HAS_DATA` on an empty stream also prevents it going stale), the stream becomes stale and must be recreated, losing track of unconsumed changes. A paused/broken downstream Task for too long silently risks this — monitor stream staleness, don't assume it stays valid indefinitely.

## 3. Tasks — Snowflake-native scheduling, with real DAG support
`CREATE TASK` runs a single SQL statement (often a `MERGE`/`INSERT` consuming a Stream) on a cron schedule or triggered by another task completing, with `AFTER` clauses building a task DAG natively within Snowflake — for pipelines entirely within Snowflake (ingest → stream → transform → mart), this avoids needing an external orchestrator at all. **Serverless tasks** (no user-managed virtual warehouse — Snowflake manages the compute) suit variable/bursty workloads where sizing a dedicated warehouse would mean paying for idle capacity; user-managed-warehouse tasks run on a warehouse you size.
- A Stream+Task pair is the idiomatic Snowflake-native pattern for "process only what changed since last run" without hand-rolling a watermark/high-water-mark column comparison — but it only works for intra-Snowflake pipelines; CDC from an external source system still needs Snowpipe/Snowpipe Streaming (or an external CDC tool like Debezium) to land the initial changes into a Snowflake table first.

## 4. Where this still needs an external orchestrator
Multi-system pipelines (Snowflake plus S3, an API, a non-Snowflake database write) still need Airflow/Dagster/dbt Cloud-style orchestration for the parts outside Snowflake. Use Tasks for the Snowflake-internal portion of a pipeline, and an external orchestrator to call into Snowflake (trigger a Task, run a stored procedure) as one step of a larger cross-system DAG when the pipeline spans systems.

## Verify
- [ ] Each Stream has exactly one consuming DML/Task path.
- [ ] Stream staleness is monitored (`SYSTEM$STREAM_HAS_DATA` plus checking the underlying table's retention window) so a paused downstream Task is caught before the stream goes stale.
- [ ] Snowpipe Streaming was chosen over file-based Snowpipe for a specific, measured latency requirement — not by default.
- [ ] A multi-system pipeline's Snowflake-internal Tasks are triggered by, not duplicating, the external orchestrator's own scheduling of the same logical pipeline.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the Snowpipe intro, streams intro, CREATE STREAM and CREATE TASK pages: Snowpipe serverless loading, file-size guidance, Snowpipe Streaming for low-latency rows, stream offset and METADATA$ACTION / METADATA$ISUPDATE / METADATA$ROW_ID columns, staleness and MAX_DATA_EXTENSION_TIME_IN_DAYS, SYSTEM$STREAM_HAS_DATA, CREATE STREAM ... ON TABLE, task scheduling and AFTER dependencies, serverless tasks.

Removed: the Ingest SDK and Kafka Connect statements, the warehouse-versus-serverless cost comparison, the claim that tasks cannot call external systems, and the ad hoc SELECT offset warning.

Method: documentation only; no commands were run.
