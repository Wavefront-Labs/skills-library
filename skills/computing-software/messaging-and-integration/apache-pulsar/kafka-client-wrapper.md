---
id: computing-software.messaging-and-integration.apache-pulsar.kafka-client-wrapper
name: kafka-client-wrapper
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [kafka-wrapper, pulsar-client-kafka, kafka-migration, bootstrap-servers, pulsar-adapters]
level: practitioner
status: docs-checked
description: "Run Kafka Java client code against Pulsar with the pulsar-client-kafka wrapper: swap the dependency, point bootstrap.servers at pulsar://, and use the original-client variant."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/adaptors-kafka.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move an application written with the Apache Kafka Java client onto Pulsar with minimal code change.

The wrapper artifacts (`pulsar-client-kafka` and `pulsar-client-kafka-original`) live in the separate `apache/pulsar-adapters` repository, not the main Pulsar release.

Steps:
1. Remove the Kafka client dependency from `pom.xml` (`org.apache.kafka:kafka-clients`).
2. Add `org.apache.pulsar:pulsar-client-kafka` (use the adapters version).
Existing code then works unchanged; adjust configuration so producers and consumers point to the Pulsar service and use a Pulsar topic.

Producer example settings: topic must be a regular Pulsar topic such as `persistent://public/default/my-topic`; `props.put("bootstrap.servers", "pulsar://localhost:6650")`; `key.serializer` and `value.serializer` as in Kafka; then `new KafkaProducer(props)` and `producer.send(new ProducerRecord<>(topic, key, value))`.

Consumer example settings: `bootstrap.servers` set to `pulsar://localhost:6650`, `group.id` set to the subscription name (`my-subscription-name`), `enable.auto.commit` false, key and value deserializers; then `consumer.subscribe(Arrays.asList(topic))`, `consumer.poll(100)` and `consumer.commitSync()`.

Migrating gradually: when the application must use the original Kafka client and the Pulsar wrapper together, use the unshaded artifact `pulsar-client-kafka-original` and construct `org.apache.kafka.clients.producer.PulsarKafkaProducer` and `org.apache.kafka.clients.producer.PulsarKafkaConsumer` instead of KafkaProducer and KafkaConsumer.

Gotcha: the Kafka group id becomes the Pulsar subscription name, so existing group names carry over as subscription names.

## Checked

2026-11-03. Confirmed against the Pulsar Kafka client wrapper page: artifacts live in `apache/pulsar-adapters`, swap `kafka-clients` for `pulsar-client-kafka`, `bootstrap.servers` and `group.id` mapping (group id is the subscription name), the producer and consumer examples (`poll`, `commitSync`), and `pulsar-client-kafka-original` with `PulsarKafkaProducer`/`PulsarKafkaConsumer`. Removed: the generic Verify line.

Method: documentation only; no commands were run.
