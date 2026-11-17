---
id: computing-software.devops-ci-cd.argo-rollouts.canary-dynamic-stable-scale
name: canary-dynamic-stable-scale
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [canary, dynamicstablescale, abortscaledowndelayseconds, cost, traffic-routing, argo-rollouts]
level: advanced
status: docs-checked
description: "Scale the stable ReplicaSet down as canary traffic grows to avoid doubling pod counts during a traffic-routed canary."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/canary/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With a traffic router, the stable ReplicaSet stays scaled to 100% for the whole update. That gives instant rollback because traffic can shift back immediately, but costs roughly double the pods, similar to blue-green.

Set `dynamicStableScale: true` (available since v1.1) to shrink stable as canary weight rises, useful for high replica counts or bare-metal clusters without spare capacity:

```yaml
spec:
  strategy:
    canary:
      dynamicStableScale: true
```

Trade-off: if the rollout is aborted while this is on, the canary ReplicaSet scales down dynamically as traffic returns to stable. To keep the canary running after an abort (to debug it), set an explicit delay:

```yaml
    canary:
      dynamicStableScale: true
      abortScaleDownDelaySeconds: 600
```

`abortScaleDownDelaySeconds` defaults to 30 seconds for traffic-routed canaries; 0 means canary pods are not scaled down. `minPodsPerReplicaSet` (default 1) keeps each ReplicaSet highly available, and takes full effect only when `spec.replicas` is at least that value.

Note the docs: `maxSurge` and `maxUnavailable` apply only to basic canary. With `trafficRouting` set, the stable ReplicaSet is at full scale, so total pods can exceed twice `spec.replicas`; use `dynamicStableScale` and `setCanaryScale` instead.

Verify by comparing ReplicaSet sizes at each step in `kubectl argo rollouts get rollout NAME -w`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/canary/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
