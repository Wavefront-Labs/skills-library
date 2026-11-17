---
id: computing-software.ai-ml-engineering.mlops.streaming-inference-kafka-flink
name: streaming-inference-kafka-flink
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, streaming-inference, kafka-inference, flink, real-time-scoring, exactly-once, consumer-lag]
level: practitioner
status: draft
description: "Score events in real time from Kafka: consumer micro-batching, offset commits after producing results, idempotent outputs, Flink async I/O to model servers, lag and DLQ handling."
sources:
  - https://docs.confluent.io/kafka-clients/python/current/overview.html
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/asyncio/
  - https://kafka.apache.org/documentation/#semantics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streaming inference with Kafka / Flink

## Python consumer with micro-batching (at-least-once)
```python
from confluent_kafka import Consumer, Producer
c = Consumer({"bootstrap.servers": BROKERS, "group.id": "fraud-scorer-v3",
              "enable.auto.commit": False, "auto.offset.reset": "latest", "max.poll.interval.ms": 300000})
p = Producer({"bootstrap.servers": BROKERS, "enable.idempotence": True, "acks": "all"})
c.subscribe(["payments"])
model = load_model()
while True:
    msgs = c.consume(num_messages=256, timeout=0.05)
    good = [m for m in msgs if not m.error()]
    if not good:
        continue
    feats = [parse(m.value()) for m in good]
    for m, s in zip(good, model.predict(feats)):
        p.produce("payment-scores", key=m.key(), value=encode(m, s, MODEL_VERSION))
    p.flush()
    c.commit(asynchronous=False)        # commit only after outputs are durably produced
```
- Commit after producing: a crash re-processes a batch (duplicates) rather than losing events. Make consumers of the output idempotent (key by event id) or use Kafka transactions (`transactional.id`, `send_offsets_to_transaction`) for exactly-once within Kafka.
- Micro-batches amortise model overhead; cap by size and time to bound latency.
- Long inference stalls polling; keep `max.poll.interval.ms` above worst-case batch time or Kafka rebalances the group.
- Bad payloads go to a dead-letter topic with the error; never block the partition.
- Scale = partitions. Consumers beyond partition count sit idle.

## Flink
Load the model in `open()` of a `RichMapFunction` for in-process models, or call a model server with **Async I/O** (`AsyncDataStream.unorderedWait(stream, asyncFn, timeout, TimeUnit.MILLISECONDS, capacity)`) so slow inference does not block the operator. Set a timeout handler that emits a fallback score. Checkpointing plus a transactional Kafka sink gives end-to-end exactly-once.

## Features at serving time
Streaming features (counts over windows) must be computed the same way as in training - share the feature definitions (feature store or the same Flink job writing to both offline and online stores) to avoid training-serving skew.

## Operate
- Monitor consumer lag (per partition), p99 end-to-end latency (event time to score time), DLQ rate and score distribution.
- Deploy new model versions under a new consumer `group.id` in shadow (write to a separate topic), compare, then switch.

## Verify
- [ ] Killing a consumer mid-batch causes duplicates but no gaps (replay test with event ids).
- [ ] Lag returns to baseline after a traffic spike within the SLO.
