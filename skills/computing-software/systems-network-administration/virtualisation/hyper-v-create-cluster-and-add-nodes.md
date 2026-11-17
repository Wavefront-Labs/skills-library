---
id: computing-software.systems-network-administration.virtualisation.hyper-v-create-cluster-and-add-nodes
name: hyper-v-create-cluster-and-add-nodes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [new-cluster, add-clusternode, failover-cluster, hyper-v]
level: practitioner
status: docs-checked
description: "Create a Hyper-V failover cluster and add nodes with PowerShell: validation, AD permissions, static address, quorum witness, CSVs and post-checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/create-failover-cluster
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-cluster
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/add-clusternode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a cluster and add nodes

**Goal:** a validated Hyper-V cluster with shared storage, a witness and consistent node configuration.

## Prepare every node
```powershell
Install-WindowsFeature Hyper-V, Failover-Clustering -IncludeManagementTools -Restart
```
Shared LUNs must be presented to all nodes (or use S2D drives); validate the configuration before creating the cluster.

## Validate and create
```powershell
Test-Cluster -Node hv01,hv02,hv03
New-Cluster -Name HVCL01 -Node hv01,hv02,hv03 -StaticAddress 10.0.0.50 -NoStorage
```
- The installing user needs *Create Computer objects* on the OU or container that holds the node computer objects, or a domain administrator must prestage the CNO.
- `-NoStorage` avoids auto-adding disks; add them deliberately.
- AD-detached clusters (no CNO or VCOs in AD DS): `-AdministrativeAccessPoint Dns`.

## Storage and quorum
```powershell
Get-ClusterAvailableDisk | Add-ClusterDisk
Add-ClusterSharedVolume -Name 'Cluster Disk 2'
Set-ClusterQuorum -FileShareWitness \\files01\witness$       # or -CloudWitness / -DiskWitness 'Cluster Disk 1'
```

## Add a node later
```powershell
Test-Cluster -Node hv01,hv02,hv03,hv04 -Include 'Inventory','Network','System Configuration','Storage'
Add-ClusterNode -Cluster HVCL01 -Name hv04 -NoStorage
```

## Post-creation checks
- Cluster networks: name them and set roles (management, cluster-only, live migration, storage excluded).
- Live migration networks and authentication on every node.
- Default VM paths on CSV (`Set-VMHost -VirtualMachinePath`).
- Make existing VMs highly available: `Add-ClusterVirtualMachineRole -VMName app01`.

## Verify
`Get-ClusterNode` all *Up*; `Get-ClusterQuorum` shows the witness; validation report has no failures; a test VM live migrates between all nodes.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: Install-WindowsFeature -Name Failover-Clustering -IncludeManagementTools, Test-Cluster -Node, New-Cluster -Name/-Node/-StaticAddress/-NoStorage, -AdministrativeAccessPoint values ActiveDirectoryAndDns, Dns and None, Add-ClusterNode -NoStorage, Add-ClusterVirtualMachineRole -VMName and Set-ClusterQuorum witness parameters; the Create Computer objects requirement and prestaging option. Removed as unconfirmed: identical host configuration list and workgroup wording.

Method: documentation only; no commands were run.
