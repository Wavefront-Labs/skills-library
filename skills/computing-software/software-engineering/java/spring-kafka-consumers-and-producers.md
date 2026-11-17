---
id: computing-software.software-engineering.java.spring-kafka-consumers-and-producers
name: spring-kafka-consumers-and-producers
category: computing-software
field: software-engineering
product: java
tags: [java, spring-messaging, spring-kafka, kafkalistener, consumer-group, dead-letter-topic, errorhandlingdeserializer]
level: advanced
status: docs-checked
description: "Use Spring for Apache Kafka: KafkaTemplate send results, DefaultErrorHandler retry with dead-letter topics, ErrorHandlingDeserializer poison pills, transactions."
sources: ["https://docs.spring.io/spring-kafka/reference/", "https://github.com/spring-projects/spring-kafka/tree/main/spring-kafka-docs/src/main/antora/modules/ROOT/pages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Kafka consumers and producers

## Producer
`KafkaTemplate.send(...)` is asynchronous and returns a `CompletableFuture<SendResult<K, V>>`. Handle the result, or an unobserved failure is a lost message.
```java
CompletableFuture<SendResult<String, Order>> future = template.send("orders", order.id(), order);
future.whenComplete((result, ex) -> { if (ex != null) log.error("send failed", ex); });
```
- Use the keyed overload (`send(topic, key, data)`) when you want a key-based partition choice.
- To block, call `get()` on the future, and use the variant with a timeout.
- Alternatively register a `ProducerListener` on the template for an asynchronous callback with each send's success or failure.

## Consumer
`@KafkaListener` methods run in listener containers configured through the container factory. The container property `ackMode` controls when offsets are committed (`RECORD`, `BATCH`, `COUNT`, `TIME`, `COUNT_TIME`, `MANUAL`, `MANUAL_IMMEDIATE`). With `BATCH`, offsets are committed after the records from a poll are processed. The container docs state that the time to process a batch plus `idleBetweenPolls` must be less than the `max.poll.interval.ms` consumer property. Processing must be idempotent (at-least-once delivery).

## Errors and dead letters
```java
@Bean
DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
    var recoverer = new DeadLetterPublishingRecoverer(template);
    var handler = new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 2L));
    handler.addNotRetryableExceptions(IllegalArgumentException.class);
    return handler;
}
```
Attach it with `factory.setCommonErrorHandler(...)` on the listener container factory.
- The default `DefaultErrorHandler` configuration is `FixedBackOff(0L, 9)` (immediate retries); `FixedBackOff(1000L, 2L)` means up to 2 retries, 3 delivery attempts, one second apart. `FixedBackOff.UNLIMITED_ATTEMPTS` retries effectively forever.
- Certain exceptions (for example `DeserializationException`, `MessageConversionException`) are fatal: retries are skipped and the recoverer runs on the first failure. Add your own with `addNotRetryableExceptions(...)`. The handler only processes `RuntimeException` subclasses.
- `DeadLetterPublishingRecoverer` publishes the failed record to a topic named `<originalTopic>-dlt` (the same partition as the original) by default; pass a destination resolver to change it. With `AckMode.MANUAL_IMMEDIATE`, set `commitRecovered` to `true` on the handler to commit recovered records.
- Wrap deserializers in `ErrorHandlingDeserializer` so a record that cannot be deserialized yields a null value plus a `DeserializationException` in a header (cause and raw bytes) instead of failing the poll repeatedly. Set the delegates with `ErrorHandlingDeserializer.VALUE_DESERIALIZER_CLASS` and `KEY_DESERIALIZER_CLASS`.
- Batch listeners: throw `BatchListenerFailedException` to identify the failing record; the same handler plus recoverer is used for dead letters.
- The reference also has a non-blocking retry feature (retry topics, `@RetryableTopic`), not covered here.

## Transactions
Setting a `transactionIdPrefix` on the `DefaultKafkaProducerFactory` enables transactions; the `transactional.id` is the prefix plus a counter, and the prefix must be unique per application instance. With Spring Boot, set `spring.kafka.producer.transaction-id-prefix` and Boot wires a `KafkaTransactionManager` into the listener container.

## Verify
Produce a malformed message and a failing-handler message to a test topic; assert retries occur, the dead-letter topic receives the record, and the main consumer carries on.

## Checked
Read the Spring Kafka sending-messages, container-properties, serdes (ErrorHandlingDeserializer section grepped), error-handling (DefaultErrorHandler, dead-letter and batch sections grepped) and transactions pages from the docs source on GitHub; the docs.spring.io landing page is an index. The Apache Kafka producer and consumer config pages were not read. Removed as unconfirmed: the YAML producer config (acks, idempotence, linger), the JSON serializer class names (the current docs use Jackson 3 based classes), concurrency equals partitions advice, the 5 minute max.poll.interval default, schema registry advice, trusted packages, outbox pattern, static membership and EmbeddedKafka.
Method: docs-checked 2026-11-09 against the Spring Kafka reference pages on sending, container properties, serialization, error handling and transactions.
