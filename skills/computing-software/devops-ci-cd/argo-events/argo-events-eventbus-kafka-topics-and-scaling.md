---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-kafka-topics-and-scaling
name: argo-events-eventbus-kafka-topics-and-scaling
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, kafka, topics, partitions, trigger-topic, action-topic, scaling, eventbus]
level: sme
status: docs-checked
description: "Plan Kafka EventBus topics: the event, trigger and action topics per Sensor, naming rules, partition counts and when to use multiple EventBuses."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/kafka.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus kafka topics and scaling

A Kafka EventBus needs one event topic plus a trigger topic and an action topic per Sensor. They are not created automatically unless the broker has `auto.create.topics.enable=true`; if a topic is missing the EventSource or Sensor exits with an error.

Roles:
- Event topic: EventSources produce CloudEvents keyed by `{source}.{subject}`; Sensors consume via a consumer group and pick events matching their dependencies.
- Trigger topic: Sensor transaction coordination; the evaluated trigger state is written here, enabling exactly-once processing across Sensor replicas.
- Action topic: records completed actions (such as creating a Workflow or sending an HTTP request) to prevent duplicates after restart or rebalance.

Naming: by default `{namespace}-{eventbus-name}`, `{namespace}-{eventbus-name}-{sensor-name}-trigger` and `...-action`. If `spec.kafka.topic` is set, they are `{topic}`, `{topic}-{sensor-name}-trigger` and `{topic}-{sensor-name}-action`.

Partitions: the event topic partition count sets maximum Sensor consumer parallelism, so use at least the number of Sensor replicas; trigger and action topics need few (1 to 3).

One EventBus is enough for most cases. Use separate ones to isolate teams or environments, to give streams different throughput or retention needs, or different TLS and SASL settings. Sensors on Kafka scale horizontally with replicas above one; EventSources cannot necessarily be scaled active-active (see the EventSource HA page).

## Checked

2026-11-04. Confirmed against the Kafka EventBus page, Topics and Horizontal Scaling sections: the three topics and their roles, `auto.create.topics.enable`, the exit-with-error behaviour, both naming tables, partition guidance (at least the Sensor replica count; 1-3 for trigger and action), single versus separate EventBus guidance, and Sensor scaling. Softened the EventSource scaling sentence to the page's wording.
Method: documentation only; no commands were run.
