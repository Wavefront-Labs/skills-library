---
id: computing-software.cloud-infrastructure-engineering.keda.pause-scaledobject-autoscaling
name: pause-scaledobject-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [autoscaling-keda-sh-paused, paused-replicas, pause-autoscaling, maintenance]
level: practitioner
status: docs-checked
description: "Pause a ScaledObject with the autoscaling.keda.sh/paused and paused-replicas annotations for maintenance, and know what happens when both are set."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pausing is preferable to deleting a ScaledObject: the workload and its instances stay, but KEDA stops adjusting them. Typical reasons are cluster maintenance or relieving resource starvation by freezing non-critical workloads. Add annotations to the ScaledObject:

```yaml
metadata:
  annotations:
    autoscaling.keda.sh/paused-replicas: "0"
    autoscaling.keda.sh/paused: "true"
```

The two annotations serve different purposes:
- `autoscaling.keda.sh/paused: "true"` pauses scaling immediately and keeps the current instance count.
- `autoscaling.keda.sh/paused-replicas: "<number>"` first scales the workload to that number of replicas, then pauses. Any number is allowed, not only 0.

Typically you use one or the other. If both are present, KEDA scales to the `paused-replicas` count and then pauses. The presence of these annotations pauses autoscaling regardless of the replica number provided.

Pausing takes the instances out of operation without touching the application objects themselves. To resume, remove all paused annotations. If you paused with `autoscaling.keda.sh/paused`, you can instead set it to `false`. For ScaledJobs the equivalent is the single `autoscaling.keda.sh/paused` annotation (see scaledjob-overview-and-pausing).

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Deployments and Scaling Jobs pages: paused and paused-replicas annotations and their combination, unpausing.

Method: documentation only; no commands were run.
