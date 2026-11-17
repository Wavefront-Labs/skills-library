---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-pod-model
name: runner-kubernetes-pod-model
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [kubernetes-executor, pod, build-container, helper-container, svc]
level: practitioner
status: docs-checked
description: "The pod layout the Kubernetes executor creates for each job."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes executor pod model

Each job runs in its own pod with these containers:
- `build`: runs the job script.
- `helper`: handles git clone, artifacts and cache.
- one container per service, named after its alias, or `svc-N` (N counting from 0) when no valid alias exists.

Relevant `[runners.kubernetes]` settings:
- `namespace`: where job pods run.
- `poll_interval`: seconds between status polls; default `3`.
- `poll_timeout`: seconds before the runner times out connecting to the container it just created; default `180`.
- `cleanup_resources_timeout`: total time for Kubernetes resources to be cleaned up after the job; default `5m`.
- `pod_disruption_budget`: creates a PodDisruptionBudget per job pod to prevent voluntary eviction such as node drains; disabled by default.

The account the runner uses must have permission to create, list and attach to Pods in the namespace.

## Checked

2026-11-03. Confirmed against pod containers, poll/cleanup/PDB settings and permissions on the Kubernetes executor page. Corrected svc-X to svc-N and the poll_timeout meaning.

Method: documentation only; no commands were run.
