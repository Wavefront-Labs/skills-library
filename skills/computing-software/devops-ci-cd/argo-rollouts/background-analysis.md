---
id: computing-software.devops-ci-cd.argo-rollouts.background-analysis
name: background-analysis
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [analysis, background-analysis, startingstep, canary, prometheus, analysisrun, argo-rollouts]
level: practitioner
status: docs-checked
description: "Run an AnalysisRun in the background across canary steps with startingStep and abort the rollout on failure."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Background analysis starts an AnalysisRun when the canary begins and keeps measuring while steps progress. If a metric fails, the Rollout aborts, the canary weight returns to zero and the Rollout is Degraded. If all steps finish, the controller stops the run and the rollout succeeds.

```yaml
strategy:
  canary:
    analysis:
      templates:
        - templateName: success-rate
      startingStep: 2   # delay the run until setWeight: 40
      args:
        - name: service-name
          value: guestbook-svc.default.svc.cluster.local
    steps:
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 40
      - pause: {duration: 10m}
```

The referenced template has an `interval` so it keeps measuring:

```yaml
metrics:
  - name: success-rate
    interval: 5m
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.example.com:9090
        query: ...
```

With no end time it continues until stopped or failed. Here three failed measurements (below 95%) fail the analysis. The `startingStep` index counts from 0, so 2 is the third step. If `count` is 0 in a background analysis it runs until the rollout ends; defined inside steps, count 0 means the analysis will not run.

Verify with `kubectl argo rollouts get rollout NAME -w`, which shows the AnalysisRun in the rollout's tree view.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full): startingStep, interval, failureLimit, abort and Degraded behaviour, count 0 behaviour. The kubectl plugin get rollout watch is from the kubectl plugin page (read in full).

Removed or corrected: replaced the unsourced kubectl get analysisrun verify command.

Method: documentation only; no commands were run.
