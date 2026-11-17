---
id: computing-software.messaging-and-integration.apache-pulsar.kafka-sink-connector
name: kafka-sink-connector
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [kafka-sink, bootstrap-servers, producer-config-properties, acks, pulsar-io]
level: practitioner
status: docs-checked
description: "Configure the Pulsar IO Kafka sink: bootstrapServers, topic, acks, security options, batch and request size defaults, serializers and producerConfigProperties precedence."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/io-kafka-sink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pull messages from Pulsar topics and write them to Kafka topics.

The connector is downloaded from the Pulsar download page. Configure it with a JSON or YAML file under `configs`.

Required properties: `bootstrapServers` (comma-separated host:port list for the initial Kafka connection), `acks` (acknowledgments the producer needs from the leader; controls durability), `topic` (the Kafka target topic).

Optional properties and defaults:
- `securityProtocol`, `saslMechanism`, `saslJaasConfig` (JAAS login parameters), `sslEnabledProtocols`, `sslEndpointIdentificationAlgorithm`, `sslTruststoreLocation`, `sslTruststorePassword`: all empty by default.
- `batchsize`: 16384 (bytes a Kafka producer tries to batch together).
- `maxRequestSize`: 1048576 bytes.
- `keyDeserializationClass`: `org.apache.kafka.common.serialization.StringSerializer` (the serializer class for keys, despite the property name).
- `valueDeserializationClass`: `org.apache.kafka.common.serialization.ByteArraySerializer` for values.
- `producerConfigProperties`: map of raw Kafka producer settings. Other properties in the connector configuration take precedence over it.

YAML example:
```yaml
configs:
  bootstrapServers: "localhost:6667"
  topic: "test"
  acks: "1"
  batchSize: "16384"
  maxRequestSize: "1048576"
  producerConfigProperties:
    client.id: "test-pulsar-producer"
    security.protocol: "SASL_PLAINTEXT"
    sasl.mechanism: "GSSAPI"
    sasl.kerberos.service.name: "kafka"
    acks: "all"
```

Note: the page's example sets `acks` both at top level and inside `producerConfigProperties`; since other connector properties take precedence, the top-level value applies. The property table spells the batch property `batchsize` while the examples use `batchSize`.

## Checked

2026-11-03. Confirmed against the pulsar-site page io-kafka-sink: required properties, defaults, serializer defaults, `producerConfigProperties` precedence note and the YAML example. Removed the secrets advice and the invented Verify step.

Method: documentation only; no commands were run.
