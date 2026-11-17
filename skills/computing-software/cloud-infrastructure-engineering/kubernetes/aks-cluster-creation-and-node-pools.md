---
id: computing-software.cloud-infrastructure-engineering.kubernetes.aks-cluster-creation-and-node-pools
name: aks-cluster-creation-and-node-pools
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, aks, aks-cluster-creation, aks-node-pool, azure-cni-overlay, workload-identity, entra-id, azure]
level: practitioner
status: docs-checked
description: "Create an AKS cluster with az aks: system vs user node pools, Azure CNI Overlay, Entra ID + Azure RBAC, workload identity, availability zones and upgrade channels."
sources: ["https://learn.microsoft.com/en-us/azure/aks/use-system-pools", "https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay", "https://learn.microsoft.com/en-us/azure/aks/azure-cni-powered-by-cilium", "https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster", "https://learn.microsoft.com/en-us/azure/aks/entra-id-authorization", "https://learn.microsoft.com/en-us/azure/aks/local-accounts", "https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype", "https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster", "https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions", "https://learn.microsoft.com/en-us/azure/aks/faq", "https://learn.microsoft.com/en-us/cli/azure/aks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating AKS clusters and node pools

## Create
```bash
# --tier standard = financially backed uptime SLA; drop --outbound-type unless egress goes via your firewall
az aks create -g rg-prod -n aks-prod \
  --kubernetes-version <supported-version> --tier standard \
  --network-plugin azure --network-plugin-mode overlay --network-dataplane cilium \
  --pod-cidr 192.168.0.0/16 \
  --vnet-subnet-id /subscriptions/.../subnets/aks-nodes \
  --enable-aad --enable-azure-rbac --disable-local-accounts \
  --enable-oidc-issuer --enable-workload-identity \
  --nodepool-name system --node-count 3 --node-vm-size <vm-size> \
  --zones 1 2 3 --nodepool-taints CriticalAddonsOnly=true:NoSchedule \
  --auto-upgrade-channel stable --node-os-upgrade-channel NodeImage \
  --enable-cluster-autoscaler --min-count 3 --max-count 5 \
  --outbound-type userDefinedRouting
```
Pick the version from `az aks get-versions --location <region>`; AKS community support for a
minor ends about a year after AKS GA (see the supported versions calendar). The `patch`
auto-upgrade channel never moves to a new minor, so a cluster left on `patch` ages out of
support and AKS then performs a platform-initiated upgrade; `stable` plus a maintenance window
avoids that.

## System vs user pools
- **System** pool (`--mode System`): hosts critical system pods such as CoreDNS and
  metrics-server. At least one is required; it must have at least two nodes (three recommended
  for production), a VM SKU with at least 4 vCPUs and 4 GB memory, and support at least 30 pods.
  Taint it with `CriticalAddonsOnly=true:NoSchedule` so apps do not land there.
- **User** pools for workloads:
```bash
az aks nodepool add -g rg-prod --cluster-name aks-prod -n apps --mode User \
  --node-vm-size <vm-size> --zones 1 2 3 \
  --enable-cluster-autoscaler --min-count 2 --max-count 20 \
  --labels pool=apps --max-surge 33% --os-sku AzureLinux
az aks nodepool add ... -n spot --priority Spot --eviction-policy Delete --spot-max-price -1
```
Pool names: lowercase alphanumeric starting with a letter, 1-12 characters (Linux), 1-6
(Windows). VM size, max pods and the number of availability zones cannot be changed after the
pool is created, and Spot priority and max price are fixed at creation: add a new pool and
delete the old.

## Identity
- `--enable-azure-rbac` lets Azure role assignments (for example "Azure Kubernetes Service RBAC
  Writer" scoped to a namespace) authorize Kubernetes API access; `--disable-local-accounts`
  removes the local admin credentials.
- Workload identity: federated credential on a user-assigned managed identity for
  `system:serviceaccount:<ns>:<sa>`, the ServiceAccount annotated
  `azure.workload.identity/client-id`, and the pod labelled `azure.workload.identity/use: "true"`.

## Gotchas
- Kubenet is being retired; use Azure CNI Overlay (pods get IPs from `--pod-cidr`, default
  `10.244.0.0/16`, not from the VNet) unless pods must be directly routable. With
  `--network-plugin azure` and no `--network-plugin-mode`, AKS uses node-subnet mode.
- The node resource group (`MC_*`) is managed by AKS; do not edit resources in it manually.
- `--outbound-type` can be changed after creation only along the supported migration paths,
  and the change disrupts connectivity and changes egress IPs; decide up front where possible.

## Verify
```bash
az aks show -g rg-prod -n aks-prod --query "{v:kubernetesVersion,net:networkProfile,aad:aadProfile}"
az aks nodepool list -g rg-prod --cluster-name aks-prod -o table
kubectl get nodes -L kubernetes.azure.com/mode,topology.kubernetes.io/zone
```
- [ ] System pool tainted and zonal; user pools autoscale; local accounts disabled.

## Checked
Checked 2026-10-27 against MicrosoftDocs/azure-aks-docs (system node pools: purpose, two-node
minimum, 4 vCPU/4 GB SKU, 30 pods, taint, naming rules; create node pools: VM size and max pods
immutable; availability zones: zone count immutable; Spot pools; Azure CNI Overlay flags and
default pod CIDR; Azure CNI powered by Cilium `--network-dataplane cilium`; Entra ID
authorization roles; local accounts; workload identity annotation and label; outbound type
updates and migration paths; cluster auto-upgrade channels and platform-initiated upgrades;
supported Kubernetes versions calendar; kubenet retirement; FAQ on modifying node resource
group resources) and the Azure CLI `acs` help source
(`--tier`, `--nodepool-taints`, `--node-os-upgrade-channel` values). Replaced the out-of-support
`--kubernetes-version 1.31` (AKS community end of life 1 November 2025) with a placeholder,
switched the example channel from `patch` to `stable`, corrected the claim that outbound type
is fixed at creation, and replaced pinned VM sizes with placeholders.

Method: documentation only; no commands were run.
