---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.kafka-logger-plugin
name: kafka-logger-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, kafka-logger, kafka, logging, sasl, producer, plugin]
level: advanced
status: docs-checked
description: "Send APISIX logs to Kafka with kafka-logger: brokers and SASL, kafka_topic, producer_type, required_acks, meta_format, producer batching defaults and api_version."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/kafka-logger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kafka-logger plugin

Required: `brokers` (each with `host` and `port`) and `kafka_topic`.

Defaults:
- `brokers.sasl_config.mechanism`: `PLAIN` (also `SCRAM-SHA-256`, `SCRAM-SHA-512`); `user` and `password` required if SASL is set.
- `tls.verify`: false.
- `producer_type`: `async` (or `sync`).
- `required_acks`: 1 (allowed 1 or -1; 0 is not allowed).
- `timeout`: 3 seconds; `key`: partition key.
- `meta_format`: `default` (JSON) or `origin` (raw HTTP).
- `log_format`, `log_format_extra`, `include_req_body`, `include_resp_body` and body byte limits (524288) work as in other loggers.
- `producer_batch_num` 200, `producer_batch_size` 1048576, `producer_max_buffering` 50000, `producer_time_linger` 1 second.
- `meta_refresh_interval`: 30; `cluster_name`: 1 (async only).
- `api_version`: 1 (0, 1 or 2); use 2 to store message timestamps.
- `broker_list` is deprecated; use `brokers`.

```json
{
  "kafka-logger": {
    "brokers": [ { "host": "127.0.0.1", "port": 9092 } ],
    "kafka_topic": "test2",
    "key": "key1",
    "producer_type": "async",
    "required_acks": 1,
    "meta_format": "default",
    "batch_max_size": 1
  }
}
```

## Checked

2026-11-04. Confirmed against the APISIX kafka-logger plugin page: brokers and SASL mechanisms, tls.verify, producer_type, required_acks values, timeout, meta_format, producer batching defaults, meta_refresh_interval, cluster_name (async only), api_version values and the timestamp note, the deprecated broker_list, batch_max_size in the example. Nothing removed.

Method: documentation only; no commands were run.
