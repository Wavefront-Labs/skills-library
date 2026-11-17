---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-pause-pods
name: runner-kubernetes-pause-pods
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [pause-pods, kubernetes-autoscaler, idle-capacity, priority-class]
level: sme
status: docs-checked
description: "Reserve warm cluster capacity with pause pods (runner 18.10)."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pause pods for idle capacity

Introduced in 18.10, `[runners.kubernetes.autoscaler]` keeps spare capacity by running low-priority placeholder pods.

- `max_pause_pods`: maximum number of pause pods; `0` means unlimited.
- The pause image defaults to `registry.k8s.io/pause:3.10`.
- Pause pods use the priority class `gitlab-runner-idle-capacity` by default, which the runner creates automatically with priority `-1`; if you set `pause_pod_priority_class_name`, auto-creation is skipped and your class must have lower priority than job pods.

When a job pod needs resources, the scheduler can evict a pause pod, and the cluster autoscaler then adds a node to reschedule it, so the next job finds capacity already provisioned.

## Checked

2026-11-03. Confirmed against pause pod behaviour, defaults and priority class on the Kubernetes executor page (introduced 18.10). Corrected: the priority class is auto-created by default.

Method: documentation only; no commands were run.
