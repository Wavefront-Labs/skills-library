---
id: computing-software.devops-ci-cd.gitlab-ci.kubernetes-executor-pod-spec-overwrites-and-resources
name: kubernetes-executor-pod-spec-overwrites-and-resources
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, kubernetes-executor-overwrites, pod-resources-limits, kubernetes-pod-spec, kubernetes-executor-config]
level: advanced
status: docs-checked
description: "Configure the GitLab Runner Kubernetes executor: default requests/limits, capped per-job overwrites, namespace and service account overwrites, node selection, pod_spec."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes executor: pod spec, overwrites, resources

## 1. Runner config
```toml
[[runners]]
  executor = "kubernetes"
  [runners.kubernetes]
    namespace = "gitlab-jobs"
    cpu_request = "500m"
    memory_request = "1Gi"
    memory_limit = "2Gi"
    cpu_request_overwrite_max_allowed = "4"
    memory_limit_overwrite_max_allowed = "8Gi"
    memory_request_overwrite_max_allowed = "8Gi"
    helper_cpu_request = "100m"
    helper_memory_limit = "256Mi"
    service_memory_limit = "1Gi"
    service_account = "ci-job"
    service_account_overwrite_allowed = "^ci-.*$"
    namespace_overwrite_allowed = "^ci-.*$"
    poll_timeout = 600                       # seconds to wait when connecting to the new container (default 180)
    [runners.kubernetes.node_selector]
      "workload" = "ci"
    [runners.kubernetes.node_tolerations]
      "ci=true" = "NoSchedule"
```

## 2. Per-job overwrites (only up to the *_max_allowed caps)
```yaml
integration:
  variables:
    KUBERNETES_CPU_REQUEST: "2"
    KUBERNETES_MEMORY_REQUEST: "4Gi"
    KUBERNETES_MEMORY_LIMIT: "6Gi"
    KUBERNETES_SERVICE_MEMORY_LIMIT: "2Gi"
    KUBERNETES_SERVICE_ACCOUNT_OVERWRITE: ci-integration
```
Each overwrite is limited by its `*_overwrite_max_allowed` setting; when that setting is empty, the overwrite feature is disabled. `KUBERNETES_SERVICE_ACCOUNT_OVERWRITE` must match the `service_account_overwrite_allowed` Go regular expression (it matches any part of the value unless anchored with `^` and `$`).

## 3. pod_spec patches (anything the TOML lacks)
```toml
  [[runners.kubernetes.pod_spec]]
    name = "ephemeral-storage"
    patch_type = "strategic"
    patch = '''
      containers:
        - name: build
          resources: { limits: { ephemeral-storage: 20Gi } }
    '''
```
This feature is in beta: test on a non-production cluster first. It requires the `FF_USE_ADVANCED_POD_SPEC_CONFIGURATION` feature flag (for example `environment = ["FF_USE_ADVANCED_POD_SPEC_CONFIGURATION=true"]` on the runner). `patch_type` accepts `merge`, `json` and `strategic`.
Container names: `build`, `helper`, and for services the alias (runner 17.9+, when it is a valid DNS label) or `svc-N` counting from 0.

## 4. Gotchas
- Raise memory per job via an overwrite rather than globally.
- `poll_timeout` is for queueing more builds than the cluster can handle at a time; raise it when a cluster autoscaler delays pod start.
- Services and containers run in the same pod and share one localhost address, so two services cannot use the same port (for example two `mysql` services). Services are reachable by DNS name; older runner versions need `localhost`.
- Service container requests add to the pod and must fit a node.

## Verify
- [ ] `kubectl get pod -n gitlab-jobs -o yaml` for a running job shows the requested resources and node selector.

## Checked

2026-10-31. Confirmed against the GitLab Runner Kubernetes executor page: every `[runners.kubernetes]` key in the sample (resource requests and limits, `*_overwrite_max_allowed`, `namespace_overwrite_allowed`, `service_account_overwrite_allowed`, `node_selector`, `node_tolerations`, `poll_timeout`), the `KUBERNETES_*` job variables, pod_spec `patch_type` values, the beta status and `FF_USE_ADVANCED_POD_SPEC_CONFIGURATION` flag, container names `build`/`helper`/`svc-N`, shared localhost. Corrected: `poll_timeout` is a container connect timeout with default 180, not a scheduling wait. Removed: the exact overwrite error text and the OOMKilled/exit 137 and autoscaler timeout messages (not in the page).

Method: documentation only; no commands were run.
