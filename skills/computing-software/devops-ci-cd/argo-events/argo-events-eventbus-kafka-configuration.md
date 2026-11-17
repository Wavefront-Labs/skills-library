---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-kafka-configuration
name: argo-events-eventbus-kafka-configuration
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, kafka, eventbus, sasl, tls, consumer-group, partitioner, topics]
level: advanced
status: docs-checked
description: "Configure a Kafka EventBus: broker url, topic, TLS, SASL, consumer group, rebalance strategy, startOldest and partitioner."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/kafka.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus kafka configuration

Use a Kafka EventBus if you have many events and want to scale Sensors horizontally; use JetStream to get started quickly. The Kafka cluster must be managed independently and topics must exist (unless auto create is enabled).

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: default
spec:
  kafka:
    url: kafka:9092
    topic: "example"
```

Properties:
- `url`: comma-separated broker URLs.
- `topic`: defaults to `{namespace-name}-{eventbus-name}`.
- `version`: Kafka version; usually leave unset (defaults to the oldest supported stable version).
- `tls`: `caCertSecret`, `clientCertSecret`, `clientKeySecret`, each a Secret name and key.
- `sasl`: `mechanism` (for example PLAIN), `userSecret` and `passwordSecret`.
- `consumerGroup.groupName`: defaults to `{namespace-name}-{sensor-name}`.
- `consumerGroup.rebalanceStrategy`: sticky, roundrobin or range (default range).
- `consumerGroup.startOldest`: for a new group, start at the oldest event (true) or newest (false, default).
- `partitioner`: random (default), hash, roundrobin or manual.

TLS or SASL must also be enabled in the Kafka cluster, with certificates or credentials stored in a Kubernetes Secret.

## Checked

2026-11-04. Confirmed against the Kafka EventBus page: when to choose Kafka, the example, and each property with its default (`url`, `topic`, `version`, `tls`, `sasl`, `consumerGroup.groupName`, `rebalanceStrategy`, `startOldest`, `partitioner`) plus the Security paragraph. Nothing removed.
Method: documentation only; no commands were run.
