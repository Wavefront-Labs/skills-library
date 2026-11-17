---
id: computing-software.devops-ci-cd.argo-cd.rollouts-experiments
name: rollouts-experiments
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, experiment-crd, baseline-vs-canary, experiment-step, rollout-experiments]
level: advanced
status: docs-checked
description: "Use Argo Rollouts Experiments to run baseline and canary ReplicaSets side by side for a fixed time with analyses, inline as a canary step or as a standalone Experiment."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/experiment/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Experiments

An Experiment runs one or more ReplicaSets (from templates) for a **duration**, optionally with
AnalysisRuns comparing them, then scales them away. Use it for apples-to-apples comparison:
a fresh baseline pod vs a fresh canary pod, both receiving similar traffic, so warm-up effects and old-pod bias do not skew metrics.

## 1. Inline in a canary
```yaml
strategy:
  canary:
    steps:
      - experiment:
          duration: 30m
          templates:
            - { name: baseline, specRef: stable, replicas: 1 }
            - { name: canary,   specRef: canary, replicas: 1 }
          analyses:
            - name: compare-latency
              templateName: latency-compare
      - setWeight: 25
      - pause: { duration: 10m }
```
A template can receive an explicit traffic `weight` only with traffic routing. A Service routing to an Experiment ReplicaSet is generated when a `weight` is set or the template's `service` attribute is set.

## 2. Standalone
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Experiment
metadata: { name: jvm-flags-test }
spec:
  duration: 1h
  templates:
    - name: g1
      replicas: 2
      selector: { matchLabels: { app: api, variant: g1 } }
      template: { metadata: { labels: { app: api, variant: g1 } }, spec: { ... } }
    - name: zgc
      replicas: 2
      selector: { matchLabels: { app: api, variant: zgc } }
      template: { ... }
  analyses:
    - { name: compare, templateName: p99-compare }
```
If an analysis template is marked `requiredForCompletion: true`, the Experiment does not complete until those AnalysisRuns finish, even past `duration`. With neither `duration` nor `requiredForCompletion`, the Experiment runs indefinitely until terminated (`spec.terminate: true`).

## Gotchas
- Analysis queries must filter by pod template hash/labels, or both variants read the same metrics.
- Short experiments with little traffic produce statistically meaningless comparisons — size duration to request volume.

## Verify
- [ ] During the experiment, baseline and canary ReplicaSets exist (`kubectl get rs`); after the duration they are scaled down.

## Checked

2026-10-28. Confirmed against the Argo Rollouts Experiment page: specRef stable/canary, duration, weight requires traffic routing, generated Service rules, requiredForCompletion, runs indefinitely until spec.terminate, ReplicaSets scaled down after the duration. Removed: podTemplateHashValue analysis args and the kubectl argo rollouts get experiment command (not on this page), and the rollout-aborts-on-failed-analysis sentence.

Method: documentation only; no commands were run.
