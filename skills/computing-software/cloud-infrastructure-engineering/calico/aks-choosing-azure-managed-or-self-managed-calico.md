---
id: computing-software.cloud-infrastructure-engineering.calico.aks-choosing-azure-managed-or-self-managed-calico
name: aks-choosing-azure-managed-or-self-managed-calico
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [aks, azure, azure-cni, network-policy, azure-managed, self-managed, az-aks-create]
level: practitioner
status: docs-checked
description: "Choose between Azure-managed Calico policy, self-managed Calico policy on Azure CNI, or Calico CNI on AKS, and run the az aks create flags that select each option."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/managed-public-cloud/aks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AKS has three Calico options. What differs is who manages Calico and which features you get.

| Option | Networking | Policy | Managed by | Features |
|---|---|---|---|---|
| 1. Azure-managed | Azure CNI | Azure-managed Calico | Azure installs, upgrades, supports | Standard Kubernetes Network Policy API only |
| 2. Self-managed policy | Azure CNI | Your Calico | You | Calico and global policy, Whisker observability |
| 3. Self-managed networking and policy | Calico CNI | Calico | You | Full Calico stack |

For options 2 and 3 the cluster is supported by Azure, while Calico features are supported by the community or a commercial plan.

**Option 1 cluster:**

```bash
az group create --name my-calico-rg --location westcentralus
az aks create \
  --resource-group my-calico-rg \
  --name my-calico-cluster \
  --location westcentralus \
  --pod-cidr 192.168.0.0/16 \
  --network-plugin azure \
  --network-policy calico
```

**Option 2 cluster:** the same command with `--network-policy none`. Then `az aks get-credentials --resource-group my-calico-rg --name my-calico-cluster`, install the Calico CRDs (the v3 manifest, with a `v1beta1` variant for Kubernetes 1.34 or 1.35) and the Tigera Operator.

Prerequisites: an Azure account able to create resource groups and AKS clusters, and the `az` CLI.

**Option 3 cluster:** the same command with `--network-plugin none` (no CNI pre-installed; see Bring your own CNI with AKS). Install the CRDs and Tigera Operator as above, then an Installation with `kubernetesProvider: AKS`, `cni.type: Calico`, `calicoNetwork.bgp: Disabled` and an IP pool using `encapsulation: VXLAN`. Check with `kubectl get tigerastatus`. Windows and VPP data planes are not supported.

## Checked

2026-11-08. The three options, the option 1 and option 2 cluster commands, the CRD manifest variants and the option 3 steps and limitations were read in full on the Installing on AKS page (Calico 3.33 docs).

Method: documentation only; no commands were run.
