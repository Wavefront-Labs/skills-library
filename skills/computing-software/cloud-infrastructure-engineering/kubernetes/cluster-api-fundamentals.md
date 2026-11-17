---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-fundamentals
name: cluster-api-fundamentals
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-api, capi, clusterctl, infrastructure-provider, bootstrap-provider, control-plane-provider, management-cluster, workload-cluster, kubeadm, cluster-crd, machinedeployment, machineset, machine, kind, declarative-cluster-lifecycle, multi-cluster]
level: advanced
status: docs-checked
description: "Stand up and manage Kubernetes clusters declaratively with Cluster API: the provider model, management vs workload clusters, and the core object graph."
sources: ["https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/concepts.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/reference/versions.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/reference/clusterctl/commands/get-kubeconfig.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster API fundamentals

**Goal:** treat cluster creation, scaling and teardown as Kubernetes objects on a management cluster, so clusters are reconciled like workloads.

## 1. The provider model
Cluster API providers run as controllers on the management cluster:
- **Infrastructure provider** provisions VMs, networks and so on (AWS, Azure, Google, vSphere, bare metal such as metal3.io; when one infrastructure offers several ways, such as EC2 and EKS, each is a variant).
- **Bootstrap provider** turns a machine into a node: generates certificates, initializes the control plane, joins nodes, via bootstrap data (usually cloud-init). The kubeadm bootstrap provider is the usual one.
- **Control plane provider** manages the control plane; `KubeadmControlPlane` manages Machines running kubeadm control plane nodes. Control planes may also be pod-based or external/managed (GKE, AKS, EKS).
Install providers with `clusterctl init --infrastructure aws` (provider-specific credentials are described in each provider's docs).

## 2. Management and workload clusters
- The management cluster runs Cluster API and providers. A workload cluster is a `Cluster` object (plus children) the management cluster reconciles.
- `clusterctl move` pivots the objects to another management cluster; the documented use case is bootstrap and pivot (see `clusterctl-move-management-cluster-pivot`).
- Keep an at-least-one-worker management cluster: Cluster API controllers need a schedulable node.

## 3. Core object graph (v1beta2)
```
Cluster                        # infrastructureRef + controlPlaneRef, clusterNetwork
|- <Provider>Cluster           # e.g. VSphereCluster
|- KubeadmControlPlane         # control plane Machines
|   `- Machine -> <Provider>Machine, bootstrap config
`- MachineDeployment           # per worker pool
    `- MachineSet -> Machine -> <Provider>Machine, bootstrap config
```
- Machines are immutable (only labels, annotations, status change); changes roll out by replacement. Prefer MachineDeployments (like Deployments) over single Machines. Deleting a Machine deletes its infrastructure and Node.
- MachinePool is a provider-specific group of machines; MachineSet is the ReplicaSet-like object used by MachineDeployments.
- `clusterctl get kubeconfig <cluster> [--namespace <ns>]` prints a workload cluster kubeconfig.
- `clusterctl describe cluster <name>` shows the object tree.

## 4. API versions
`cluster.x-k8s.io/v1beta2` is supported; `v1beta1` is deprecated since Cluster API v1.11 and stops being served in v1.16 (April 2027). The latest release line at the time of checking was v1.14.x. Cluster API releases support one contract version, and clusterctl and providers must match.

## 5. Gotchas
- Provider versions in the target management cluster must be at least those in the source before `clusterctl move`.
- Use `clusterctl upgrade plan` to see upgrade targets.
- Cluster API provider CRD and `clusterctl` versions are coupled by the contract; check the versions page before mixing releases.

## Verify
- [ ] `kubectl get cluster,machines -n <ns>` shows Provisioned/Running phases.
- [ ] A workload cluster kubeconfig from `clusterctl get kubeconfig` authenticates.
- [ ] A test MachineDeployment scale-up and scale-down completes.

## Checked

Checked 2026-10-26 against Cluster API book (main branch, latest commit 2026-10-22; latest release v1.14.3). Confirmed: provider roles, Machine immutability, object graph, clusterctl get kubeconfig, API version status (v1beta2 supported, v1beta1 deprecated).

Method: documentation only; no commands were run.
