---
id: computing-software.cloud-infrastructure-engineering.kubernetes.daemonset-priority-and-node-critical-agents
name: daemonset-priority-and-node-critical-agents
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, daemonset-priority, system-node-critical, priorityclass, node-agents, cni, csi-node]
level: practitioner
status: docs-checked
description: "Give node agents (CNI, CSI node, log/metrics shippers) the right PriorityClass so they always fit on and are never evicted from nodes, without abusing system-node-critical."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#how-daemon-pods-are-scheduled"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet priority for node-critical agents

## Why it matters
DaemonSet pods are scheduled by the default scheduler. If a node is already full of app pods,
a newly added DaemonSet (or an updated one with bigger requests) is `Pending` on that node
unless it can **preempt**. During node-pressure eviction, low-priority agents may be evicted
— losing the CNI or CSI node plugin breaks every pod on the node.

## Built-in classes
| Class | Value | Use |
|---|---|---|
| `system-node-critical` | 2000001000 | must run on **every** node for the node to work: CNI agent, kube-proxy, CSI node plugin |
| `system-cluster-critical` | 2000000000 | cluster add-ons that may move: CoreDNS, metrics-server, cluster-autoscaler |
A ResourceQuota `scopeSelector` on PriorityClass with `limitedResources` admission config can restrict
which namespaces may use these classes.

For observability/security agents (Fluent Bit, node-exporter, Falco) create your own tier:
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: {name: node-agent}
value: 1000000000
preemptionPolicy: PreemptLowerPriority
description: "Per-node agents: above all apps, below system-*"
```
```yaml
# DaemonSet pod template
spec:
  priorityClassName: node-agent
  tolerations:
  - operator: Exists          # run on tainted nodes too (control plane, GPU, spot) — be deliberate
```

## Also needed
- **Requests set and small**: preemption and scheduling work from requests. The kubelet ranks
  eviction by whether usage exceeds requests, then priority, then usage relative to requests.
- Tolerations: DaemonSet pods automatically get tolerations for `node.kubernetes.io/not-ready` and
  `unreachable` (NoExecute), `disk-pressure`, `memory-pressure`, `pid-pressure` and `unschedulable`
  (NoSchedule) and, for `hostNetwork: true` pods only, `network-unavailable`. Custom taints need
  explicit tolerations.

## Gotchas
- Every vendor DaemonSet claiming `system-node-critical` dilutes it — reserve it for things
  without which pods cannot start or reach storage.
- Higher priority than app pods means a node-agent update can **preempt app pods** on full
  nodes. Keep agent requests stable.
- Placeholder pods with negative priority are the first preemption victims — good.

## Verify
- [ ] `kubectl get ds -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,PRIO:.spec.template.spec.priorityClassName,DESIRED:.status.desiredNumberScheduled,READY:.status.numberReady` shows a class on every agent and DESIRED=READY.

## Checked
2026-10-23, against the Kubernetes website DaemonSet page (default scheduler binds DaemonSet pods, automatic tolerations table, preemption), the pod priority page (built-in values, user-defined maximum 1,000,000,000 which the custom class respects, ResourceQuota PriorityClass scope), and the node-pressure eviction page (eviction ranking). The "since 1.17" note and the Guaranteed-QoS claim were removed as unconfirmed.
Method: documentation only; no commands were run.
