---
id: computing-software.cloud-infrastructure-engineering.keda.idle-min-max-replica-counts
name: idle-min-max-replica-counts
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [idlereplicacount, minreplicacount, maxreplicacount, scale-to-zero, replica-bounds]
level: practitioner
status: docs-checked
description: "Understand minReplicaCount, maxReplicaCount and idleReplicaCount in a ScaledObject, including the constraint that idleReplicaCount can only be 0."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three fields bound the replicas of a ScaledObject target.

`minReplicaCount` (default 0) is the floor KEDA scales down to. Set it to `n` if you always need at least `n` pods. When it is 1 or higher the scaler is always considered active, so any activation threshold is ignored.

`maxReplicaCount` (default 100) is passed straight into the generated HPA as its maximum.

`idleReplicaCount` is optional and ignored by default. If set it must be less than `minReplicaCount`, and the documentation warns that because of HPA controller limitations the only supported value is 0; any other value will not work correctly. The behaviour: with no trigger activity the workload sits at the idle count; when activity appears KEDA immediately scales it to `minReplicaCount`, then the HPA takes over up to the maximum; when activity stops it drops back to the idle count. Example from the page: idle 0, min 10, max 100.

Choosing: if you only need a floor, omit `idleReplicaCount` and set `minReplicaCount`. If you need "off when idle, warm pool of 10 when busy", use idle 0 with min 10. CPU and memory only ScaledObjects on a Deployment or StatefulSet cannot use `minReplicaCount: 0`; the admission webhook rejects that.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification and webhook rules: defaults, idleReplicaCount limitation to 0, the idle 0 and min 10 example, CPU/memory minReplicaCount 0 rejection.

Method: documentation only; no commands were run.
