---
id: computing-software.devops-ci-cd.argo-rollouts.failure-limit-and-success-conditions
name: failure-limit-and-success-conditions
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [failurelimit, consecutivesuccesslimit, failurecondition, successcondition, analysis, inconclusive, argo-rollouts]
level: advanced
status: docs-checked
description: "Combine successCondition, failureCondition, failureLimit and consecutiveSuccessLimit to control how a metric passes or fails."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each metric evaluates a measurement against `successCondition` and/or `failureCondition` (expr expressions over `result`). `failureLimit` is the number of failed measurements tolerated; the default 0 means no failures are tolerated. `consecutiveSuccessLimit` (since v1.8) is the number of consecutive successes required.

To disable them: `failureLimit: -1`, or `consecutiveSuccessLimit: 0` (its default, meaning inapplicable). Note that 0 means different things: for failureLimit it is active with zero tolerance.

Three behaviours:

1. **Only failureLimit** (default): measure on an interval; the run fails when failures exceed the limit.
2. **Only consecutiveSuccessLimit**: the analysis succeeds once N consecutive measurements succeed.
3. **Both**: wait for N consecutive successes while limited by overall failures, e.g. at most 3 failures before 4 consecutive successes.

Outcomes with both set: failureLimit violated is Failure (it takes priority, whatever the success streak); not violated and streak satisfied is Success; neither violated nor satisfied is Inconclusive.

```yaml
metrics:
  - name: total-errors
    interval: 5m
    failureCondition: result[0] >= 10
    failureLimit: 3
```

When an analysis is terminated prematurely it always ends successfully, unless failureLimit is enabled and violated (then it ends in failure). consecutiveSuccessLimit, if enabled, does not affect the termination status.

Verify in the AnalysisRun status phase and per-measurement results.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/.

Removed or corrected: the claim that count triggers the evaluation table and the "useful for waiting" gloss; premature-termination wording aligned to the page.

Method: documentation only; no commands were run.
