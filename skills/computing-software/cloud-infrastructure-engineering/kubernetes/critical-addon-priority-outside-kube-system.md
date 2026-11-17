---
id: computing-software.cloud-infrastructure-engineering.kubernetes.critical-addon-priority-outside-kube-system
name: critical-addon-priority-outside-kube-system
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, priorityclass, critical-addons, system-cluster-critical, system-node-critical, resourcequota]
level: practitioner
status: docs-checked
description: "Run cluster add-ons outside kube-system with system-cluster-critical or system-node-critical, and stop tenants abusing those classes with quota."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#resource-quota-per-priorityclass"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical add-ons outside kube-system

Add-ons like CNI agents, CSI node plugins, ingress controllers, DNS and log shippers often live in
their own namespaces. Give them the built-in classes: they carry the highest priorities, so the
scheduler can preempt lower-priority pods for them and the kubelet ranks priority when it evicts:
- `system-node-critical` (2000001000): must run on every node (CNI, CSI node, kube-proxy).
- `system-cluster-critical` (2000000000): cluster-wide services (CoreDNS, metrics-server,
  ingress controller).

```yaml
spec:
  priorityClassName: system-node-critical
```
Priority values above 1,000,000,000 are reserved for these built-in classes; user-defined classes
cannot exceed that.

## Keep tenants from using them
```yaml
# AdmissionConfiguration for ResourceQuota (apiserver --admission-control-config-file)
limitedResources:
- resource: pods
  matchScopes:
  - scopeName: PriorityClass
    operator: In
    values: [system-cluster-critical, system-node-critical]
```
Then create a quota in each add-on namespace that allows them:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: critical-pods, namespace: ingress-nginx}
spec:
  hard: {pods: "20"}
  scopeSelector:
    matchExpressions:
    - {scopeName: PriorityClass, operator: In, values: [system-cluster-critical]}
```
An admission policy (for example ValidatingAdmissionPolicy) can do the same check.

## Verify
```bash
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,PRIO:.spec.priority
```
Only pods in expected add-on namespaces show priority 2000000000 or 2000001000.

## Checked
2026-10-23, against the Kubernetes website pod priority and preemption page (built-in values 2000000000 / 2000001000, ResourceQuota PriorityClass scope with limitedResources admission config, quota example) and the PriorityClass validation source (user-defined maximum 1,000,000,000). The "usable outside kube-system since 1.17" claim was removed as unconfirmed.
Method: documentation only; no commands were run.
