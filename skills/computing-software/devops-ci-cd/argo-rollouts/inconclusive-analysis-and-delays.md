---
id: computing-software.devops-ci-cd.argo-rollouts.inconclusive-analysis-and-delays
name: inconclusive-analysis-and-delays
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [inconclusive, initialdelay, startingstep, analysis, pause, manual-judgement, argo-rollouts]
level: advanced
status: docs-checked
description: "Use Inconclusive results for human judgement and delay metrics with initialDelay and startingStep."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Inconclusive runs.** A run is Inconclusive when it is neither successful nor failed. This happens when a metric defines no success or failure conditions, or defines both and the measurement meets neither. An Inconclusive run pauses the rollout at its current step and needs manual intervention: resume (promote) or abort.

The intended use is automating measurement collection while letting a human decide whether the value is acceptable, then either resume the rollout or abort it.

**Delaying analysis.** If the metrics provider needs time to collect data for the canary, delay in two ways.

Per metric, `initialDelay` on a metric (different metrics may use different delays):

```yaml
metrics:
  - name: success-rate
    initialDelay: 5m
    successCondition: result[0] >= 0.95
```

Per rollout, `startingStep` on the background analysis delays creating the AnalysisRun until a given step index is reached (for example `startingStep: 2` waits for the third step, `setWeight: 40`).

```yaml
analysis:
  templates:
    - templateName: success-rate
  startingStep: 2
```

Verify by checking that the AnalysisRun is created only once the target step is reached, and that its phase shows Inconclusive when paused for judgement.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full): Inconclusive causes, pause at current step with manual resume or abort, initialDelay per metric, startingStep for background analysis.

Removed or corrected: removed the kubectl promote and abort commands and the claim that Job metrics go Inconclusive on ErrImagePull (neither is on the cited page).

Method: documentation only; no commands were run.
