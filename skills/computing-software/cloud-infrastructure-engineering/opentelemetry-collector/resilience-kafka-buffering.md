---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.resilience-kafka-buffering
name: resilience-kafka-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, resiliency, kafka, buffer, exporter, receiver]
level: sme
status: docs-checked
description: "Decouple Collector tiers with Kafka as a durable buffer using the kafka exporter and receiver."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/kafkareceiver/README.md
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/kafkaexporter/README.md
  - https://opentelemetry.io/docs/collector/resiliency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The resiliency page recommends a message queue such as Kafka for the highest resilience, especially between tiers like Agent and Gateway. An agent exports to a Kafka topic and a gateway consumes it. If the gateway is down, messages accumulate in the topic up to Kafka's retention limits and the agent is unaffected while Kafka is up. If Kafka itself is down, the producer needs its own sending queue, possibly with a WAL.

Agent (producer):

```yaml
exporters:
  kafka:
    brokers: ['kafka-broker1:9092', 'kafka-broker2:9092']
    traces:
      topic: otlp_spans
```

Gateway (consumer):

```yaml
receivers:
  kafka:
    brokers: ['kafka-broker1:9092', 'kafka-broker2:9092']
    traces:
      topics: [otlp_spans]
    initial_offset: earliest
```

Details from the component READMEs:

- Defaults: `brokers` localhost:9092; topics `otlp_spans`, `otlp_metrics`, `otlp_logs`; `encoding` `otlp_proto`; receiver `group_id` `otel-collector`.
- `initial_offset` (default `latest`, or `earliest`) applies only when no offset was committed, so `earliest` processes the backlog.
- Loss is tied to Kafka failure, misconfiguration, expiry, or a producer without local buffering.
- The page notes the operational cost and need for Kafka expertise.
- The resiliency page's own example uses a single `topic: otlp_traces` key on both components; the current component READMEs use per-signal blocks (exporter `topic`, receiver `topics`) as shown above.

## Checked

Method: docs-checked 2026-11-09 against the resiliency page, the kafka exporter README and the kafka receiver README (raw markdown, read in full or by settings section).
