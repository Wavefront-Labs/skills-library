---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-kafka-at-least-once
name: jaeger-kafka-at-least-once
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, message-marking, wait-for-result, block-on-overflow, retry-on-failure]
level: sme
status: docs-checked
description: "Configure the Kafka ingester for at-least-once delivery with message_marking.after, wait_for_result and unbounded retries."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/kafka/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid losing spans Kafka already delivered when storage is down.

By default the Kafka receiver commits an offset as soon as the pipeline accepts the record, which happens before the storage writes, so a backend outage loses spans Kafka considers delivered. To commit only after spans are durable:
```
receivers:
  kafka:
    message_marking:
      after: true
      on_error: false
exporters:
  jaeger_storage_exporter:
    trace_storage: some_storage
    retry_on_failure:
      enabled: true
      max_elapsed_time: 0
    queue:
      wait_for_result: true
      block_on_overflow: true
      sizer: bytes
      num_consumers: 1
      queue_size: 104857600
      batch:
        sizer: bytes
        flush_timeout: 200ms
        min_size: 1048576
        max_size: 4194304
```
Also no batch processor in the pipeline. `max_elapsed_time: 0` means never give up on a batch, because giving up pauses the partition. `block_on_overflow: true` makes a full queue wait instead of failing the record.

The storage must return errors: Cassandra and ClickHouse always do; Elasticsearch and OpenSearch need `write_mode: sync` and should use `poison_pill_handling: drop` or the dead-letter pipeline so a permanently rejected document cannot hold the offset forever. Reference configs: config-kafka-ingester-sync.yaml and config-kafka-ingester-dead-letter.yaml.

## Checked

2026-11-08: read the whole Kafka page (raw markdown from the jaegertracing/documentation repo, v2/2.22), including the At-least-once delivery and Sizing sections. Confirmed the config block, the explanations and the storage requirements. The linked Delivery Guarantees page was not used for any claim here.

Method: documentation only; no commands were run.
