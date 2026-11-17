---
id: computing-software.cybersecurity-defensive.cloud-security.kubernetes-audit-logs
name: kubernetes-audit-logs
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-detection, kubernetes-audit-logs, audit-policy, eks-control-plane-logging, aks-diagnostic-settings, gke-audit-logs, kubernetes-detection]
level: advanced
status: docs-checked
description: "Collect and use Kubernetes API audit logs: audit policy levels, enabling on self-managed, EKS, AKS and GKE, and which events to alert on."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/", "https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html", "https://cloud.google.com/kubernetes-engine/docs/how-to/audit-logging", "https://learn.microsoft.com/en-us/azure/aks/monitor-aks-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes audit logs

The API server audit log records requests to the Kubernetes API. It is a primary detection and
forensic source for cluster-level attacks.

## Enable
- **Self-managed**: pass `--audit-policy-file` to kube-apiserver (if omitted, no events are logged;
  the policy must contain `rules`) and `--audit-log-path` for the log backend (`-` means standard out;
  without it the log backend is disabled).
- **EKS**: enable control plane log types per cluster (console, AWS CLI or EKS API). Logs go to
  CloudWatch Logs in the same account; delivery is best effort.
- **AKS**: diagnostic settings categories `kube-audit` (all events including get and list) or
  `kube-audit-admin` (excludes get and list, so less noise).
- **GKE**: Admin Activity audit logs cannot be disabled; Data Access audit logs must be explicitly enabled.

## Audit policy
Levels: `None`, `Metadata`, `Request`, `RequestResponse` (the last logs request and response bodies).
Rules are evaluated from a policy file; `omitStages` skips stages such as `RequestReceived`.
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages: ["RequestReceived"]
rules:
  - level: RequestResponse
    resources: [{group: "rbac.authorization.k8s.io"}]
  - level: Metadata
```

## Events worth alerting on (detection ideas, not from the docs)
- `pods/exec`, `pods/attach`, `pods/portforward` in production namespaces.
- Secrets get/list by unusual identities; new `clusterrolebindings` to `cluster-admin`.
- Privileged pod creation; requests from `system:anonymous`; many 403s from one identity.

## Gotchas
- Volume and cost: get/list/watch traffic dominates; filter in the policy or use `kube-audit-admin` on AKS.
- Avoid `RequestResponse` on Secrets, since it records bodies.

## Verify
Run `kubectl exec` into a test pod and create a test ClusterRoleBinding; both appear in the audit
destination.

## Checked
2026-11-01. Confirmed on the Kubernetes auditing page, EKS control plane logs page, AKS monitoring reference
and GKE audit logging page: the policy flags and behaviour, audit levels, `omitStages`, EKS destination and
best-effort delivery, kube-audit vs kube-audit-admin, GKE Admin Activity/Data Access behaviour. The
high-signal event list is detection guidance, labelled as not from the docs. Removed: EKS log type names and
CLI command, GuardDuty, the CloudWatch Logs Insights query, the EKS username-mapping note, and the policy rules
for kube-proxy and mutating verbs.
Method: documentation only; no commands were run.
