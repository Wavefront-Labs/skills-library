---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kafka-to-loki-ingestion
name: kafka-to-loki-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-source-kafka, kafka-to-loki, loki-ingest, grafana-alloy, kafka]
level: practitioner
status: docs-checked
description: "Consume logs from Kafka topics into Loki with Alloy loki.source.kafka: consumer group, labels from topic and key via loki.relabel, SASL or TLS authentication."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.kafka/", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.relabel/", "https://grafana.com/docs/loki/latest/send-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka to Loki ingestion

`loki.source.kafka` reads messages from Kafka using a consumer group and forwards them to other `loki.*` components.
Kafka needs at least one producer writing to at least one topic.

## Alloy
```alloy
loki.source.kafka "logs" {
  brokers                = ["kafka-0:9092", "kafka-1:9092"]
  topics                 = ["app-logs", "audit-logs"]
  group_id               = "alloy-loki"
  use_incoming_timestamp = true
  labels                 = {job = "kafka"}
  relabel_rules          = loki.relabel.kafka.rules
  forward_to             = [loki.write.default.receiver]
  authentication {
    type = "sasl"
    sasl_config {
      user     = "alloy"
      password = sys.env("KAFKA_PASSWORD")
      use_tls  = true
    }
  }
}

loki.relabel "kafka" {
  forward_to = []
  rule {
    source_labels = ["__meta_kafka_topic"]
    target_label  = "topic"
  }
}
```
Notes from the component reference:
- Required arguments are `brokers`, `topics` and `forward_to`. `group_id` defaults to `loki.source.kafka`;
  `use_incoming_timestamp` defaults to false; `assignor` is `range`, `roundrobin` or `sticky` (default `range`).
- A topic starting with `^` is treated as a regular expression and may match several topics.
- `labels` are applied to every message. Internal labels available for relabelling: `__meta_kafka_group_id`,
  `__meta_kafka_member_id`, `__meta_kafka_message_key`, `__meta_kafka_message_offset`, `__meta_kafka_partition`,
  `__meta_kafka_topic`. All labels starting with `__` are removed before forwarding unless relabelled through a
  `loki.relabel` component passed in `relabel_rules`.
- `authentication.type` is `none`, `ssl` or `sasl`; `ssl` needs a `tls_config` block and `sasl` needs `sasl_config`
  (`mechanism` default `PLAIN`, `user`, `password`, `use_tls`). Client certificate and key must both be given.
- Avoid unbounded values (message key, partition, offset) as Loki labels.

## Checked
2026-11-01. Confirmed on the loki.source.kafka reference page: arguments, defaults, meta labels, authentication and
sasl_config fields. Removed: the `version` pin, SCRAM mechanism example, loki.process JSON parsing stages, consumer
scaling and lag-metric advice, rejection behaviour of old timestamps.
Method: documentation only; no commands were run.
