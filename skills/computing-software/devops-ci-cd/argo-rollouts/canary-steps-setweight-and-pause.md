---
id: computing-software.devops-ci-cd.argo-rollouts.canary-steps-setweight-and-pause
name: canary-steps-setweight-and-pause
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [canary, steps, setweight, pause, promote, argo-rollouts]
level: practitioner
status: docs-checked
description: "Define canary steps with setWeight and pause, including timed and indefinite pauses and manual promotion."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/canary/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A canary Rollout lists `steps` the controller evaluates in order each time `.spec.template` changes. `setWeight` is the percentage of traffic (or, without a router, approximate pod ratio) for the canary; `pause` stops the rollout.

```yaml
spec:
  replicas: 10
  minReadySeconds: 30
  revisionHistoryLimit: 3
  strategy:
    canary:
      maxSurge: '25%'
      maxUnavailable: 0
      steps:
        - setWeight: 10
        - pause:
            duration: 1h
        - setWeight: 20
        - pause: {}
```

Pause units are `s`, `m` and `h`; no suffix means seconds. `pause: {}` has no duration, so the rollout pauses indefinitely by adding a `PauseCondition` to `.status.pauseConditions` until promoted:

```bash
kubectl argo rollouts promote ROLLOUT
```

Without traffic management the controller makes a best effort to hit the last `setWeight` by scaling replica counts; with 10 replicas and 10% it scales the canary to one pod. Steps are skipped on the initial deploy of a Rollout.

If `steps` is omitted entirely the canary behaves like a rolling update governed by `maxSurge` and `maxUnavailable` (both default 25%, and not both 0).

Other canary fields: `analysis`, `antiAffinity`, `canaryService`, `stableService`, `trafficRouting`.

Verify with `kubectl argo rollouts get rollout NAME -w`, which shows the current step.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Canary page and Rollout Specification page: `setWeight` and `pause` semantics, `PauseCondition` in `.status.pauseConditions`, pause duration units and the seconds default, `kubectl argo rollouts promote`, best-effort pod ratio without traffic management, steps skipped on initial deploy, `maxSurge` and `maxUnavailable` defaults and the not-both-zero rule, and the other canary fields. Nothing removed.
Method: documentation only; no commands were run.
