---
id: computing-software.data-engineering.apache-kafka.producer-error-handling
name: producer-error-handling
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-producer, producer-error-handling, send-callback, retriable-exception, delivery-timeout, record-too-large, flush, graceful-shutdown, dead-letter-queue]
level: practitioner
status: docs-checked
description: "Handle Kafka producer failures: async send callbacks, retriable vs fatal errors, delivery.timeout.ms, RecordTooLarge and serialization errors, flush on shutdown."
sources:
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html
  - https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer error handling

**Goal:** every record is either acknowledged by Kafka or surfaced as a failure your code handles. No silent drops.

## send() is asynchronous
```java
producer.send(record, (metadata, ex) -> {
  if (ex == null) return;
  if (ex instanceof RecordTooLargeException || ex instanceof SerializationException) {
    deadLetter(record, ex);                 // permanent: will never succeed
  } else {
    failures.incrementAndGet();             // retriable errors already retried until delivery.timeout.ms
    log.error("send failed after retries", ex);
    stopAcceptingInput();                   // let the caller fail upstream / replay
  }
});
```
Fire-and-forget `send(record)` with no callback and no `get()` loses errors entirely.
Calling `.get()` on every future makes the producer synchronous (one in-flight record): correct but slow. Use callbacks, or collect futures per batch and check them before committing upstream offsets.

## Retries are built in
With defaults (`retries=MAX_INT`, `delivery.timeout.ms=120000`, `enable.idempotence=true`), transient errors (leader election, `NotEnoughReplicas`, timeouts) are retried automatically and without duplicates/reordering. The callback only sees an error once `delivery.timeout.ms` expires or the error is non-retriable. Do not write your own retry loop around `send` (it reintroduces duplicates).

## Error classes
| Error | Meaning | Action |
|---|---|---|
| `TimeoutException` (delivery timeout) | Brokers unavailable too long | Alert; pause source; replay |
| `RecordTooLargeException` | Bigger than `max.request.size` / topic `max.message.bytes` | DLQ or store payload externally |
| `SerializationException` | Bad data / schema registry rejected | DLQ |
| `AuthorizationException`, `TopicAuthorizationException` | ACL missing | Fatal, fix config |
| `ProducerFencedException`, `OutOfOrderSequenceException` | Transactional/idempotent fatal state | Close and recreate producer |

## Python (librdkafka)
```python
def on_delivery(err, msg):
    if err: handle_failure(err, msg)
p.produce(topic, key=k, value=v, on_delivery=on_delivery)
p.poll(0)                   # serve callbacks regularly; without poll() callbacks never run
...
remaining = p.flush(30)     # at shutdown; >0 means undelivered messages
```
`BufferError` from `produce()` = local queue full: call `p.poll(1)` and retry the produce.

## Shutdown
Call `flush()` then `close(Duration)`. Killing the process without flushing loses buffered records (up to `buffer.memory`). Handle SIGTERM in containers.

## Verify
- [ ] Stop the brokers in a test: the app surfaces failures after `delivery.timeout.ms` rather than reporting success.
- [ ] Oversized message test lands in the DLQ with the error reason.
- [ ] Shutdown path logs `flush` result 0 remaining.

## Checked
2026-10-28. Confirmed in the Kafka 4.0 producer config page, KafkaProducer javadoc (3.9) and the Confluent Python client docs: `retries` and `delivery.timeout.ms` semantics (retries bounded by the delivery timeout), the `ProducerFencedException` / `OutOfOrderSequenceException` / `AuthorizationException` fatal-error group, in-order callbacks, `produce()` raising `BufferError` on a full local queue, `flush()` returning the number of messages still queued, `poll()` serving callbacks. Nothing removed beyond the unversioned documentation anchor.
Method: documentation only; no commands were run.
