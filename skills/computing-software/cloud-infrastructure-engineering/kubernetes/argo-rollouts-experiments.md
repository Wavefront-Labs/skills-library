---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argo-rollouts-experiments
name: argo-rollouts-experiments
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment-strategies, rollout-experiment, argo-rollouts, analysis, a-b-testing]
level: practitioner
status: docs-checked
description: "Run Argo Rollouts Experiments that start baseline and canary ReplicaSets side by side for a fixed time with analysis, standalone or as a step inside a canary Rollout."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/experiment/", "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/", "https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_get_experiment/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Rollouts Experiments

An Experiment runs one or more short-lived ReplicaSets (for example baseline and canary built from
the same template) for a duration, runs AnalysisTemplates against them, then scales them down.
Comparing a fresh baseline with the canary avoids bias from long-running stable pods.

## As a canary step
```yaml
strategy:
  canary:
    steps:
    - experiment:
        duration: 30m
        templates:
        - {name: baseline, specRef: stable, replicas: 1}
        - {name: canary, specRef: canary, replicas: 1}
        analyses:
        - name: compare-latency
          templateName: latency-comparison
          args:
          - {name: baseline-hash, value: "{{templates.baseline.podTemplateHash}}"}
          - {name: canary-hash, value: "{{templates.canary.podTemplateHash}}"}
    - setWeight: 20
    - pause: {duration: 10m}
```
If an AnalysisRun fails or errors, the Experiment ends early with that status. The
Experiment's pod hashes differ from the Rollout's stable/canary hashes on purpose,
so use the `templates.<name>.podTemplateHash` variables in metric queries. A Service for an Experiment
ReplicaSet is generated only if a `weight` (which requires traffic routing) or `service` is set on the
template, so otherwise no production traffic reaches it.

## Standalone
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Experiment
metadata: {name: jvm-flags-test}
spec:
  duration: 1h
  templates:
  - name: g1
    replicas: 2
    selector: {matchLabels: {app: api, variant: g1}}
    template: {metadata: {labels: {app: api, variant: g1}}, spec: {containers: [{name: api, image: acme/api:5, env: [{name: JAVA_OPTS, value: "-XX:+UseG1GC"}]}]}}
  - name: zgc
    replicas: 2
    selector: {matchLabels: {app: api, variant: zgc}}
    template: {metadata: {labels: {app: api, variant: zgc}}, spec: {containers: [{name: api, image: acme/api:5, env: [{name: JAVA_OPTS, value: "-XX:+UseZGC"}]}]}}
  analyses:
  - {name: compare, templateName: gc-pause-comparison}
```

## Inspect
```bash
kubectl argo rollouts get experiment jvm-flags-test --watch
```

## Verify
The Experiment completes (or ends `Failed`/`Error` on a failed AnalysisRun), and its ReplicaSets scale to zero afterwards.
Without `spec.duration` or an analysis with `requiredForCompletion: true`, an Experiment runs
until terminated (`spec.terminate: true`).

## Checked

Documentation release: Argo Rollouts docs (argo-rollouts repo docs/, latest release v1.10.1, repo commit 2026-10-20).
Confirmed against features/experiment.md: `specRef: stable|canary`, `duration` counted from when all ReplicaSets are healthy, `analyses`, `progressDeadlineSeconds`, the lifecycle (failed analysis ends the Experiment, `requiredForCompletion`, run indefinitely without duration, ReplicaSets scaled to zero), weight/service Service generation, and the pod-hash variables; `kubectl argo rollouts get experiment NAME -w` from the generated CLI reference.
Corrected: the `podTemplateHashValue` args (documented for AnalysisRun args, not Experiment step analyses); removed the unsourced `experiment` label query and the claim that the Rollout "aborts before any weight is set".

Method: documentation only; no commands were run.
