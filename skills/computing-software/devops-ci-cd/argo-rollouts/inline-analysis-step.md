---
id: computing-software.devops-ci-cd.argo-rollouts.inline-analysis-step
name: inline-analysis-step
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [analysis, inline-analysis, steps, count, interval, canary, argo-rollouts]
level: practitioner
status: docs-checked
description: "Add an analysis step to canary steps so the rollout blocks until the AnalysisRun finishes, with count and interval."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `analysis` step starts an AnalysisRun when the step is reached and blocks the rollout until it completes. Success proceeds to the next step; failure aborts the rollout.

```yaml
steps:
  - setWeight: 20
  - pause: {duration: 5m}
  - analysis:
      templates:
        - templateName: success-rate
      args:
        - name: service-name
          value: guestbook-svc.default.svc.cluster.local
```

If the template metric specifies no `interval`, the analysis performs a single measurement and completes. For several measurements, set `count` and `interval`:

```yaml
metrics:
  - name: success-rate
    successCondition: result[0] >= 0.95
    interval: 60s
    count: 5
    provider:
      prometheus:
        address: http://prometheus.example.com:9090
        query: ...
```

The same template can be reused for background analysis (with an interval and no count) and inline analysis (with count). Remember the gotcha: a `count` of 0 for an analysis defined in steps means it will not execute.

Use inline analysis for gates ("after 20% for 5 minutes, check error rate"), and background analysis for continuous guard rails.

Verify with `kubectl argo rollouts get rollout NAME -w`: the tree view shows the AnalysisRun created by the analysis step.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full): inline analysis step blocks the rollout, no interval means a single measurement, count and interval, count 0 inside steps. The tree view is from the kubectl plugin page (read in full).

Removed or corrected: dropped the unsourced claim that both styles can be combined in one Rollout and the kubectl describe analysisrun command.

Method: documentation only; no commands were run.
