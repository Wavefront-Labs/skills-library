---
id: computing-software.devops-ci-cd.flux.controller-sharding
name: controller-sharding
category: computing-software
field: devops-ci-cd
product: flux
tags: [sharding, sharding-key, watch-label-selector, horizontal-scaling, source-controller]
level: advanced
status: docs-checked
description: "Scale Flux horizontally by deploying extra controller instances per shard and labelling resources with sharding.fluxcd.io/key."
sources:
  - https://fluxcd.io/flux/installation/configuration/sharding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For tens of thousands of objects, run several instances of source-controller, kustomize-controller and helm-controller, each watching one shard key.

At bootstrap, create a directory per shard (for example `clusters/my-cluster/flux-system/shard1/kustomization.yaml`) that:
- takes `../gotk-components.yaml` as a resource, with `nameSuffix: "-shard1"` and `commonAnnotations: sharding.fluxcd.io/role: "shard"`;
- deletes the shared objects (Namespace, CRDs, ClusterRoles, ServiceAccounts and so on) and the notification-controller, source-watcher and image controllers, which do not support sharding;
- retargets the Service and Deployment selectors and the source-controller `--storage-adv-addr` to the `-shard1` name.

Each sharded controller runs with `--watch-label-selector=sharding.fluxcd.io/key=shard1`. Add `shard1` to the main `kustomization.yaml` resources, and patch the main controllers with `--watch-label-selector=!sharding.fluxcd.io/key` so they ignore sharded objects.

Assign work by labelling both the source and its Kustomization or HelmRelease:

```yaml
metadata:
  labels:
    sharding.fluxcd.io/key: shard1
```

Verify with `kubectl -n flux-system get deployments`; you should see `source-controller-shard1`, `kustomize-controller-shard1` and `helm-controller-shard1` beside the main ones. Upgrades via bootstrap or the Flux GitHub Action update the shards too.

Extra replicas of one controller are failover standbys only (just the leader reconciles), so they add no capacity; use sharding.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/sharding/ (raw source in the fluxcd/website repository).

Removed or corrected: the advice to try vertical scaling first, which is not on the page.

Method: documentation only; no commands were run.
