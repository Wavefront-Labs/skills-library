---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-ha-leader-election
name: argo-events-sensor-ha-leader-election
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, sensor, high-availability, leader-election, kafka, leases, replicas]
level: advanced
status: docs-checked
description: "Run Sensors with more than one replica (active-passive) and choose NATS or Kubernetes leader election, noting Kafka Sensors scale horizontally."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/ha.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor ha leader election

The Sensor controller creates a Deployment (default 1 replica) per Sensor. Setting `spec.replicas` above 1 gives an Active-Passive setup: one pod serves, the rest stand by, and a standby is elected automatically if the active pod goes away. Do not scale the Deployment by hand; set `spec.replicas`.

Leader election defaults to NATS. With a Kafka EventBus no leader election is needed, because a Sensor on Kafka can scale horizontally and all replicas actively process events. For other buses you can opt in to Kubernetes native leader election with the annotation `events.argoproj.io/leader-election: k8s`, and grant the Sensor ServiceAccount a Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-events-leaderelection-role
rules:
  - apiGroups: ["coordination.k8s.io"]
    resources: ["leases"]
    verbs: ["get", "create", "update"]
```

Setting `spec.replicas: 0` keeps the Sensor but executes no triggers until scaled back up (HA/DR Recommendations page). The DR/HA recommendations page covers more.

## Checked

2026-11-04. Confirmed against the Sensor High Availability page (default one replica, Active-Passive with `spec.replicas` above 1, automatic election, no manual scaling, NATS default, no election needed with a Kafka EventBus, the `events.argoproj.io/leader-election: k8s` annotation and the `leases` Role) and the HA/DR Recommendations page (`replicas: 0`). "All replicas actively process events" on Kafka is from the Kafka EventBus page. Nothing removed.
Method: documentation only; no commands were run.
