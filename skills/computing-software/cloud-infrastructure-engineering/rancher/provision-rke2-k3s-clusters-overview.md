---
id: computing-software.cloud-infrastructure-engineering.rancher.provision-rke2-k3s-clusters-overview
name: provision-rke2-k3s-clusters-overview
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [provisioning, rke2, k3s, capi, machine-pools, custom-clusters, windows]
level: practitioner
status: docs-checked
description: "How Rancher launches RKE2 and K3s clusters on new infrastructure nodes or existing custom nodes, CAPI-based provisioning, CNI choices, reprovisioning and Windows notes."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/launch-kubernetes-with-rancher
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher can install Kubernetes on bare metal, on-premises VMs, or VMs from an infrastructure provider, either dynamically provisioning nodes or using **existing custom nodes**. With provider-hosted **machine pools**, if a node loses connectivity Rancher can create a replacement so the pool count stays as expected.

RKE2 provisioning arrived in Rancher v2.6 (tech preview up to v2.6.4, GA in v2.6.5). Nodes must meet the RKE2 requirements for downstream clusters. It is built on the upstream Cluster API (CAPI) framework, which lets you:

- provision RKE2 clusters on any provider that has a Rancher node driver;
- fully configure RKE2 inside Rancher;
- choose Calico, Cilium or Multus as CNI options in addition to Canal.

Because CAPI controllers drive it, **configuration changes may reprovision nodes**. The page's example: enabling drain before delete on an existing cluster deletes the existing control plane and worker nodes and creates new ones. The same behaviour does not apply to etcd nodes.

Windows is supported for RKE2 with the vSphere node driver, Calico and Flannel CNI for custom clusters, Project Network Isolation for Calico, containerd, Terraform provisioning and custom clusters from the UI. Windows custom clusters require **Calico** as the CNI.

For custom clusters, any node previously used in a cluster must be cleaned before reuse, or provisioning may fail. For automation, the page names the Rancher2 Terraform provider as the most common programmatic route.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Launching Kubernetes with Rancher. Removed the cluster_v2 resource name, which is not on the page.

Method: documentation only; no commands were run.
