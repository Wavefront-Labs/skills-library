---
id: computing-software.devops-ci-cd.tekton.tekton-controller-high-availability
name: tekton-controller-high-availability
category: computing-software
field: devops-ci-cd
product: tekton
tags: [high-availability, controller, webhook, leader-election]
level: advanced
status: docs-checked
description: "Run the Tekton Pipelines controller and webhook with multiple replicas, tune leader election buckets, and protect the webhook from disruption."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/enabling-ha.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controller: active/active, with the workqueue distributed across buckets so each replica owns some. Default is one replica, which disables HA in practice.

```sh
kubectl -n tekton-pipelines scale deployment tekton-pipelines-controller --replicas=3
```

Leader election ConfigMap defaults: `data.buckets` 1 (maximum 10), `data.leaseDuration` 15s, `data.renewDeadline` 10s, `data.retryPeriod` 2s. When installed by the Tekton Operator, configure these via `TektonConfig` `spec.pipeline.performance` rather than the ConfigMap.

To turn HA off, scale back to one replica (the recommended way); the controller flag `-disable-ha=true` also exists. Setting `-disable-ha=false` while running several replicas makes each replica process work items separately, which leads to unwanted behaviour when creating resources such as TaskRuns, so it is not recommended.

Webhook: stateless, so scale it with `kubectl -n tekton-pipelines scale deployment tekton-pipelines-webhook --replicas=3` or raise `minReplicas` of its HorizontalPodAutoscaler. A single replica can disappear during node drains or cluster-autoscaler scale-down, and Tekton resources cannot be created, updated or deleted meanwhile. Use multiple replicas, the `safe-to-evict: false` annotation, and a PodDisruptionBudget.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): enabling-ha.md. Removed: the claim that -disable-ha=true is the supported way to disable HA (the page recommends running one replica).

Method: documentation only; no commands were run.
