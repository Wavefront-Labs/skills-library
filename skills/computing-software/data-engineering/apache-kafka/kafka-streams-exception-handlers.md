---
id: computing-software.data-engineering.apache-kafka.kafka-streams-exception-handlers
name: kafka-streams-exception-handlers
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-streams, deserialization-exception-handler, production-exception-handler, processing-exception-handler, uncaught-exception-handler, poison-pill, dlq]
level: advanced
status: docs-checked
description: "Handle failures in Kafka Streams: deserialization, production and processing exception handlers, the uncaught exception handler (REPLACE_THREAD), and DLQ routing."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/config-streams/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-1033%3A+Add+Kafka+Streams+exception+handler+for+exceptions+occurring+during+processing
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-671%3A+Introduce+Kafka+Streams+Specific+Uncaught+Exception+Handler
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Streams exception handlers

**Goal:** a single bad record does not kill the application or silently vanish; failures are routed and counted.

## Where errors happen and the hook for each
| Stage | Hook | Default |
|---|---|---|
| Deserializing input | `default.deserialization.exception.handler` | `LogAndFailExceptionHandler` |
| Your processor code (Kafka 3.9+, KIP-1033) | `processing.exception.handler` | `LogAndFailProcessingExceptionHandler` |
| Producing output (serialization / broker errors like RecordTooLarge) | `default.production.exception.handler` | `DefaultProductionExceptionHandler` (fail) |
| Anything that kills a stream thread | `KafkaStreams#setUncaughtExceptionHandler` | `SHUTDOWN_CLIENT` |

## Config
```properties
default.deserialization.exception.handler=org.apache.kafka.streams.errors.LogAndContinueExceptionHandler
processing.exception.handler=org.apache.kafka.streams.errors.LogAndContinueProcessingExceptionHandler
```
Skipped records increment the `dropped-records` metric (total and rate). Alert on it.

## Custom DLQ handler (deserialization)
```java
public class DlqDeserHandler implements DeserializationExceptionHandler {
  private KafkaProducer<byte[], byte[]> dlq;
  public void configure(Map<String, ?> cfg) { dlq = new KafkaProducer<>(producerProps(cfg)); }
  public DeserializationHandlerResponse handle(ErrorHandlerContext ctx, ConsumerRecord<byte[], byte[]> rec, Exception e) {
    ProducerRecord<byte[], byte[]> out = new ProducerRecord<>("orders.dlq", rec.key(), rec.value());
    out.headers().add("error", e.toString().getBytes()).add("src", (rec.topic()+"/"+rec.partition()+"/"+rec.offset()).getBytes());
    dlq.send(out);
    return DeserializationHandlerResponse.CONTINUE;
  }
}
```
(Signature varies by version: KIP-1033 (accepted for 3.9) adds `ErrorHandlerContext` to the handler signatures; older versions pass a `ProcessorContext`.)

## Uncaught exceptions
```java
streams.setUncaughtExceptionHandler(ex -> {
  log.error("stream thread died", ex);
  return ex instanceof RetriableAppException
      ? StreamsUncaughtExceptionResponse.REPLACE_THREAD
      : StreamsUncaughtExceptionResponse.SHUTDOWN_APPLICATION;   // or SHUTDOWN_CLIENT
});
```
`REPLACE_THREAD` shuts the failed thread down and starts a new one while the client is RUNNING or REBALANCING (for the global thread it falls back to shutting down the client). `SHUTDOWN_APPLICATION` shuts down every client of the application. Pair `REPLACE_THREAD` with the handlers above rather than relying on it as the poison-pill strategy.

## Choosing behaviour
- Bad input format (schema mismatch): continue + DLQ.
- Business logic exception on one record: catch inside the processor and branch to an error topic (explicit), or use the processing handler.
- Infrastructure failures (auth, missing topic): fail fast, do not continue.
- A CONTINUE from a production or processing handler skips the record; use it deliberately and alert on `dropped-records`.

## Checked
2026-10-28. Confirmed: handler config names and defaults (`default.deserialization.exception.handler`, `default.production.exception.handler` = `DefaultProductionExceptionHandler`, `processing.exception.handler` = `LogAndFailProcessingExceptionHandler`) on the Kafka 3.9 Streams configuration page; `ErrorHandlerContext`, `LogAndContinueProcessingExceptionHandler`, `dropped-records` metric and the 3.9 acceptance in KIP-1033; `StreamsUncaughtExceptionResponse` values, `SHUTDOWN_CLIENT` default and the behaviour of each value in KIP-671. Corrected: the response enum is `StreamsUncaughtExceptionResponse`, not `StreamThreadExceptionResponse`. Removed: 4.0 rename, KIP-1034 dead-letter config and exactly-once loss claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Produce a malformed record in staging: app keeps running, DLQ receives it with headers, `dropped-records-total` increments.
- [ ] Alert exists on DLQ topic growth and on thread replacements.
