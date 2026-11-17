---
id: computing-software.devops-ci-cd.argo-rollouts.anti-affinity-for-autoscaler-churn
name: anti-affinity-for-autoscaler-churn
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [antiaffinity, cluster-autoscaler, blue-green, node-scaling, scheduling, canary, argo-rollouts]
level: advanced
status: docs-checked
description: "Inject pod anti-affinity so new ReplicaSet pods avoid nodes with the old version and survive autoscaler scale-down."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/anti-affinity/anti-affinity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: blue-green (or canary with traffic management) briefly doubles pod count. The cluster autoscaler adds a node; when the old version scales down the autoscaler removes a now-empty node, and pods that ended up on it are deleted and recreated. This is most common when a Rollout has a dedicated instance group.

Solution: have the Rollout inject a `PodAntiAffinity` into the new ReplicaSet so new pods cannot share nodes with the previous version. Then the nodes that get scaled down hold only old pods, and the new pods are never disturbed.

Enable it with the `antiAffinity` struct in the blue-green or canary strategy:

```yaml
strategy:
  blueGreen:
    antiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution: {}
```

or the soft form with a weight from 1 to 100:

```yaml
    antiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        weight: 1
```

`requiredDuringSchedulingIgnoredDuringExecution` demands that the new version's pods land on different nodes than the previous version's; if impossible they are not scheduled. The preferred form only tries to separate them and still schedules the pods if it cannot.

Existing affinity rules on the ReplicaSet are not modified.

Trade-off: deployments can take longer because new nodes are more likely to be created to satisfy the anti-affinity rules, most often when a rollout has its own dedicated instance group.

Verify: the new ReplicaSet's pod template shows the injected podAntiAffinity.

## Checked

2026-11-08. Confirmed against the Argo Rollouts anti-affinity page (read in full): the autoscaler churn mechanism, antiAffinity in blueGreen or canary, required and preferred forms, weight 1 to 100, existing affinity untouched.

Removed or corrected: removed the unsourced advice to specify only one form, replaced the tight-cluster stall trade-off with the documented longer-deployment trade-off, and removed the kubectl verify command.

Method: documentation only; no commands were run.
