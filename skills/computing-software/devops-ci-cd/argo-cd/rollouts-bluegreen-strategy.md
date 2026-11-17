---
id: computing-software.devops-ci-cd.argo-cd.rollouts-bluegreen-strategy
name: rollouts-bluegreen-strategy
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, bluegreen-strategy, preview-service, active-service, auto-promotion, pre-promotion-analysis]
level: advanced
status: gated
description: "Run blue-green releases with Argo Rollouts: active and preview Services, manual or timed promotion, pre/post-promotion analysis, scale-down delay, abort and rollback."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/", "https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BlueGreen strategy with preview/active Services

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: api }
spec:
  replicas: 4
  revisionHistoryLimit: 3
  selector: { matchLabels: { app: api } }
  template: { ... }                          # same pod template as a Deployment
  strategy:
    blueGreen:
      activeService: api-active              # production traffic
      previewService: api-preview            # new version for testing
      autoPromotionEnabled: false            # wait for manual promote
      # autoPromotionSeconds: 600            # or promote automatically after this many seconds (default nil)
      previewReplicaCount: 1                 # smaller preview stack, scaled up on promotion
      scaleDownDelaySeconds: 60              # keep old ReplicaSet for fast rollback / connection drain
      prePromotionAnalysis:
        templates: [{ templateName: smoke-tests }]
        args: [{ name: url, value: http://api-preview.app.svc }]
      postPromotionAnalysis:
        templates: [{ templateName: error-rate }]
```
Both Services are plain `Service` objects selecting `app: api`; the controller changes the selector of the active Service to point at the new ReplicaSet on promotion (the docs warn of a propagation delay while nodes update their rules, so keep the old ReplicaSet for `scaleDownDelaySeconds`, default 30).

## Operating
```bash
kubectl argo rollouts get rollout api --watch
kubectl argo rollouts promote api            # switch active to the new ReplicaSet
kubectl argo rollouts abort api              # (gated: unconfirmed, source is paywalled or blocked)
kubectl argo rollouts undo api               # (gated: unconfirmed, source is paywalled or blocked)
kubectl argo rollouts retry rollout api      # (gated: unconfirmed, source is paywalled or blocked)
```

## Gotchas
- A failed `postPromotionAnalysis` switches traffic back to the old ReplicaSet, only while it still exists (gated: unconfirmed, source is paywalled or blocked).
- Running two full stacks doubles capacity during rollout — plan quotas or use `previewReplicaCount`.
- Argo CD shows the app Suspended while waiting for promotion (gated: unconfirmed, source is paywalled or blocked).
- Migration from a Deployment via `workloadRef`: see the Argo Rollouts migration docs (not checked here).

## Verify
- [ ] Preview Service serves the new version while active still serves the old; after promote, active switches and old pods scale down after the delay.

## Checked

2026-11-02. Confirmed from the Argo Rollouts BlueGreen page: activeService, previewService, autoPromotionEnabled (defaults to true), autoPromotionSeconds (default nil), previewReplicaCount, scaleDownDelaySeconds (default 30 seconds), pre/postPromotionAnalysis, the promotion sequence and the selector propagation delay; from the kubectl plugin page: kubectl argo rollouts get rollout NAME -w. Removed the rollouts-pod-template-hash label name and the 10 min figure. Gated: abort/undo/retry semantics, rollback after failed post-promotion analysis, Suspended status.

Method: documentation only; no commands were run.
