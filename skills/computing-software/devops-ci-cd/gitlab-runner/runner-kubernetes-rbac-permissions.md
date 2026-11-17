---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-rbac-permissions
name: runner-kubernetes-rbac-permissions
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [kubernetes, rbac, permissions, pods-log, events]
level: advanced
status: docs-checked
description: "Which Kubernetes permissions the runner service account needs and when."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes runner permissions

The service account needs rights to create and manage job pods and related resources in the job namespace.

Conditional permissions listed in the docs:
- `events`: needed only for GitLab 16.2.1 and later; the permissions table ties `list` to `print_pod_warning_events` and `watch` to `FF_PRINT_POD_EVENTS`.
- `namespace`: needed only when enabling `namespace_per_job`, and then through a ClusterRole and ClusterRoleBinding.
- `pods/log`: needed only when `FF_KUBERNETES_HONOR_ENTRYPOINT` or `FF_WAIT_FOR_POD_TO_BE_REACHABLE` is enabled, or when `FF_USE_LEGACY_KUBERNETES_EXECUTION_STRATEGY` is disabled and `CI_DEBUG_SERVICES` is `true`.

The Helm chart by default grants all verbs on all resources in the core API group; see its page for limiting `rbac.rules`.

## Checked

2026-11-03. Confirmed against permission notes on the Kubernetes executor page and the chart default on Install on Kubernetes. Fixed the pods/log conditions.

Method: documentation only; no commands were run.
