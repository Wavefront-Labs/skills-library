---
id: computing-software.devops-ci-cd.argo-rollouts.troubleshooting-analysis-and-experiment-not-ending
name: troubleshooting-analysis-and-experiment-not-ending
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [troubleshooting, analysisrun, experiment, terminate, failures-vs-errors, faq, argo-rollouts]
level: advanced
status: docs-checked
description: "Diagnose AnalysisRuns and Experiments that never finish and tell failures from errors."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Why does my AnalysisRun not end?** Its length is set by the metrics. Each metric can set `interval`, `count`, and limits (`consecutiveErrorLimit`, `inconclusiveLimit`, `failureLimit`). With no interval, one measurement is taken. `count` sets how many measurements are taken; omit it and the metric keeps measuring until stopped (typical for background analysis). An AnalysisRun also ends if `.spec.terminate` is true, regardless of its state.

**Why does my Experiment not end?** Duration comes from `.spec.duration` and the analyses. After the duration the experiment scales down its ReplicaSets and marks the AnalysisRuns successful unless `requiredForCompletion` is set on an analysis, in which case it waits for those runs. If `duration` is unset and there are no AnalysisRuns, the ReplicaSets run forever. AnalysisRuns without `requiredForCompletion` make the Experiment fail only if they fail or error. Setting `.spec.terminate: true` ends it regardless of the Experiment's state.

**Failure versus error.** A failure is when the failure condition evaluates true, or a run with no failure condition evaluates the success condition false. An error means the controller could not take the measurement at all, for example an invalid Prometheus URL; errors are limited by `consecutiveErrorLimit`.

Verify by reading the AnalysisRun's message and per-measurement phase in its status.

## Checked

2026-11-08. Confirmed against the Argo Rollouts FAQ (read in full): AnalysisRun and Experiment end conditions, requiredForCompletion, spec.terminate, failures versus errors.

Removed or corrected: removed the kubectl argo rollouts terminate commands and the kubectl describe verify command (not on the cited page).

Method: documentation only; no commands were run.
