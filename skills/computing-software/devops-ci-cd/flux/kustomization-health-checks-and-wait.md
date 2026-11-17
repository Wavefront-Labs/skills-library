---
id: computing-software.devops-ci-cd.flux.kustomization-health-checks-and-wait
name: kustomization-health-checks-and-wait
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, healthchecks, wait, kstatus, timeout]
level: sme
status: docs-checked
description: "Make a Flux Kustomization verify rollouts with spec.healthChecks or spec.wait, and what Ready means afterward."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After applying, a Kustomization can verify that workloads actually rolled out. Two options:

`.spec.healthChecks` lists specific objects. Entries can be built-in kinds (Deployment, DaemonSet, StatefulSet, PersistentVolumeClaim, Pod, PodDisruptionBudget, Job, CronJob, Service, Secret, ConfigMap, CustomResourceDefinition), Flux kinds such as HelmRelease and GitRepository, or any custom resource compatible with kstatus.

```yaml
spec:
  interval: 5m
  prune: true
  sourceRef:
    kind: GitRepository
    name: webapp
  timeout: 3m
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: backend
      namespace: dev
```

`.spec.wait: true` checks all reconciled resources and causes `.spec.healthChecks` to be ignored. Use it when you want every applied object healthy, not a hand-picked list.

`.spec.timeout` sets a timeout for any operation during reconciliation, such as building, applying and health checking. Kustomizations listed in another's `dependsOn` are only applied once this one is Ready.

`.spec.retryInterval` sets a separate retry cadence for failed reconciliations and defaults to `.spec.interval`.

Inspect status with `flux get kustomizations` and `kubectl describe kustomization NAME` (Status and Events).

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `healthChecks` supported kinds, `wait` ignoring `healthChecks`, `timeout`, `retryInterval` default; `flux get kustomizations` checked on its CLI page. Removed advice on sizing the timeout.

Method: documentation only; no commands were run.
