---
id: computing-software.devops-ci-cd.flagger.flagger-canary-target-and-primary
name: flagger-canary-target-and-primary
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary, primary, deployment, hpa, config-tracking]
level: practitioner
status: docs-checked
description: "Understand how Flagger derives the primary Deployment and HPA from the canary target, config tracking of ConfigMaps and Secrets, selector labels and progress deadline."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A canary targets a Deployment or DaemonSet. Flagger generates `deployment/<targetRef.name>-primary` and `hpa/<autoscalerRef.name>-primary`. The primary is the stable release and receives all traffic; the target deployment is scaled to zero. Flagger detects changes to the target, including its secrets and configmaps, and runs analysis before promoting.

```yaml
spec:
  progressDeadlineSeconds: 60
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  autoscalerRef:
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    name: podinfo
    primaryScalerReplicas:
      minReplicas: 2
      maxReplicas: 5
```

- `primaryScalerReplicas` overrides replica bounds on the generated primary HPA. Flagger requires the `autoscaling/v2` HPA API.
- With an `autoscalerRef`, Flagger pauses traffic increases while target and primary scale. Autoscaler changes only become active in the primary HPA when a rollout starts and completes successfully.
- The deployment needs a single label selector `app: <NAME>`; `name` and `app.kubernetes.io/name` also work. For another convention use the `-selector-labels=my-app-label` flag or Helm `selectorLabels`.
- Config tracking: Flagger copies each referenced ConfigMap and Secret as `<name>-primary`. Annotate one with `flagger.app/config-tracking: disabled` to share the same object, or disable globally with `-enable-config-tracking=false` (Helm `configTracking.enabled=false`).
- `progressDeadlineSeconds` is the maximum time to make progress before rollback; default ten minutes.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
