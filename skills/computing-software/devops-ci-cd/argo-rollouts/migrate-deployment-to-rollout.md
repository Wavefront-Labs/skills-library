---
id: computing-software.devops-ci-cd.argo-rollouts.migrate-deployment-to-rollout
name: migrate-deployment-to-rollout
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [migration, workloadref, scaledown, deployment, rollout, convert, argo-rollouts]
level: practitioner
status: docs-checked
description: "Convert a Deployment into a Rollout or reference it through workloadRef without causing downtime."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/migrating/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two approaches.

**Convert.** Change three things: `apiVersion` from `apps/v1` to `argoproj.io/v1alpha1`, `kind` from `Deployment` to `Rollout`, and replace the Deployment strategy (`rollingUpdate` or `recreate`) with `blueGreen` or `canary`.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {}
```

Warning: if the Deployment already serves live production traffic, run the Rollout next to it before deleting or scaling down the Deployment, otherwise you may see downtime. It also lets you test the Rollout first.

**Reference with workloadRef.** Keep the Deployment as the source of the pod template, scale it to zero, and let a Rollout manage the pods:

```yaml
spec:
  replicas: 5
  selector:
    matchLabels: {app: rollout-ref-deployment}
  workloadRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rollout-ref-deployment
    scaleDown: onsuccess
```

`scaleDown` options: `never` (Deployment untouched), `onsuccess` (scaled down after the Rollout is healthy), `progressively` (scaled down as the Rollout scales up; scaled back up on failure). Updates are made by changing the Deployment's pod template. Do not use both `template` and `workloadRef`.

Verify: `kubectl get deploy,rollout` shows the Deployment at 0 replicas and the Rollout healthy.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/migrating/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
