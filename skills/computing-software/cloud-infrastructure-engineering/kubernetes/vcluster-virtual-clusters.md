---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vcluster-virtual-clusters
name: vcluster-virtual-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vcluster, virtual-cluster, multi-tenancy, k3s, syncer, host-cluster, tenant-isolation, crd-isolation, cluster-scoped-resources, sleep-mode, vcluster-platform]
level: advanced
status: docs-checked
description: "Give each tenant a full virtual Kubernetes API server inside one host cluster with vcluster, for stronger isolation than namespaces without cluster-per-tenant cost."
sources: ["https://www.vcluster.com/docs/vcluster/introduction/architecture", "https://www.vcluster.com/docs/vcluster/configure/vcluster-yaml/sleep", "https://www.vcluster.com/docs/vcluster/configure/vcluster-yaml/policies/resource-quota", "https://www.vcluster.com/docs/vcluster/manage/upgrade/supported_versions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vcluster — a real API server per tenant, one host cluster's worth of nodes

**Goal:** give each tenant their own Kubernetes API server (so they can create
CRDs, cluster-scoped RBAC, even other namespaces, without touching anyone else's) while
all vclusters still schedule pods onto the same underlying host-cluster nodes — cheaper
than `computing-software.cloud-infrastructure-engineering.kubernetes.cluster-per-tenant-vs-shared-cluster`'s
dedicated-cluster option, stronger isolation than
`computing-software.cloud-infrastructure-engineering.kubernetes.namespace-soft-multi-tenancy`.

## 1. How it works
- A vcluster (on an existing Kubernetes cluster, the default placement) runs in its own namespace of the
  **host cluster** as a StatefulSet pod: one container holding the Kubernetes API server, controller manager,
  data store (embedded SQLite by default; etcd and other stores are options) and the syncer, plus a separate
  CoreDNS pod. Tenants can create `CustomResourceDefinition`s and `Namespace`s inside it, scoped to their
  virtual cluster.
- A **syncer** component translates real workloads: when a tenant creates a Pod in
  their vcluster, the syncer creates the *actual* Pod in a host-cluster namespace
  (one per vcluster) so it schedules on real nodes. With shared nodes, Pods, Secrets, ConfigMaps, Services,
  Endpoints and PersistentVolumeClaims sync by default; Ingresses, Gateway API objects, NetworkPolicies,
  PersistentVolumes, StorageClasses, ServiceAccounts, PodDisruptionBudgets, PriorityClasses, Namespaces and
  custom resources do not unless enabled. Other resources (CRDs, RBAC) live only inside the vcluster.
- Objects synced to the host namespace carry owner references back to the vcluster, so deleting the vcluster
  or its namespace removes them.

## 2. When this beats plain namespaces
- A tenant needs to install their own CRDs/Operators, or needs cluster-scoped RBAC for
  a tool that assumes it (many Helm charts assume `ClusterRole` access) — namespace
  multi-tenancy can't safely grant that; vcluster can, because "cluster-scoped" is
  contained.
- Tenants need a different Kubernetes distribution or version from the host: each vcluster has its own
  control plane, so its distribution does not need to match the host's, within the supported combinations in
  the Kubernetes compatibility matrix.
- You want to offer "your own cluster" self-service UX while still consolidating compute onto shared nodes.

## 3. Operational notes
- **Shared nodes are not a security boundary for untrusted tenants.** With shared nodes tenants share the
  same kernel and worker nodes (same caveat as namespace multi-tenancy re: hostile tenants — see
  `namespace-soft-multi-tenancy`'s Gotchas). Private nodes give each cluster dedicated nodes, CNI and CSI;
  Dedicated Nodes scope workloads to a labelled node pool.
- **Sleep mode**: configure `sleep.auto.afterInactivity` (for example `1h`) in `vcluster.yaml`. Without a
  platform agent the cluster scales down its workloads and its control plane stays running to detect
  activity; with vCluster Platform the control plane can be scaled down too. `vcluster pause <name>
  --namespace <ns>` pauses manually. Check the idle timeout before offering it to tenants who expect always-on
  availability.
- A host-side cap comes from `policies.resourceQuota` in `vcluster.yaml`: vcluster creates the ResourceQuota
  in the vcluster's own host namespace, and it applies to all resources synced to the host.

## Gotchas
- Debugging crosses two API servers: `kubectl` against the vcluster shows the tenant's
  view; the actual Pod/Service lives in a differently-named object in the host
  cluster's backing namespace — tooling (log aggregation, cost allocation) needs to
  know both to correlate.
- Not every resource type syncs by default — check the `sync.toHost` settings in `vcluster.yaml` before
  assuming e.g. an Ingress or a given CRD's instances will reach the host.
- Host-cluster node-level failures (kubelet issues, node pressure) still affect every
  vcluster scheduled there — vcluster does not add node-level fault isolation between
  tenants.
- vcluster supports specific Kubernetes versions on the host cluster; check the Kubernetes compatibility
  matrix in the lifecycle policy before a host upgrade.

## Verify
- [ ] A tenant can install a CRD and create cluster-scoped RBAC inside their vcluster
      with zero visibility or effect on another tenant's vcluster or the host.
- [ ] `kubectl get pods` in the vcluster and the corresponding host-cluster namespace
      both show the workload, confirming the syncer is working end to end.
- [ ] Host-cluster ResourceQuota on the backing namespace actually caps the tenant's
      real resource consumption (tested by over-requesting inside the vcluster).
- [ ] A paused or sleeping vcluster resumes correctly, with the resume latency acceptable for the use case it's offered for.

## Checked

Checked against `loft-sh/vcluster-docs` main (pushed 2026-10-23): introduction/architecture, configure/vcluster-yaml/sleep, manage/sleep-wakeup, configure/vcluster-yaml/policies/resource-quota, manage/upgrade/supported_versions, and the sync-to-host and distro fragments.
Confirmed: control plane components in a StatefulSet with SQLite default; default and non-default synced resources; owner references and cleanup; shared versus private nodes and the untrusted-tenant caveat; `sleep.auto.afterInactivity`; `policies.resourceQuota` placement; the Kubernetes compatibility matrix.
Wrong in the draft: k3s as the usual API server and `--sync` flags (configuration is `sync.toHost` in `vcluster.yaml`); the claim that sleep scales the control plane to zero (only with Platform). Removed as unconfirmed: cluster-admin safety wording and "created in seconds".

Method: documentation only; no commands were run.
