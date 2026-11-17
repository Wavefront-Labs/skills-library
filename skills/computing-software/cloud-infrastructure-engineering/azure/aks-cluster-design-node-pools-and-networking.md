---
id: computing-software.cloud-infrastructure-engineering.azure.aks-cluster-design-node-pools-and-networking
name: aks-cluster-design-node-pools-and-networking
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-cluster, node-pools, aks-networking, azure-cni, azure-cni-overlay, kubenet, cilium, system-node-pool, user-node-pool, cluster-autoscaler, node-autoprovisioning, karpenter, availability-zones, aks-upgrades, auto-upgrade-channel, node-os-upgrade, planned-maintenance, outbound-type, managed-nat-gateway, aks-automatic, uptime-sla, azure-linux]
level: advanced
status: docs-checked
description: "Design an AKS cluster: CNI overlay/Cilium, subnet sizing, system vs user node pools across zones, autoscaler or node auto-provisioning, outbound type, auto-upgrade channels, maintenance, tier/SLA."
sources: ["https://learn.microsoft.com/azure/aks/concepts-network-cni-overview", "https://learn.microsoft.com/azure/aks/azure-cni-overlay", "https://learn.microsoft.com/azure/aks/azure-cni-powered-by-cilium", "https://learn.microsoft.com/azure/aks/update-azure-cni", "https://learn.microsoft.com/azure/aks/use-system-pools", "https://learn.microsoft.com/azure/aks/free-standard-pricing-tiers", "https://learn.microsoft.com/azure/aks/auto-upgrade-cluster", "https://learn.microsoft.com/azure/aks/auto-upgrade-node-os-image", "https://learn.microsoft.com/azure/aks/planned-maintenance", "https://learn.microsoft.com/azure/aks/egress-outboundtype", "https://learn.microsoft.com/azure/aks/private-clusters", "https://learn.microsoft.com/azure/aks/spot-node-pool", "https://learn.microsoft.com/azure/aks/supported-kubernetes-versions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS cluster design — node pools, networking and upgrades decided up front

**Goal:** a cluster whose IP plan won't run out, whose system pods can't be starved by
workloads, that upgrades itself inside a window, and whose outbound path is deliberate.

## 1. Networking choice
| Mode | Pod IPs | Pick when |
|---|---|---|
| **Azure CNI Overlay** (the default when `--network-plugin` is omitted) | private overlay CIDR, nodes from VNet | almost always: conserves VNet IPs, up to 250 pods per node, simpler configuration |
| Azure CNI Node Subnet (legacy flat) | from VNet subnet | pods must be directly routable from VNet/on-prem (rare); `--network-plugin azure` without `--network-plugin-mode` gives this mode |
| Azure CNI Pod Subnet (dynamic IP) | separate pod subnet | routable pods but smaller node subnet |
| kubenet | overlay via UDR | legacy; retires March 31, 2028 - don't start new, migrate to Azure CNI Overlay |
Add the **Cilium** dataplane (`--network-dataplane cilium`, works with Overlay, Pod Subnet and Node Subnet IPAM); Cilium enforces network policy itself, so no separate policy engine is needed. Overlay + Cilium is the default network of AKS Automatic.
Subnet sizing (overlay): only nodes consume VNet addresses, so leave room for surge nodes during upgrades.
`--pod-cidr` defaults to `10.244.0.0/16`; pick `--service-cidr`, `--dns-service-ip` and `--pod-cidr` ranges that do not overlap your peered or on-premises networks.

## 2. Create
```bash
az aks create -g rg -n aks-prod -l uksouth --tier standard \
  --network-plugin azure --network-plugin-mode overlay --network-dataplane cilium --network-policy cilium \
  --vnet-subnet-id <snet-aks> --outbound-type userDefinedRouting \
  --zones 1 2 3 --nodepool-name system --node-count 3 --node-vm-size Standard_D4ds_v5 \
  --enable-managed-identity --assign-identity <uami> --enable-oidc-issuer --enable-workload-identity \
  --enable-aad --enable-azure-rbac --aad-admin-group-object-ids <group> --disable-local-accounts \
  --enable-private-cluster --private-dns-zone <zone-id-or-system> \
  --auto-upgrade-channel patch --node-os-upgrade-channel NodeImage \
  --enable-cluster-autoscaler --min-count 3 --max-count 6 \
  --attach-acr myacr --os-sku AzureLinux
az aks nodepool add -g rg --cluster-name aks-prod -n apps --mode User --node-vm-size Standard_D8ds_v5 \
  --zones 1 2 3 --enable-cluster-autoscaler --min-count 3 --max-count 30 --max-pods 110 \
  --node-taints "" --labels workload=apps --os-sku AzureLinux
az aks nodepool update ... -n system --node-taints CriticalAddonsOnly=true:NoSchedule
```
- `--tier standard` = financially backed uptime SLA (99.95 % API server availability with availability zones, 99.9 % without); `free` is best-effort for dev and test. `premium` adds the SLA plus 24-month long-term support (LTS, which must be enabled).
- **System pool**: at least 2 nodes (3 recommended, across zones), VM SKU of at least 4 vCPU and 4 GB, tainted `CriticalAddonsOnly=true:NoSchedule`; keep apps off it. **User pools** per workload class (general, memory, GPU, Spot
  `--priority Spot --eviction-policy Delete --spot-max-price -1` (the max price must be -1 or positive; spot pools carry the `kubernetes.azure.com/scalesetpriority=spot:NoSchedule` taint), Windows `--os-type Windows`).
- `--outbound-type`: `loadBalancer` (default; SNAT ports are limited, see `--load-balancer-outbound-ports`), `managedNATGateway` (AKS-managed VNet) / `userAssignedNATGateway` (bring-your-own VNet, create the NAT gateway first), `userDefinedRouting` (you configure the egress path, for example a hub firewall) and `none` (no egress configured, no default route required). Changing the outbound type changes the cluster's outbound public IPs.
- **Private cluster**: API server on a private endpoint; use `az aks command invoke` or a jump
  box; or **API server VNet integration** for a routable API server without the private DNS dance.
- Node auto-provisioning (`--node-provisioning-mode Auto`) replaces per-pool autoscaler sizing; clusters that use it cannot be stopped and its node pools cannot be stopped.

## 3. Upgrades
- Control plane: `--auto-upgrade-channel patch|stable|rapid|node-image|none` (`none` is the default, `node-image` is legacy); `stable` = latest patch of minor N-1. Node OS: `--node-os-upgrade-channel NodeImage` (the default for new Standard clusters since API 2023-06-01; weekly cadence), `SecurityPatch`, `Unmanaged` or `None`.
- **Planned maintenance** windows: `az aks maintenanceconfiguration add -g rg --cluster-name aks-prod -n aksManagedAutoUpgradeSchedule --schedule-type Weekly --day-of-week Saturday --interval-weeks 1 --start-time 02:00 --duration 8 --utc-offset +00:00`
  and `aksManagedNodeOSUpgradeSchedule` for node OS patching. With auto-upgrade use a window of four hours or more. Without windows, upgrades happen whenever.
- Manual: `az aks get-upgrades`, `az aks upgrade --kubernetes-version 1.32.x` (control plane
  then pools, or `--control-plane-only`); per-pool `az aks nodepool upgrade` with
  `--max-surge 33%` and **PodDisruptionBudgets** that allow at least one eviction; a PDB
  that allows none blocks the drain. `--drain-timeout` (minutes) bounds the wait and
  `--undrainable-node-behavior Cordon|Schedule` (default `Schedule`) decides what happens to nodes that cannot be drained.
- AKS supports three GA minor versions (N, N-1, N-2); LTS (Premium tier) extends support to 24 months. Clusters that stay on an unsupported version past the 60-day grace period get a platform-initiated upgrade.

## 4. Baseline add-ons
`--enable-addons monitoring` (Container Insights with Prometheus → Managed Prometheus +
Managed Grafana via `--enable-azure-monitor-metrics`), `azure-keyvault-secrets-provider`
(Secrets Store CSI), `--enable-image-cleaner`, `--enable-defender`, `--enable-azure-policy`
(Gatekeeper), **Application Routing** add-on (managed NGINX ingress) or App Gateway for
Containers / AGIC. KEDA (`--enable-keda`) and VPA add-ons exist. Prefer add-ons over
self-managed Helm for these; they're upgraded with the cluster.

## 5. Capacity and cost
Cluster autoscaler behaviour is tuned with `--cluster-autoscaler-profile key=value ...`.
Spot pools for batch need a toleration for the `kubernetes.azure.com/scalesetpriority=spot:NoSchedule` taint.
Start/stop (`az aks stop`) for dev clusters. Set `--max-pods` deliberately; system pools must support at least 30 pods.

## Gotchas
- Changing the IPAM mode after creation is a forward-only migration: only Azure CNI Node Subnet and kubenet clusters can move to Azure CNI Overlay, and it cannot be reversed. Moving to the Cilium dataplane is a separate update that does not change the IPAM mode.
- Overlay pods aren't reachable from the VNet; services via internal LB (`service.beta.kubernetes.io/azure-load-balancer-internal: "true"`).
- UDR outbound without the egress rules AKS requires leaves nodes unable to bootstrap; follow the limit-egress-traffic article for the required FQDNs.
- A custom private DNS zone (format `privatelink.<region>.azmk8s.io`) needs a user-assigned identity with *Private DNS Zone Contributor* and *Network Contributor* roles, passed with `--assign-identity`, before create.

## Verify
- [ ] `kubectl get nodes -L topology.kubernetes.io/zone` shows pools spread across the zones; system nodes carry the `CriticalAddonsOnly` taint and only kube-system pods.
- [ ] `az aks show --query "{tier:sku.tier,ch:autoUpgradeProfile,out:networkProfile.outboundType,plugin:networkProfile.networkPluginMode}"` matches design.
- [ ] Test upgrade of a user pool completes with PDB-respecting evictions; app error rate flat.
- [ ] `az aks check-acr --acr myacr.azurecr.io` passes from nodes; a pod can pull a private image.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (concepts-network-cni-overview, azure-cni-overlay, azure-cni-powered-by-cilium, update-azure-cni, use-system-pools, free-standard-pricing-tiers, auto-upgrade-cluster, auto-upgrade-node-os-image, planned-maintenance, egress-outboundtype, private-clusters, spot-node-pool, supported-kubernetes-versions; main branch) and the Azure CLI `acs` module parameter definitions for the `az aks create` flags used.
- Corrected: API server SLA is 99.95 % with availability zones and 99.9 % without (not 99.99 %); kubenet retires on 31 March 2028; Azure CNI Overlay is the default only when `--network-plugin` is omitted; system pool minimum is two nodes (three recommended) with at least 4 vCPU and 4 GB.
- Confirmed: overlay pod limit 250 per node, `--network-dataplane cilium`, default pod CIDR, outbound types, maintenance configuration names and flags, auto-upgrade channel names, node OS channel values and default, `--undrainable-node-behavior` values, spot flags and taint, N to N-2 support and 24-month LTS on Premium, 60-day platform grace period, IPAM migration direction.
- Removed as unconfirmed: subnet sizing arithmetic, the 30-minute drain timeout, `--max-pods` advice, node resource group lock, Windows pool requirements, specific egress FQDNs, autoscaler profile values and Hubble.
Method: documentation only; no commands were run.
