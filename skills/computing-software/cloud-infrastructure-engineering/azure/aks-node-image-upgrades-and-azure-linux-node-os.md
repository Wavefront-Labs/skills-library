---
id: computing-software.cloud-infrastructure-engineering.azure.aks-node-image-upgrades-and-azure-linux-node-os
name: aks-node-image-upgrades-and-azure-linux-node-os
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, node-image-upgrade, azure-linux-node-os, node-os-upgrade-channel, os-sku, maintenance-window]
level: practitioner
status: docs-checked
description: "Keep AKS nodes patched: node image upgrades, node OS upgrade channels and maintenance windows, and adopting or migrating node pools to Azure Linux."
sources: ["https://learn.microsoft.com/azure/aks/upgrade-node-image", "https://learn.microsoft.com/azure/aks/auto-upgrade-node-os-image", "https://learn.microsoft.com/azure/aks/upgrade-os-version", "https://learn.microsoft.com/azure/aks/use-azure-linux", "https://learn.microsoft.com/azure/aks/planned-maintenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS node image upgrades and Azure Linux

**Goal:** weekly OS patches on nodes without Kubernetes version changes, and a lean, Microsoft-maintained node OS.

## Node image upgrades (manual)
```bash
az aks nodepool get-upgrades -g rg -n aks01 --nodepool-name user1 --query latestNodeImageVersion
az aks nodepool show -g rg --cluster-name aks01 -n user1 --query nodeImageVersion
az aks nodepool upgrade -g rg --cluster-name aks01 -n user1 --node-image-only --max-surge 33%
```
Node image upgrades cordon/drain/replace nodes like version upgrades; respect PodDisruptionBudgets.

## Automatic: node OS upgrade channel
```bash
az aks update -g rg -n aks01 --node-os-upgrade-channel NodeImage
az aks maintenanceconfiguration add -g rg --cluster-name aks01 -n aksManagedNodeOSUpgradeSchedule \
  --schedule-type Weekly --day-of-week Sunday --interval-weeks 1 --start-time 02:00 --duration 4 --utc-offset +00:00
```
Channels: `NodeImage` (new node image on a weekly cadence; the default for new Standard clusters since API version 2023-06-01), `SecurityPatch` (AKS-tested, security-only VHD updates applied with safe deployment practices), `Unmanaged` (the OS's own unattended upgrades) and `None`. Separate from the cluster auto-upgrade channel (Kubernetes versions) and its `aksManagedAutoUpgradeSchedule` window. With the `NodeImage` channel Linux unattended upgrades are disabled by default.

## Azure Linux node OS
- Open-source Linux distribution created by Microsoft for AKS container hosts; packages are built from source and validated, and the image is lightweight.
- New pool: `az aks nodepool add -g rg --cluster-name aks01 -n azl1 --os-sku AzureLinux`
- Migrate an existing Linux pool in place by updating its OS SKU (the command can fail if the target OS has no node image for your Kubernetes version, VM size or FIPS setting). `AzureLinux` follows the default Azure Linux version for your Kubernetes version; versioned SKUs such as `AzureLinux3` must be migrated manually before Kubernetes upgrades:
```bash
az aks nodepool update -g rg --cluster-name aks01 -n user1 --os-sku AzureLinux
```
  Or add an Azure Linux pool, cordon/drain the Ubuntu pool, delete it.

## Gotchas
- DaemonSets or agents that assume Ubuntu packages/paths (apt, specific kernel modules) need validation on Azure Linux.
- A higher `--max-surge` speeds upgrades but needs spare VM quota (and IPs on node-subnet networking); a PodDisruptionBudget that allows no disruption blocks drains and stalls upgrades.

## Verify
- [ ] All pools on the latest node image (or within one week); maintenance window configured; Azure Linux pools pass workload tests.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (upgrade-node-image, auto-upgrade-node-os-image, upgrade-os-version, use-azure-linux, planned-maintenance; main branch) and the Azure CLI `acs` help for `--max-surge` and `--node-image-only`.
- Confirmed: `az aks nodepool get-upgrades` output `latestNodeImageVersion` versus `nodeImageVersion`; `--node-image-only`; node OS channel values, weekly NodeImage cadence and default; `aksManagedNodeOSUpgradeSchedule`; in-place `az aks nodepool update --os-sku` between Linux SKUs and its failure condition; versioned OS SKUs need manual migration.
- Removed as unconfirmed: faster boot and fewer packages marketing claims, "rolling reimage" detail, and the node-subnet sizing remark beyond spare IPs.
Method: documentation only; no commands were run.
