---
id: computing-software.data-engineering.etl-pipeline-design.poison-messages
name: poison-messages
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, poison-message, dead-letter-queue, retry-topics, max-receive-count, consumer-errors, error-handling]
level: practitioner
status: docs-checked
description: "Stop one malformed message blocking a stream or queue consumer: classify failures, bound retries, route to a DLQ with context, replay after fixes."
sources:
  - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
  - https://cloud.google.com/pubsub/docs/handling-failures
  - https://docs.confluent.io/platform/current/connect/concepts.html#dead-letter-queue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poison messages

**Goal:** one bad record (corrupt bytes, schema mismatch, value that crashes your code) does not halt processing of everything behind it.

## Why it is worse in ordered logs
Standard queues (SQS, Pub/Sub) redeliver the bad message while others proceed. An ordered log (a Kafka partition, a Kinesis shard) has no way to redeliver around one record: if the consumer keeps retrying the bad offset, everything behind it waits and lag grows. SQS says the same about FIFO queues: a dead-letter queue breaks exact message order, so do not use one where order carries meaning.

## Classify failures
| Type | Example | Handling |
|---|---|---|
| Permanent (poison) | undeserializable payload, missing required field, invalid enum | DLQ immediately, no retries |
| Transient | DB timeout, 503 from API | retry with backoff, then DLQ |
| Systemic | wrong credentials, schema registry down | stop and alert; do NOT DLQ everything |
Distinguishing systemic from poison matters: if 100% of messages fail, it is your system, and dumping all traffic into the DLQ creates a mess. Add a circuit breaker (e.g. pause when >N% fail in a window).

## Patterns
**Queues (built-in redrive):**
- SQS: a redrive policy with `maxReceiveCount` moves a message to the dead-letter queue after that many receives. Set it high enough to allow sufficient retries (a value of 1 sends a message to the DLQ after a single failed receive). The DLQ must be created first and be in the same account and Region as the source queue. A redrive allow policy controls which source queues may use it (all source queues by default, specific queues via `byQueue` up to 10 ARNs, or `denyAll`). Messages can be moved back out with DLQ redrive.
- Pub/Sub: a dead-letter topic is a property of the subscription, not the topic. Maximum delivery attempts is default 5, minimum 5, maximum 100, and is approximate (a message can be forwarded after fewer attempts or a few more). Pub/Sub wraps the original message and adds attributes identifying the source subscription; attach a subscription to the dead-letter topic to inspect them. The Pub/Sub service account needs publisher and subscriber roles on the dead-letter resources, or attempts are not counted.

**Kafka consumers (do it yourself; pseudocode, the client calls are illustrative):**
```python
try:
    event = deserialize(msg.value())
    handle(event)
except (DeserializationError, ValidationError) as e:
    dlq.produce("orders.dlq", key=msg.key(), value=msg.value(), headers=[
        ("error.class", type(e).__name__.encode()), ("error.msg", str(e)[:1000].encode()),
        ("src.topic", msg.topic().encode()), ("src.partition", str(msg.partition()).encode()),
        ("src.offset", str(msg.offset()).encode())])
consumer.store_offsets(msg)      # move on either way
```
Non-blocking retries for transient errors: retry topics with delays (`orders.retry.1m`, `orders.retry.10m`) then DLQ. Note this breaks per-key ordering for retried records.

Kafka Connect (sink connectors only; DLQs do not apply to source connectors): the `errors.tolerance` property is `none` (default; an invalid record fails the task and the connector goes to a failed state) or `all`. With `all`, Connect ignores errors and writes nothing to the worker log, so you must use internal metrics or count records at source and sink to notice failures. Route bad records to a DLQ topic with `errors.tolerance = all` plus `errors.deadletterqueue.topic.name`. The topic alone does not say why a record failed: set `errors.deadletterqueue.context.headers.enable=true` (default `false`) to add context headers, whose keys start with `_connect.errors`.

## DLQ hygiene
- Keep the original bytes untouched plus error context headers; never "fix" in place.
- Monitor DLQ depth/rate; alert on any growth for critical streams (SQS documents CloudWatch alarms for messages moved to a DLQ).
- Owner and runbook: inspect, fix code or data, **replay** from DLQ to the main topic (or a reprocess topic) with a tool that preserves keys; mark replayed.
- Retention on DLQ longer than on the source. In SQS standard queues the original enqueue timestamp is kept when a message moves to the DLQ, so a DLQ retention equal to the source's can delete messages almost immediately.

## Verify
- [ ] Inject a malformed record: consumer lag does not grow, DLQ gets one record with headers.
- [ ] Simulate dependency outage: consumer pauses/alerts instead of flooding the DLQ.

## Checked
Checked 2026-11-08: SQS dead-letter queue page (read in full), Confluent Kafka Connect concepts, Dead Letter Queue section (read lines 95-155), Pub/Sub dead-letter topics page (read the concept, properties and console steps, lines 25-110 of about 600; the rest is per-language samples). Removed: SQS visibility timeout advice, Pub/Sub retry policy backoff, Spring Kafka `@RetryableTopic`, Kafka Streams and Flink handlers (not on pages read). The Kafka consumer snippet is illustrative pseudocode and was not checked against a client library.
Method: documentation only; no commands were run.
