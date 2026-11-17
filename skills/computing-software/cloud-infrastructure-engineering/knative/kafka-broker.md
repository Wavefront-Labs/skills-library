---
id: computing-software.cloud-infrastructure-engineering.knative.kafka-broker
name: kafka-broker
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [kafka-broker, kafka, ordered-delivery, data-plane, broker-class]
level: advanced
status: docs-checked
description: "Know what the native Kafka Broker offers: HA control plane, scalable data plane and ordered delivery."
sources:
  - https://knative.dev/docs/eventing/brokers/broker-types/kafka-broker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide when to use the Knative Broker for Apache Kafka and what it provides.

The Kafka Broker is a native Kafka implementation of the Knative Broker API. Its features are:
- Control plane high availability.
- A horizontally scalable data plane.
- Extensively configurable behavior.
- Ordered delivery of events, based on the CloudEvents partitioning extension.
- Support for any Kafka version, from earlier versions to the newest.
- Two data plane modes: isolated per namespace, or shared.

Events are stored as Kafka records in binary content mode.

Before creating a Broker, ask your administrator to install the Knative Kafka Broker.

Select the class with the case-sensitive annotation `eventing.knative.dev/broker.class`:
- `Kafka`: shared data plane. The `kafka-broker-receiver` and `kafka-broker-dispatcher` deployments in `knative-eventing` serve all such Brokers.
- `KafkaNamespaced`: the controller creates a data plane per namespace that has a Broker, isolating them at the cost of more deployments and resources. Its `spec.config` ConfigMap must live in the Broker's namespace.

Ordering is set per Trigger with the annotation `kafka.eventing.knative.dev/delivery.order`: `unordered` (the default, non-blocking) or `ordered` (a per-partition blocking consumer that waits for the subscriber's successful response before the next message of that partition).

`spec.config` points at a ConfigMap such as `kafka-broker-config` in `knative-eventing`. An optional annotation `kafka.eventing.knative.dev/external.topic` points the Broker at an externally managed topic.

## Checked

2026-11-04. Confirmed against the Knative Broker for Apache Kafka page (knative/docs source): the notable-features list, binary content mode storage, the installation prerequisite, the case-sensitive `eventing.knative.dev/broker.class` annotation with `Kafka` and `KafkaNamespaced`, the shared versus per-namespace data plane (`kafka-broker-receiver` and `kafka-broker-dispatcher`), the resource trade-off, the `spec.config` ConfigMap rule for `KafkaNamespaced`, and the optional `kafka.eventing.knative.dev/external.topic` annotation. Added the delivery-order annotation and its two values from the same page. Nothing removed.

Method: documentation only; no commands were run.
