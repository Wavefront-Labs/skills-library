---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-k8s-filtering
name: tetragon-policy-k8s-filtering
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [k8s-filtering, tetragon, kubernetes, podselector, nodeselector]
level: practitioner
status: docs-checked
description: "Scope a Tetragon TracingPolicy to namespaces, pods, containers, host workloads or nodes using in-kernel Kubernetes identity filters."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/k8s-filtering/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Kubernetes identity aware policies

Goal: apply a TracingPolicy only to chosen workloads. Filtering happens in-kernel via eBPF, which cuts event copying for observability and lets enforcement happen before a syscall finishes. To apply policies correctly before containers start, Tetragon uses OCI runtime hooks; without them it applies policies best-effort using the k8s API server.

## Mechanisms

- Namespace: use kind `TracingPolicyNamespaced`; same contents as `TracingPolicy` but only applies to pods of its namespace.
- Pod labels: `podSelector` field.
- Container fields: `containerSelector`; only `name` and `repo` are supported.
- Host workloads: `hostSelector`; only `{}` (match all host workloads) or `null` (match none). Any non-null `hostSelector` on a `TracingPolicyNamespaced` is an error.
- Nodes: `nodeSelector`, a standard Kubernetes label selector (`matchLabels`, `matchExpressions`) evaluated by each agent against its own node's labels. Empty or omitted means all nodes. Only applies to policies managed via the Kubernetes API (not file or gRPC loaded). Relabeling a node re-evaluates policies. Gated-out policies show as `skipped` in `tetra tracingpolicy list`. If the selector cannot be evaluated, the policy loads (fails open). Warning: anyone who can edit node labels can unload an enforcement policy, so restrict label edits.

```yaml
spec:
  nodeSelector:
    matchLabels:
      nodepool: gpu
    matchExpressions:
    - key: kubernetes.io/arch
      operator: In
      values:
      - amd64
```

## Semantics

`containerSelector` is a second-level filter on `podSelector`. If `hostSelector`, `podSelector` and `containerSelector` are all null (omitted), filtering is disabled and everything is selected.

| host | pod | container | Result |
|---|---|---|---|
| null | null | {...} | matching containers in all pods, no host |
| null | {...} | null | all containers in matching pods, no host |
| null | {...} | {...} | matching containers in matching pods, no host |
| {} | null | null | all host workloads |
| {} | {...} | {...} | host plus matching containers in matching pods |

Namespace example: a `podSelector` `matchExpressions` on key `k8s:io.kubernetes.pod.namespace` with operator `In` and values `kube-system`, combined with `hostSelector: {}`, matches that namespace plus host workloads.

## Checked

2026-11-08. Read the Kubernetes identity aware policies page in full (raw docs markdown from cilium/tetragon). Checked the mechanisms, nodeSelector behaviour and semantics table against it; no claims removed.

Method: documentation only; no commands were run.
