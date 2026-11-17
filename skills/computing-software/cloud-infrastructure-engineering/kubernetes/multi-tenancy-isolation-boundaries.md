---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-tenancy-isolation-boundaries
name: multi-tenancy-isolation-boundaries
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy, namespace-isolation, resourcequota, limitrange, soft-multi-tenancy, hard-multi-tenancy, vcluster, hierarchical-namespaces, control-plane-isolation, noisy-neighbor, kube-system]
level: advanced
status: docs-checked
description: "Namespaces as a soft multi-tenancy boundary, where ResourceQuota and LimitRange stop noisy neighbours, and when to escalate to virtual clusters or separate clusters."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://github.com/kubernetes-sigs/hierarchical-namespaces", "https://github.com/loft-sh/vcluster", "https://github.com/projectcapsule/capsule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-tenancy — what a namespace boundary actually promises

**Goal:** stop treating "put each tenant in its own namespace" as a finished
security answer, and know which specific control from the other skills in this
set closes which specific gap — namespaces alone promise almost nothing. RBAC
scoping and ServiceAccount hygiene are in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`
and
`computing-software.cloud-infrastructure-engineering.kubernetes.service-account-token-security`;
network isolation is in
`computing-software.cloud-infrastructure-engineering.kubernetes.network-policy-security-boundary`.

## 1. A namespace alone is an organizational boundary, not a security one
Namespaces scope names and let RBAC/NetworkPolicy/ResourceQuota *target* them —
by themselves they do nothing. A cluster with ten namespaces and no RBAC,
NetworkPolicy, or quota differences between them has ten folders, not ten
tenants. "Soft multi-tenancy" (trusted tenants, e.g. different teams in the
same company) is the realistic target for namespace-based isolation; "hard
multi-tenancy" (mutually untrusting tenants, e.g. different paying customers
who might attack each other) generally needs a stronger boundary than
namespace + RBAC + NetworkPolicy can provide — see §4.

Kubernetes' own multi-tenancy documentation notes that "hard" and "soft" are confusing terms with no
single definition, and frames the choice as multi-team tenancy (tenants are teams in one organization)
versus multi-customer tenancy.

## 2. ResourceQuota and LimitRange — the noisy-neighbor control
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: tenant-a, namespace: tenant-a}
spec:
  hard: {requests.cpu: "20", requests.memory: 40Gi, limits.cpu: "40", limits.memory: 80Gi, pods: "100", persistentvolumeclaims: "20"}
---
apiVersion: v1
kind: LimitRange
metadata: {name: default-limits, namespace: tenant-a}
spec:
  limits: [{type: Container, default: {cpu: 500m, memory: 512Mi}, defaultRequest: {cpu: 250m, memory: 256Mi}}]
```
- `ResourceQuota` caps the namespace's **aggregate** consumption — without it,
  one tenant's unbounded Deployment can starve every other tenant on
  shared nodes of schedulable capacity, a pure availability (not
  confidentiality) failure but still a real cross-tenant harm.
- `LimitRange` supplies **defaults** for pods that specify no
  requests/limits at all — without a `LimitRange`, a `ResourceQuota` that
  requires `requests.cpu` on the namespace causes every pod *without* an
  explicit request to be **rejected outright** at admission, which surprises
  teams who only tested with fully-specified pod specs. Set both together.
- Quota is **per-namespace**; a tenant spread across multiple namespaces needs
  quota applied to each, or an aggregating mechanism (hierarchical namespaces,
  §3) — forgetting a quota on a secondary namespace a tenant was given
  reopens the exact gap the primary namespace's quota closed.

## 3. Hierarchical Namespaces and policy inheritance
The Hierarchical Namespace Controller (HNC) propagates objects from a parent namespace to its
children. By default HNC propagates only RBAC Roles and RoleBindings; it can be configured to
propagate other kinds, including custom resources. This is useful when one tenant legitimately needs
several namespaces (per-environment: `tenant-a-dev`, `tenant-a-staging`) and you want policy
defined once rather than copy-pasted and drifting. HNC also offers hierarchical resource quotas
(HRQ), which were beta in HNC v1.1 and are not installed by default. HNC does not make isolation
stronger between unrelated tenants; it reduces policy drift within one tenant's namespace tree.

## 4. Where namespace-based isolation stops, and the escalation paths
Shared-control-plane multi-tenancy (even with full RBAC/quota/NetworkPolicy)
still shares: the kube-apiserver and its blast radius if compromised, the
underlying node kernel (unless sandboxed per
`kubelet-and-node-hardening`'s RuntimeClass discussion), etcd, and any
cluster-scoped resource (CRDs, StorageClasses, admission webhook configs) that
no namespace boundary can scope. For hard multi-tenancy, in increasing order
of isolation and cost:
- **Sandboxed runtime per tenant** (via `RuntimeClass`) — Kubernetes' multi-tenancy docs describe
  virtual machines and userspace kernels as sandboxing approaches that insulate the host from
  container escapes; this addresses the shared-kernel risk specifically.
- **Virtual clusters** (for example vCluster) — each tenant gets its own Kubernetes API server and
  control plane, so tenants can install their own CRDs, which avoids conflicts over cluster-scoped
  objects such as CRDs and webhooks in a shared control plane. Check the product documentation for
  whether worker nodes and the kernel remain shared in the mode you choose. (Capsule is a different
  model: it groups several namespaces into a Tenant inside one shared cluster.)
- **Dedicated node pools per tenant** (`nodeSelector`/taints+tolerations
  scoping each tenant to its own nodes) — removes noisy-neighbor and
  node-level cross-tenant exposure (one tenant's compromised node never has
  another tenant's pods on it), at the cost of losing bin-packing efficiency
  across tenants.
- **Separate clusters per tenant** — full isolation, including the control
  plane and etcd; highest operational cost (N times the cluster-lifecycle
  burden).
Pick the level that matches the actual trust relationship between tenants —
most internal multi-team setups don't need separate clusters; most
true multi-customer SaaS platforms with adversarial incentives between
tenants eventually do, or land on vclusters/dedicated nodes as a middle
ground.

## Gotchas
- `kube-system` and other cluster-infrastructure namespaces are not a tenant
  namespace and should never be in scope for any tenant's RBAC/NetworkPolicy
  — a webhook/policy accidentally scoped broadly enough to include it (see the
  `namespaceSelector` exclusion pattern in `admission-webhooks-validating-and-
  mutating`) risks tenant policy interfering with cluster infrastructure.
- `ResourceQuota` does not cap **node-level** resources like ephemeral
  storage from unbounded log/temp-file growth unless `requests.ephemeral-
  storage`/`limits.ephemeral-storage` are explicitly included — a quota that
  only covers CPU/memory still lets one tenant fill a shared node's disk.
- CRDs installed for one tenant's use are **cluster-scoped by definition** —
  there's no native per-namespace CRD; a tenant with CRD-creation RBAC (rare,
  but check) can affect every other tenant's view of that CRD's schema.

## Verify
- [ ] Every tenant namespace has both `ResourceQuota` and a matching
      `LimitRange` — tested by deploying a pod with no explicit
      requests/limits and confirming it gets sane defaults rather than being
      rejected or left unbounded.
- [ ] Ephemeral storage is included in quota, not just CPU/memory.
- [ ] No tenant-scoped RBAC or NetworkPolicy selector is broad enough to match
      `kube-system` or other infrastructure namespaces.
- [ ] The trust relationship between tenants has been explicitly matched to an
      isolation tier (namespace-only vs. sandboxed runtime vs. vcluster vs.
      dedicated nodes vs. separate cluster) — not defaulted to namespaces
      because that's what was easiest to set up first.
- [ ] If tenants span multiple namespaces, quota and policy are confirmed
      applied to every one of them, not just the first/primary namespace
      created for that tenant.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026; HNC, vCluster and Capsule READMEs (main)
- Confirmed in the Kubernetes resource quota page that quotas can cover `requests.ephemeral-storage` and `limits.ephemeral-storage`, that a LimitRange supplies defaults for pods that declare no compute requirements, and that creating a pod without requests is rejected when the quota limits that resource.
- Corrected HNC behaviour from the HNC concepts guide: by default it propagates only RBAC Roles and RoleBindings (other kinds are configurable), and hierarchical resource quotas are beta in v1.1 and not installed by default.
- Corrected the virtual-cluster entry: Capsule groups namespaces into Tenants within one shared cluster (Capsule README), unlike vCluster's per-tenant control plane (vCluster README); confirmed node isolation with taints and tolerations, sandboxing with VMs or userspace kernels, and CRD and webhook conflicts in a shared control plane in the Kubernetes multi-tenancy page.
- Removed the unsupported claim that separate clusters are the only option removing shared-fate risk from a cluster-level 0-day.

Method: documentation only; no commands were run.
