---
id: computing-software.software-engineering.quarkus.quarkus-kafka-commit-and-failure-strategies
name: quarkus-kafka-commit-and-failure-strategies
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, kafka, commit-strategy, dead-letter-queue, acknowledgment, reactive-messaging]
level: practitioner
status: docs-checked
description: "Choose Quarkus Kafka incoming-channel commit strategies (throttled, latest, ignore, checkpoint) and failure strategies (fail, ignore, dead-letter-queue), plus ack modes."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/kafka.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Kafka: commit, acknowledgment and failure strategies

Configure per channel under `mp.messaging.incoming.<channel>.`; the connector is `smallrye-kafka`.

## Acknowledgment
Every received message must be acked or processing counts as an error. Payload and `Record` parameters are acked on method return (`POST_PROCESSING`); methods returning a stream or `CompletionStage` ack when the downstream message is acked; a `Message` parameter means `MANUAL` (call `msg.ack()`). Override with `@Acknowledgment(Acknowledgment.Strategy.PRE_PROCESSING)` or `Strategy.NONE`.

## Commit strategy (`commit-strategy`)
Runs when a record's message is acked; decides when the offset is committed.
- `throttled`: commits the highest consecutive acked offset every `auto.commit.interval.ms` (default 5000). At-least-once even with async processing. Marked unhealthy if a record is unacked after `throttled.unprocessed-record-max-age.ms` (default 60000); a value of 0 or less disables the check but risks running out of memory with poison-pill messages. Default unless `enable.auto.commit` is explicitly true.
- `latest`: commits the offset as soon as acked. Only at-least-once without async processing; expensive under high load.
- `ignore`: no commit; default when `enable.auto.commit` is true, delegating to the Kafka client. With auto commit true it does NOT guarantee at-least-once.
- `checkpoint`: stores offsets plus processing state in a state store (experimental); unhealthy if state is not persisted within `checkpoint.unsynced-state-max-age.ms` (default 10000).

The connector disables Kafka auto commit unless you enable it. For high throughput use `throttled`, or set `enable.auto.commit=true` with `@Acknowledgment(Acknowledgment.Strategy.NONE)`.

## Failure strategy (`failure-strategy`)
Applied when a message is nacked:
- `fail` (default): the application fails; the offset is not committed.
- `ignore`: log and continue; the offset is committed.
- `dead-letter-queue`: commit the offset and write the record to a dead letter topic. Attributes: `dead-letter-queue.topic` (default `dead-letter-topic-$channel`), `dead-letter-queue.key.serializer`, `dead-letter-queue.value.serializer`. Added headers: `dead-letter-reason`, `dead-letter-cause`, `dead-letter-topic`, `dead-letter-partition`, `dead-letter-offset`.
- `delayed-retry-topic`: failed records go to delayed retry topics with configurable delays and maximum retries.

## Retry and deserialization
- `@Retry(delay = 10, maxRetries = 5)` from SmallRye Fault Tolerance retries a failing consumer; after the last retry the message is nacked and the failure strategy applies. For `Uni`/`CompletionStage` returns add `@NonBlocking` on Fault Tolerance 5.1.0 and earlier.
- Deserialization failures: expose a bean implementing `DeserializationFailureHandler<T>` with `@Identifier("name")` and set `mp.messaging.incoming.<channel>.value-deserialization-failure-handler=name` (or `key-`). Without a handler the app is marked unhealthy; `fail-on-deserialization-failure=false` logs and yields `null` (and goes to the DLQ if `failure-strategy=dead-letter-queue`).

## Checked

2026-11-07. Read in full: kafka.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
