---
id: computing-software.devops-ci-cd.argo-rollouts.experiment-crd-lifecycle
name: experiment-crd-lifecycle
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [experiment, templates, duration, requiredforcompletion, terminate, ab-testing, argo-rollouts]
level: advanced
status: docs-checked
description: "Define an Experiment with templates, analyses and duration, and understand its lifecycle and use cases."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/experiment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Experiment runs one or more ephemeral ReplicaSets and can launch AnalysisRuns against them. Use cases: Kayenta-style baseline versus canary comparison for a fixed duration, A/B/C tests with several versions, or running a new version with different labels so a Service does not send it traffic.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Experiment
spec:
  duration: 20m
  progressDeadlineSeconds: 30
  templates:
    - name: purple
      replicas: 1
      service:
        name: service-name
      selector: {matchLabels: {app: canary-demo, color: purple}}
      template: {...}
  analyses:
    - name: compare-results
      templateName: compare
      requiredForCompletion: true
```

Lifecycle:

1. A ReplicaSet is created per template (plus a Service if `service` is set).
2. All must become available within `progressDeadlineSeconds` or the Experiment fails; then it moves from Pending to Running.
3. An AnalysisRun starts for each entry in `analyses`.
4. If `duration` is set, it waits that long (counted from all ReplicaSets healthy).
5. A failed or errored AnalysisRun ends the Experiment with that status.
6. Analyses marked `requiredForCompletion: true` extend it past the duration.
7. With neither duration nor required analyses, it runs until `spec.terminate: true`.
8. On completion, ReplicaSets scale to zero and unfinished AnalysisRuns end.

ReplicaSet names combine the Experiment and template names. `replicas` defaults to 1.

Verify with `kubectl get experiment` and `kubectl argo rollouts get experiment NAME`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/experiment/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
