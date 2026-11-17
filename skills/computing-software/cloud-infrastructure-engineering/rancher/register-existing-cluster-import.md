---
id: computing-software.cloud-infrastructure-engineering.rancher.register-existing-cluster-import
name: register-existing-cluster-import
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [import, registered-clusters, cluster-admin, eks, aks, gke, agent-environment-variables, no-proxy]
level: practitioner
status: docs-checked
description: "Import an existing Kubernetes cluster into Rancher: cluster-admin and node role prerequisites, AKS and GKE limits, the registration command, proxy variables, and delete behaviour."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-clusters-in-rancher-setup/register-existing-clusters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registration replaced the older "import" feature, and how much Rancher can manage depends on the cluster type.

**Prerequisites**

- You need `cluster-admin` in the target cluster. GKE does not grant it by default, so create a ClusterRoleBinding to `cluster-admin` for your user first.
- Registered RKE clusters must have all three roles: etcd, controlplane and worker.
- EKS, AKS and GKE clusters need at least one managed node group.
- AKS can only be imported if **local accounts are enabled**; clusters using Microsoft Entra ID for authentication fail with an error.
- GKE Autopilot is not supported.
- EKS Anywhere can be registered but is treated as imported, without full lifecycle support.

**Procedure:** **Cluster Management > Import Existing**, choose the type, set Member Roles, and for a generic cluster optionally set Agent Environment Variables (including `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`), Project Network Isolation, and version management for RKE2 and K3s. Click **Create**, then run the displayed `kubectl` command on a node whose kubeconfig points at the target. With self-signed Rancher certificates you will see `certificate signed by unknown authority`; use the displayed `curl` variant instead. `NO_PROXY` must follow the Golang format: comma-delimited IPs, CIDRs, domain names or special labels such as `*`.

The cluster appears as **Pending**, then **Active**, with `Default` and `System` projects. An active cluster cannot be re-registered.

Deleting a registered EKS, AKS or GKE cluster in Rancher only **disconnects** it; the cluster stays live, unlike clusters Rancher created. For Terraform imports, define only the minimum fields (for EKS: cloud credential, name, region and `imported = true`), since Rancher overwrites differing configuration.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Registering Existing Clusters. Nothing removed.

Method: documentation only; no commands were run.
