---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-level-resources
name: pod-level-resources
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resources, pod-level-resources, requests-limits, podlevelresources, qos]
level: practitioner
status: docs-checked
description: "Set CPU and memory requests and limits for the whole pod with spec.resources, let containers share the budget, and know the feature-gate and scheduling rules."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/assign-pod-level-resources/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://kubernetes.io/docs/concepts/resource-management/resource-managers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod-level resources

Since 1.32 (alpha, `PodLevelResources` gate; beta and on by default from 1.34) a pod can declare one CPU and
memory budget shared by its containers.

```yaml
apiVersion: v1
kind: Pod
metadata: {name: shared-budget}
spec:
  resources:
    requests: {cpu: "1", memory: 1Gi}
    limits:   {cpu: "2", memory: 2Gi}
  containers:
  - name: app
    image: acme/app:3
  - name: helper
    image: acme/helper:1
    resources:
      limits: {memory: 256Mi}       # optional cap inside the pod budget
```

## Rules
- Supported resources at pod level: `cpu`, `memory` and `hugepages`. Not supported for Windows pods.
- When both levels are set, pod-level requests and limits take precedence; containers together cannot use more than the
  pod-level limits, and containers without their own requests or limits work within the pod's boundaries.
- Pod-level resources take precedence in determining the QoS class, and the OOM score adjustment considers both levels.
- The gate must be enabled for the control plane and all nodes.
- The CPU, Memory and Topology managers only align pods by pod-level resources when `PodLevelResourceManagers`
  is on (alpha in 1.36, beta in 1.37, off by default). In-place resize of pod-level resources needs
  `InPlacePodLevelResourcesVerticalScaling` (check its current stage in the feature-gate reference).

## When it helps
Sidecar-heavy pods where per-container sizing is guesswork, and bursty helpers that idle most of
the time. Keep per-container limits for a helper that must never starve the main app.

## Verify
```bash
kubectl get pod shared-budget -o jsonpath='{.spec.resources}{"\n"}{.status.qosClass}'
```

## Checked

2026-10-26: kubernetes.io assign-pod-level-resources and manage-resources-containers pages (v1.37 docs, kubernetes/website main 2026-10-25), the PodLevelResources feature-gate page and the kubelet feature-gate listing. Confirmed: stage history (alpha 1.32, beta default-on 1.34), supported resource types, precedence, QoS and OOM score statements, Windows exclusion, control-plane-and-nodes requirement, PodLevelResourceManagers and in-place resize gates. Removed the unconfirmed sum-validation rule, older-kubelet remark and the node describe check.

Method: documentation only; no commands were run.
