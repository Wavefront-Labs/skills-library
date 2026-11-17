---
id: computing-software.cloud-infrastructure-engineering.knative.kafka-source
name: kafka-source
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [kafkasource, kafka-topic, strimzi, kafka-source-dispatcher, partition-order]
level: practitioner
status: docs-checked
description: "Install the KafkaSource controller and read Kafka topics into CloudEvents sent to a sink."
sources:
  - https://knative.dev/docs/eventing/sources/kafka-source/
  - https://knative.dev/docs/eventing/configuration/keda-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: consume messages from existing Kafka topics and deliver them as CloudEvents.

The `KafkaSource` reads messages stored in existing Apache Kafka topics and sends them as CloudEvents over HTTP to its configured `sink`. It preserves the order of messages in the topic partitions by waiting for a successful response from the sink before delivering the next message in the same partition.

Install:
1. Apply the `eventing-kafka-controller.yaml` release file from the knative-extensions `eventing-kafka-broker` repository.
2. Apply `eventing-kafka-source.yaml`, the Kafka Source data plane, from the same repository.
3. Verify with `kubectl get deployments.apps,statefulsets.apps -n knative-eventing` that the `kafka-controller` deployment and the `kafka-source-dispatcher` statefulset are running.

Optional topic creation: the page assumes Strimzi operates Kafka and shows a `KafkaTopic` with label `strimzi.io/cluster: my-cluster`, 3 partitions, 1 replica, `retention.ms: 7200000` and `segment.bytes: 1073741824`. Equivalent operations can be done with the Apache Kafka CLI or any other tool.

Operational notes:
- Order is kept per partition only, as the sink must answer before the next message of that partition goes out.
- KEDA autoscaling is an Alpha feature; enabling it turns on scaling for all KafkaSources, Triggers referencing Kafka Brokers and Subscriptions referencing KafkaChannels.
- Consumption starts from the latest offset by default; `spec.initialOffset` accepts `earliest` or `latest` and is honoured only when the consumer group has no committed offsets.
- Scale consumers with `kubectl scale kafkasource` or the `spec.consumers` field.
- The key deserializer is chosen with the label `kafkasources.sources.knative.dev/key-type`: `string` (default), `int`, `float` or `byte-array`.

## Checked

2026-11-04. Confirmed against the Knative Source for Apache Kafka page and the KEDA configuration page (knative/docs source): what `KafkaSource` does and its per-partition ordering, the two apply commands for the controller and data plane, the `kafka-controller` deployment and `kafka-source-dispatcher` statefulset check, the Strimzi `KafkaTopic` values (label, 3 partitions, 1 replica, `retention.ms`, `segment.bytes`), and KEDA being Alpha. Added `initialOffset`, scaling and key-type facts from the same page and corrected the KEDA scope: it applies to KafkaSources, Triggers on Kafka Brokers and Subscriptions on KafkaChannels, not only to the dispatcher. Nothing removed.

Method: documentation only; no commands were run.
