---
id: computing-software.software-engineering.quarkus.quarkus-kafka-exactly-once-processing
name: quarkus-kafka-exactly-once-processing
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, kafka, exactly-once, transactions, exactlyonce, idempotence]
level: advanced
status: docs-checked
description: "Exactly-once consume-transform-produce in Quarkus Kafka with @ExactlyOnce or KafkaTransactions, auto-configured properties, database combos and pooled producers."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/kafka.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Kafka: exactly-once processing

Kafka transactions commit consumer offsets together with produced records (consume-transform-produce).

## Declarative: `@ExactlyOnce`
Put `io.quarkus.smallrye.reactivemessaging.kafka.ExactlyOnce` on a method that has both `@Incoming` and `@Outgoing`, both channels managed by the Kafka connector. Use payload parameters (`Record<K, V>`, plain types), not `Message<?>`.
```java
@Incoming("orders-in") @Outgoing("orders-out") @ExactlyOnce
Record<String, Integer> process(Record<String, Integer> order) {
    return Record.of(order.key(), order.value() + 1);
}
```
Return a `List` to produce several records, `Uni`/`CompletionStage` for non-blocking, or a `ProducerRecord` with a topic name to route (for example to a dead-letter topic) inside the same transaction.

Auto-configured (overridable in `application.properties`): outgoing `transactional.id` = `${quarkus.application.name}-<channel-name>`, `enable.idempotence=true`, `acks=all`; incoming `commit-strategy=ignore`, `isolation.level=read_committed`; `failure-strategy` defaults to `ignore`.

On an exception the Kafka transaction aborts, the offset resets to the last committed position and the record is retried on the next poll; a `@Transactional` database transaction rolls back too. A DB transaction runs inside the Kafka one; if DB commits but Kafka fails, the record is reprocessed, so make the consumer idempotent (or use a transactional outbox).

## Manual: `KafkaTransactions`
Inject `@Channel("prices-out") KafkaTransactions<Integer> txProducer` (with `@OnOverflow(value = OnOverflow.Strategy.BUFFER, bufferSize = 500)`; size it to fit `max.poll.records`). Batch consumers are recommended; single records cost performance.
```java
@Incoming("prices-in")
public Uni<Void> run(Message<ConsumerRecords<String, Integer>> batch) {
    return txProducer.withTransactionAndAck(batch, emitter -> {
        for (var r : batch.getPayload()) emitter.send(KafkaRecord.of(r.key(), r.value() + 1));
        return Uni.createFrom().voidItem();
    });
}
```
Configure `mp.messaging.incoming.prices-in.commit-strategy=ignore` and `failure-strategy=ignore`. `withTransactionAndAck` acks/nacks and does not return a failing `Uni`; a plain `withTransaction` failure that you return from `@Incoming` stops the channel. On abort the consumer resets to the last committed offset, or to the start of the partition if none, even when the reset policy is `latest`.

## Limits and extras
- One transaction at a time per producer; overlapping or nested `withTransaction` calls throw `IllegalStateException`. Limit REST concurrency with `@Bulkhead(1)`.
- `transactional.id` must be unique across instances in production.
- Concurrency: `mp.messaging.outgoing.<ch>.pooled-producer=true` (sizes `pooled-producer.max-pool-size` default 10, `pooled-producer.initial-pool-size` default 0), `ordered=partition`, `@Blocking(ordered = false)` and `withTransactionAndAwait(metadata, ...)`.
- Consumers reading only committed records: `mp.messaging.incoming.<ch>.isolation.level=read_committed`.

## Checked

2026-11-07. Read in full: kafka.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
