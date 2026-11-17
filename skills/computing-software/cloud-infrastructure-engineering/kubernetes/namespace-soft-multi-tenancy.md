---
id: computing-software.cloud-infrastructure-engineering.kubernetes.namespace-soft-multi-tenancy
name: namespace-soft-multi-tenancy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy, namespace, resourcequota, limitrange, networkpolicy, rbac, soft-multi-tenancy, shared-cluster, tenant-isolation, priorityclass, noisy-neighbor]
level: advanced
status: docs-checked
description: "Isolate tenants within one shared cluster using namespaces, ResourceQuota, LimitRange, NetworkPolicy, and RBAC."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://kubernetes.io/docs/concepts/policy/limit-range/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespace soft multi-tenancy — one cluster, isolated-enough tenants

**Goal:** give each tenant (team, customer, environment) a namespace that behaves like
its own cluster for everyday use — can't see others' resources, can't starve others of
CPU/memory, can't be reached over the network by default — without the cost of a
dedicated cluster per tenant. "Soft" means the kernel/node is still shared; see
`computing-software.cloud-infrastructure-engineering.kubernetes.cluster-per-tenant-vs-shared-cluster`
for when soft isolation isn't enough and `computing-software.cloud-infrastructure-engineering.kubernetes.vcluster-virtual-clusters`
for a stronger middle ground.

## 1. The four controls, stacked
A namespace alone provides naming/RBAC-scope isolation only. Full soft multi-tenancy
needs all of:
- **RBAC** — `Role`/`RoleBinding` scoped to the namespace per
  `computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`.
  Prefer namespaced roles for tenants and avoid cluster-scoped permissions.
- **ResourceQuota** — hard caps per namespace on `requests.cpu`, `requests.memory`,
  `limits.cpu`, `limits.memory`, object counts (`count/pods`, `count/services`,
  `count/secrets`). Without it, one tenant's runaway Deployment can starve the whole
  node pool.
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: tenant-quota, namespace: team-a}
spec:
  hard: {requests.cpu: "20", requests.memory: 40Gi, limits.cpu: "40", limits.memory: 80Gi, count/pods: "200"}
```
- **LimitRange** — per-container/pod defaults and min/max, so a pod with no resources
  set still passes a compute quota (the LimitRange defaults are applied before the quota check).
- **NetworkPolicy** — default-deny ingress (and usually egress) per namespace, with
  explicit allow rules for what must cross the boundary (shared platform DNS, an
  ingress controller, specific cross-tenant service calls if genuinely needed).
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: team-a}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
```

## 2. Noisy-neighbor controls beyond quota
- `PriorityClass` per tenant tier so the scheduler can preempt lower-priority pods for
  higher-priority ones and node-pressure eviction ranks pods by priority — quota caps
  steady-state use but doesn't protect against burst contention during scheduling.
- Separate **node pools per tenant tier** (with taints/tolerations) when tenants have
  meaningfully different risk profiles (e.g. an untrusted or highly bursty tenant should
  not share nodes with a latency-sensitive one) — this is a step toward
  `cluster-per-tenant-vs-shared-cluster` without going all the way to separate clusters.
- Namespaces and quotas do not isolate the shared node and kernel — for genuinely adversarial
  tenants, soft multi-tenancy is not a security boundary (see Gotchas).

## Gotchas
- **Soft multi-tenancy is not a security boundary against hostile tenants.** Pods of different
  tenants still share the node, kernel and kubelet (the Kubernetes multi-tenancy docs call out
  node isolation, sandboxing and virtual control planes as further steps). Use namespaces for
  trusted-but-separate internal teams; for mutually hostile tenants, use `vcluster-virtual-clusters`,
  node isolation with sandboxing, or separate clusters.
- With a compute `ResourceQuota`, a pod that does not specify the tracked requests or limits is
  **rejected** at admission unless a `LimitRange` supplies defaults.
- Default-deny NetworkPolicy breaks DNS resolution unless an explicit egress allow for
  kube-dns/CoreDNS is added — a very common "why can't pods resolve anything" outage
  right after rolling out default-deny.
- Quota exhaustion errors (`exceeded quota`) surface at object creation, not at CI/CD
  plan time — a tenant's deploy pipeline needs to surface this clearly or it looks like
  an unrelated failure.
- The `pods` quota counts only pods in a non-terminal phase, while the generic `count/pods`
  counts every Pod object, so completed Job pods can fill a `count/pods` ceiling until deleted.

## Verify
- [ ] Every tenant namespace has RBAC, ResourceQuota, LimitRange, and a default-deny
      NetworkPolicy with explicit allows — checked via a policy-as-code scan
      (see `computing-software.cloud-infrastructure-engineering.kubernetes.policy-enforcement-for-multi-tenancy`),
      not manual review.
- [ ] A test pod with no resources set in a quota'd namespace still gets sane defaults
      from LimitRange and counts correctly against quota.
- [ ] Cross-namespace traffic is blocked by default and only the intended exceptions
      (DNS, shared ingress) work.
- [ ] A load test confirms one tenant exhausting its quota does not degrade another
      tenant's pods on shared nodes.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Namespace, RBAC, quota and network policy as the soft multi-tenancy controls; shared kubelet and API server unless virtual
  control planes are used; node isolation and sandboxing as further steps; NetworkPolicy needs a CNI that enforces it:
  Kubernetes multi-tenancy page.
- Compute quota rejects pods without requests/limits unless a LimitRange applies defaults; `count/<resource>` syntax and
  `pods` counting only non-terminal pods: resource-quotas and limit-range pages.
- Node-pressure eviction considers pod priority: node-pressure eviction page.
- Removed: the claim that quota is bypassed by pods without resources (the opposite is true), the cross-tenant leak claim
  about `nodes` and `persistentvolumes`, and kernel-level side-channel specifics.

Method: documentation only; no commands were run.
