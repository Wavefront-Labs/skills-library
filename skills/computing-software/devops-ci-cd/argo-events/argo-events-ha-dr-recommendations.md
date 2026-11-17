---
id: computing-software.devops-ci-cd.argo-events.argo-events-ha-dr-recommendations
name: argo-events-ha-dr-recommendations
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, high-availability, disaster-recovery, persistence, anti-affinity, pdb, replicas]
level: advanced
status: docs-checked
description: "Harden a production Argo Events install with persistent volumes, anti-affinity, pod priority, a PodDisruptionBudget and replica settings for EventSources and Sensors."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/dr_ha_recommendations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events ha dr recommendations

A minimal bus (`spec.nats.native` with `auth: token`) is not enough for production. The page's EventBus recommendations all use the NATS `native` bus:

EventBus:
- Persistent volumes (for example `storageClassName: standard`, `ReadWriteOnce`, `20Gi`) avoid event loss when pods crash, even though pods sync data between them.
- Anti-affinity so a disaster cannot take all pods: best effort via `preferredDuringSchedulingIgnoredDuringExecution` or a hard `requiredDuringSchedulingIgnoredDuringExecution` rule matching labels `controller: eventbus-controller` and `eventbus-name: default`. Use `topologyKey: topology.kubernetes.io/zone` instead of `kubernetes.io/hostname` for availability-zone spread. `nodeSelector` and `tolerations` are also settable.
- Pod priority through `priorityClassName` or `priority` to reduce eviction.
- A `PodDisruptionBudget` with `maxUnavailable: 1` for a 3-replica bus, selecting the same labels (change the name if your bus is not `default`).

EventSources and Sensors: set `spec.replicas` above 1 for HA (default 1). `replicas: 0` keeps the object but runs no pods: useful as the passive side of active-passive DR; a webhook EventSource Service then has no endpoints and requests fail, and a Sensor executes no triggers. Pod `affinity`, `nodeSelector`, `tolerations`, `priorityClassName` and `priority` go under `spec.template`.

## Checked

2026-11-04. Confirmed against the HA/DR Recommendations page: the `native` examples, persistent volume values, both anti-affinity forms with labels and `topologyKey` values, `nodeSelector`/`tolerations`/priority fields, the PodDisruptionBudget, and `spec.replicas` behaviour (default 1, 0 keeps the object but runs no pods) for EventSources and Sensors, with the `spec.template` fields. Nothing removed; the opening sentence now says the EventBus examples are for the NATS native bus.
Method: documentation only; no commands were run.
