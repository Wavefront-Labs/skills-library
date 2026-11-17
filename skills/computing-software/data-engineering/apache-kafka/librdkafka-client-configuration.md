---
id: computing-software.data-engineering.apache-kafka.librdkafka-client-configuration
name: librdkafka-client-configuration
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, librdkafka, confluent-kafka-python, confluent-kafka-go, kafka-producer, kafka-consumer, poll, flush, client-configuration]
level: practitioner
status: docs-checked
description: "Configure librdkafka-based clients (confluent-kafka-python, Go, .NET, node-rdkafka): config names that differ from Java, poll/flush rules, delivery reports and debug logging."
sources:
  - https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
  - https://docs.confluent.io/kafka-clients/python/current/overview.html
  - https://github.com/confluentinc/librdkafka/blob/master/INTRODUCTION.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# librdkafka client configuration

**Goal:** run Python/Go/.NET/C Kafka clients built on librdkafka correctly. They look like the Java client but behave differently in key places.

## Producer (confluent-kafka-python)
```python
from confluent_kafka import Producer
p = Producer({
    "bootstrap.servers": BS,
    "enable.idempotence": True,
    "linger.ms": 20,                 # default 5 ms in librdkafka 1.x+
    "compression.type": "zstd",
    "queue.buffering.max.messages": 200000,
    "message.timeout.ms": 300000,    # = Java delivery.timeout.ms
})
def on_delivery(err, msg):
    if err: log.error("delivery failed %s key=%s", err, msg.key())
for rec in records:
    while True:
        try:
            p.produce("orders", key=rec.key, value=rec.value, on_delivery=on_delivery); break
        except BufferError:          # local queue full
            p.poll(1)
    p.poll(0)                        # serve delivery callbacks
p.flush(30)                          # MUST call before exit, else queued messages are lost
```
Delivery callbacks only fire from `poll()`/`flush()`. No poll -> queue fills -> `BufferError`.

## Consumer
```python
from confluent_kafka import Consumer, KafkaException
c = Consumer({
    "bootstrap.servers": BS, "group.id": "billing",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True, "enable.auto.offset.store": False,   # commit only what you processed
    "partition.assignment.strategy": "cooperative-sticky",
    "max.poll.interval.ms": 300000,
})
c.subscribe(["orders"])
try:
    while running:
        msg = c.poll(1.0)
        if msg is None: continue
        if msg.error(): raise KafkaException(msg.error())
        process(msg)
        c.store_offsets(msg)          # auto-commit thread commits stored offsets
finally:
    c.close()                         # leave group cleanly, commit final offsets
```
`enable.auto.offset.store=false` + `store_offsets` gives at-least-once with background commits, the idiomatic librdkafka pattern.

## Config name differences from Java
| Java | librdkafka |
|---|---|
| `delivery.timeout.ms` | `message.timeout.ms` (alias `delivery.timeout.ms` accepted) |
| `buffer.memory` | `queue.buffering.max.kbytes` / `.messages` |
| `max.poll.records` | n/a: `poll()` returns one message |
| `fetch.min.bytes` | `fetch.min.bytes` (same) |
| SASL OAuth via JAAS | `sasl.mechanism=OAUTHBEARER` + `oauth_cb` / `sasl.oauthbearer.method=oidc` |

## Debugging
```python
{"debug": "broker,topic,msg", "log_level": 7}     # or "debug": "consumer,cgrp" for group issues
```
`stats_cb` + `statistics.interval.ms` (0 disables, granularity 1000 ms) emits librdkafka statistics; the application must register the stats callback.

## Gotchas
- `message.timeout.ms` is enforced locally and limits how long a produced message waits for successful delivery (0 is infinite); when messages time out, enable `debug` to see why.
- One consumer instance per thread: do not share a single consumer across threads (Confluent Python client docs).

## Checked
2026-10-28. Confirmed against librdkafka CONFIGURATION.md: `linger.ms` default 5, `queue.buffering.max.messages`/`.kbytes`, `message.timeout.ms` default 300000, `enable.auto.offset.store`, `max.poll.interval.ms` default 300000, `statistics.interval.ms`, `sasl.oauthbearer.method` (default, oidc), `compression.type` values, `enable.idempotence`; and against INTRODUCTION.md and the Confluent Python client docs: disabling the automatic offset store and calling `store_offsets` after processing. Removed: fork, GIL-callback, `consume(num_messages)`, error-string and statistics-content claims that no fetched page states.
Method: documentation only; no commands were run.

## Verify
- [ ] Graceful shutdown path calls `flush()` (producer) / `close()` (consumer).
- [ ] Delivery error callback is wired to alerting; the local producer queue does not keep growing.
