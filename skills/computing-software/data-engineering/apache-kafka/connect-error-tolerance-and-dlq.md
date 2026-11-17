---
id: computing-software.data-engineering.apache-kafka.connect-error-tolerance-and-dlq
name: connect-error-tolerance-and-dlq
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-connect, errors-tolerance, connect-dead-letter-queue, errors-deadletterqueue-topic-name, errors-log-enable, context-headers, failed-task, poison-pill]
level: advanced
status: docs-checked
description: "Keep Kafka Connect sinks running past bad records: errors.tolerance, DLQ topic with context headers, retry timeouts, logging, and what errors the framework cannot route to a DLQ."
sources:
  - https://kafka.apache.org/documentation/#connect_errorreporting
  - https://github.com/apache/kafka/blob/trunk/docs/kafka-connect/user-guide.md
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/errors/DeadLetterQueueReporter.java
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/errors/ErrorHandlingMetrics.java
  - https://github.com/apache/kafka/blob/trunk/connect/api/src/main/java/org/apache/kafka/connect/sink/ErrantRecordReporter.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Connect error tolerance and dead-letter queues

**Goal:** one malformed record does not stop a sink connector, and every skipped record is recoverable.

Default `errors.tolerance=none`: any error during conversion or transformation fails the connector task (`FAILED` state) until someone intervenes. The defaults are `errors.retry.timeout=0`, `errors.log.enable=false` and no DLQ topic.

## Configure a DLQ (sink connectors only)
```json
"errors.tolerance": "all",
"errors.deadletterqueue.topic.name": "dlq.orders-s3-sink",
"errors.deadletterqueue.topic.replication.factor": "3",
"errors.deadletterqueue.context.headers.enable": "true",
"errors.log.enable": "true",
"errors.log.include.messages": "false",
"errors.retry.timeout": "300000",
"errors.retry.delay.max.ms": "60000"
```
- Context headers (`__connect.errors.` plus `topic`, `partition`, `offset`, `connector.name`, `task.id`, `stage`, `class.name`, `exception.class.name`, `exception.message`, `exception.stacktrace`) tell you where and why each record failed; they are off unless `errors.deadletterqueue.context.headers.enable=true`. DLQ replication factor defaults to 3.
- `errors.log.include.messages=true` also logs the record key, value and headers, which may be sensitive: avoid for PII.
- `errors.retry.timeout` is the maximum time (ms) to retry a failed operation, with `errors.retry.delay.max.ms` as the maximum wait between attempts; the default 0 means no retries.

## What goes to the DLQ (and what does not)
Covered: errors in the key, value and header **converters** and in **transformations** (the framework's stages). The docs say error reporting also applies to the sink connector itself while processing consumed records; for individual bad records inside `put()`, a sink task reports them through the errant record reporter (`ErrantRecordReporter`, since 2.6), so check whether your connector uses it.
The DLQ settings (`errors.deadletterqueue.*`) belong to sink connectors; `errors.tolerance=all` on a source connector skips failed records and logs them.

## Reprocessing the DLQ
1. Inspect the DLQ topic with a console consumer, printing headers.
2. Fix the cause (schema, SMT config, upstream producer).
3. Replay: a second connector instance reading the DLQ topic with the fixed config, or a small consumer that repairs and re-produces to the original topic.

## Alerting
- Alert on DLQ topic message rate above zero (or a threshold): `errors.tolerance=all` without DLQ monitoring silently drops data.
- Task error metrics (group `task-error-metrics`): `total-record-failures`, `total-record-errors`, `total-records-skipped`, `total-retries`, `total-errors-logged`, `deadletterqueue-produce-requests`, `deadletterqueue-produce-failures`.
- Task status: `GET /connectors/<name>/status` shows any `FAILED` task with its `trace`; restart with `POST /connectors/<name>/restart?includeTasks=true&onlyFailed=true`.

## Verify
- [ ] Produce a malformed record in test: connector stays RUNNING, record appears in the DLQ with error headers.
- [ ] DLQ rate alert is wired and tested.
- [ ] Runbook documents DLQ replay steps.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed (user guide error-reporting section and Connect source): `errors.tolerance` default none, `errors.retry.timeout` default 0, `errors.retry.delay.max.ms` default 60000, `errors.log.enable` and `errors.log.include.messages` defaults false, `errors.deadletterqueue.topic.name`, `.topic.replication.factor` (default 3) and `.context.headers.enable` (default false), the context header names (DeadLetterQueueReporter), the converter and transformation stages, `ErrantRecordReporter` since 2.6, and the task error metric names and group (ErrorHandlingMetrics, ConnectMetricsRegistry). Fixed: the metric group is `task-error-metrics`, not `connector-task-metrics`. Removed: the Confluent blog link, `kcat`, JDBC-sink support claims, the 3.0 gate and the "source connectors have no DLQ" overstatement.

Method: documentation only; no commands were run.
