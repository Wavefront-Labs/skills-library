---
id: computing-software.devops-ci-cd.argo-rollouts.bluegreen-strategy-basics
name: bluegreen-strategy-basics
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [blue-green, activeservice, previewservice, autopromotionenabled, rollout, argo-rollouts]
level: practitioner
status: docs-checked
description: "Configure a blue-green Rollout with active and preview Services and manual or automatic promotion."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `spec.strategy.blueGreen` the controller edits Services rather than relying on rolling logic. `activeService` is mandatory and carries production traffic. `previewService` is optional and points at the new ReplicaSet so you can test it without serving users.

```yaml
spec:
  replicas: 2
  revisionHistoryLimit: 2
  strategy:
    blueGreen:
      activeService: rollout-bluegreen-active
      previewService: rollout-bluegreen-preview
      autoPromotionEnabled: false
```

When `.spec.template` changes, a new ReplicaSet is created. If the active Service is not sending traffic to any ReplicaSet, the controller immediately starts sending traffic to the new one; otherwise it keeps pointing at the old ReplicaSet while the new one becomes available.

`autoPromotionEnabled` defaults to true: promote as soon as the new ReplicaSet is fully available. Set false to pause just before promotion; resume with:

```bash
kubectl argo rollouts promote ROLLOUT
```

`autoPromotionSeconds` (default nil) auto-promotes after that many seconds in the paused state; it is ignored if `autoPromotionEnabled` is false.

Caveat from the docs: when the selector on a Service changes there is a propagation delay while nodes update iptables, so old pods must stay alive briefly (see bluegreen-scale-down-and-preview-replicas). Also, ALB Ingress with blue-green is not supported without a chance of downtime.

Verify: `kubectl argo rollouts get rollout NAME --watch`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/.

Removed or corrected: the "first deploy" gloss.

Method: documentation only; no commands were run.
