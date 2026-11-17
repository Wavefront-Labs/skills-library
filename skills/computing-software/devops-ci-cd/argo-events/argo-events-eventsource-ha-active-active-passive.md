---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventsource-ha-active-active-passive
name: argo-events-eventsource-ha-active-active-passive
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, high-availability, active-active, active-passive, leader-election, replicas, eventsource]
level: advanced
status: docs-checked
description: "Pick the right HA strategy per EventSource type, and use Kubernetes leader election instead of NATS when required."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/ha.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventsource ha active active passive

The EventSource controller creates a Deployment (replicas default 1) per EventSource. HA means setting `spec.replicas` above 1, never scaling it manually, which can cause unexpected behaviour. Some sources forbid multiple live clients with the same attributes (for example the same NATS `clientID`) or would emit duplicates, so strategies differ.

Active-Active (all pods serve traffic): AWS SNS, AWS SQS, Bitbucket, Bitbucket Server, GitHub, GitLab, NetApp StorageGRID, Slack, Stripe, Webhook.

Active-Passive (one active pod, the rest standby with automatic election): AMQP, Azure Events Hub, Calendar, Emitter, GCP PubSub, Generic, File, HDFS, Kafka, Minio, MQTT, NATS, NSQ, Pulsar, Redis, Resource.

Active-active types cannot be mixed with active-passive types in one EventSource (EventSource With Multiple Events page).

Leader election uses NATS by default, except with a Kafka EventBus where Kubernetes leader election is used. On other buses opt in with the annotation:

```yaml
annotations:
  events.argoproj.io/leader-election: k8s
```

and bind the EventSource ServiceAccount to a Role allowing `get`, `create` and `update` on `leases` in `coordination.k8s.io`. An EventSource on a Kafka bus cannot necessarily scale active-active (Kafka EventBus page).

## Checked

2026-11-04. Confirmed against the EventSource High Availability page: default of one replica, `spec.replicas`, the warning against manual scaling, both type lists, election of a standby pod, NATS default versus Kubernetes leader election with a Kafka EventBus, the `events.argoproj.io/leader-election: k8s` annotation and the `leases` Role (get, create, update). The no-mixing rule and the Kafka caveat come from the Multiple Events and Kafka EventBus pages. Nothing removed.
Method: documentation only; no commands were run.
