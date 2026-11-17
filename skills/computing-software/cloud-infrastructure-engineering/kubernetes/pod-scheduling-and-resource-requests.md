---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-scheduling-and-resource-requests
name: pod-scheduling-and-resource-requests
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-scheduler, scheduling, resource-requests, allocatable, node-affinity, pod-affinity, pod-anti-affinity, nodeselector, taints, tolerations, topology-spread-constraints, priorityclass, preemption, pending-pods, failedscheduling, limitrange, resourcequota, ephemeral-storage, gpu, extended-resources, bin-packing, cluster-autoscaler, karpenter, descheduler, qos-class, eviction]
level: practitioner
status: docs-checked
description: "Place pods on purpose: requests vs allocatable, affinity, taints, topology spread, PriorityClass preemption, quotas, and diagnosing Pending/FailedScheduling."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/", "https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/init-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod scheduling and resource requests — placing pods on purpose

**Goal:** every pod lands on a node that can actually run it, critical pods win contention,
replicas spread across failure domains, and a `Pending` pod can be explained in one command.
Container sizing basics (limits, probes, QoS) live in
`computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes`;
this skill is about the scheduler.

## 1. How the scheduler decides
1. **Filter**: drop nodes that fail any hard rule — free *requests* capacity, `nodeSelector`/
   required affinity, untolerated `NoSchedule` taints, volume zone, host ports.
2. **Score**: rank survivors on soft rules (preferred affinity, spread, image locality,
   least/most allocated).
3. **Bind**, or if nothing fits and the pod has higher priority, try **preemption**.

The scheduler sums **requests**, never actual usage. A node at 10% CPU utilisation can still
reject a pod because requests are fully booked. Capacity it counts is **allocatable**
(capacity minus kube-reserved, system-reserved and eviction threshold):
`kubectl describe node <NODE>` → `Allocatable` and `Allocated resources`.

## 2. Sizing requests
- Start from observed `container_memory_working_set_bytes` and CPU rate over a representative
  period and add headroom; pick the percentile and margin that match your risk tolerance.
- Run VPA in `updateMode: "Off"` to get recommendations without it touching pods.
- Pods with **no requests** are BestEffort: scheduled anywhere, evicted first.
- Set `ephemeral-storage` requests for anything writing logs or scratch to disk so the
  scheduler accounts for local storage.
- Init containers: the Pod's effective request is the higher of the sum of app container requests
  and the highest single init container request.
- Sidecars count: an injected mesh proxy adds its requests to every pod.

## 3. Placement controls (pick the weakest that works)
```yaml
spec:
  nodeSelector: {kubernetes.io/arch: arm64}            # hard, simple equality
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions: [{key: node.kubernetes.io/instance-type, operator: In, values: [m7g.xlarge, m7g.2xlarge]}]
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm: {topologyKey: kubernetes.io/hostname, labelSelector: {matchLabels: {app: api}}}
  tolerations:
  - {key: dedicated, operator: Equal, value: gpu, effect: NoSchedule}
  topologySpreadConstraints:
  - {maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: DoNotSchedule, labelSelector: {matchLabels: {app: api}}, matchLabelKeys: [pod-template-hash]}
  priorityClassName: business-critical
```
- **Taints repel, tolerations permit — they do not attract.** To dedicate nodes, taint them
  *and* add node affinity on the workload.
- `NoExecute` taints evict running pods; `tolerationSeconds` delays it (default 300 s for
  `node.kubernetes.io/not-ready` and `unreachable`, which is why failover takes ~5 min).
- Prefer `topologySpreadConstraints` over pod anti-affinity for spreading: the Kubernetes docs do
  not recommend inter-pod affinity and anti-affinity in clusters larger than several hundred nodes,
  and required anti-affinity limits replicas to the number of domains.
- `matchLabelKeys: [pod-template-hash]` (beta and on by default since Kubernetes 1.27) makes spread
  apply per ReplicaSet so rollouts do not skew.

## 4. Priority and preemption
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata: {name: business-critical}
value: 100000
preemptionPolicy: PreemptLowerPriority
```
- Keep the number of classes small and do not give batch jobs a higher value than serving
  workloads.
- `system-cluster-critical` (2000000000) and `system-node-critical` (2000001000) are the built-in
  classes for critical system pods; user classes may use any 32-bit value up to 1 billion.
- `preemptionPolicy` defaults to `PreemptLowerPriority`; `Never` makes a class non-preempting.
- Preemption respects PDBs only best-effort; a victim can still be killed.
- "Overprovisioning" pattern: low-priority pause pods hold spare capacity so real pods
  preempt them while the autoscaler adds nodes (with Cluster Autoscaler use priority `-10` for
  these pods, per its FAQ).

## 5. Namespace guardrails
- **ResourceQuota** caps total requests/limits/object counts per namespace. Once a quota covers
  a compute resource such as `requests.cpu`, pods must specify a request or limit for it or the
  quota system may reject them at admission.
- **LimitRange** injects default requests/limits into containers that omit them and
  enforces min/max — pair it with every quota.

## 6. Diagnosing Pending
```bash
kubectl get pods --field-selector=status.phase=Pending -A
kubectl describe pod <POD> | sed -n '/Events/,$p'
# "0/12 nodes are available: 3 Insufficient memory, 4 node(s) had untolerated taint {dedicated: gpu}, 5 node(s) didn't match pod topology spread constraints."
kubectl get nodes -L topology.kubernetes.io/zone,node.kubernetes.io/instance-type
kubectl describe node <NODE> | sed -n '/Allocated resources/,/Events/p'
```
Read the counts: they partition all nodes by the *first* filter each failed. Also check the
autoscaler's own events (`TriggeredScaleUp`, `NotTriggerScaleUp`) — the cluster-autoscaler or
Karpenter will not add a node if no node group could satisfy the pod either.

## Gotchas
- `IgnoredDuringExecution` means relabelling a node never moves running pods; use the
  descheduler if you need rebalancing.
- `DoNotSchedule` (the default) leaves a pod Pending when the spread cannot be satisfied, for
  example when a zone has no capacity; `ScheduleAnyway` degrades instead.
- PVC zone binding: a pod with an existing zonal volume can only run in that zone. Use
  `volumeBindingMode: WaitForFirstConsumer` on StorageClasses.
- DaemonSet requests reduce every node's usable capacity; account for them in node sizing.
- Extended resources (such as GPUs) cannot be overcommitted, so request and limit must be equal
  if both are set.
- Huge requests "for safety" waste money and make autoscaling coarse; right-size from data.

## Verify
- [ ] `kubectl get pods -A -o json | jq` shows no containers without CPU and memory requests.
- [ ] Killing one zone's nodes leaves each critical Deployment with ≥ N-1 zones serving.
- [ ] A test pod with no toleration never lands on dedicated nodes.
- [ ] Every Pending pod event explains itself, and the autoscaler reacts within minutes.
- [ ] Each namespace with a ResourceQuota also has a LimitRange.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; latest release v1.37): Pod Priority and Preemption, Taints and Tolerations, Pod Topology Spread Constraints, Assigning Pods to Nodes, Resource Quotas, init containers, managing container resources, and feature-gate stage pages; Cluster Autoscaler FAQ (master) for the overprovisioning priority. Confirmed: 300 s default `tolerationSeconds` for not-ready/unreachable NoExecute taints, built-in priority values, `preemptionPolicy` default, PDBs honoured only best-effort on preemption, `matchLabelKeys` beta since 1.27, `DoNotSchedule` default, effective init-container request rule, extended-resource request=limit rule, quota behaviour (softened to "may reject"). Fixed: anti-affinity guidance now cites the documented scale caveat; quota wording. Removed as unconfirmed: p90-p95 and 20% sizing figures, "3-4 classes", "instantly" and the disk-pressure eviction remark.

Method: documentation only; no commands were run.
