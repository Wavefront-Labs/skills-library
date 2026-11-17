---
id: computing-software.systems-network-administration.virtualisation.hyper-v-live-migration-performance-options
name: hyper-v-live-migration-performance-options
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, smb-direct, migration-performance-option, live-migration, rdma, compression, smb-bandwidth-limit, windows-server]
level: advanced
status: docs-checked
description: "Tune Hyper-V live migration transport (TCP/IP, compression, SMB with SMB Direct/RDMA), concurrency limits, and SMB bandwidth caps so migrations are fast without starving storage."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbbandwidthlimit
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/configure-live-migration-smb-bandwidth
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Live migration performance options

**Goal:** migrate VMs in seconds during drains and patching without saturating the storage network.

## Transport options
```powershell
Set-VMHost -VirtualMachineMigrationPerformanceOption Compression   # compresses data to speed up migration on constrained networks
Set-VMHost -VirtualMachineMigrationPerformanceOption SMB           # SMB transport: highest throughput, uses SMB Direct on RDMA adapters
Set-VMHost -VirtualMachineMigrationPerformanceOption TCPIP         # standard live migration
```
Microsoft's Azure Local guidance: use SMB when at least 5 Gbps is available for live migration and the adapters are RDMA-capable, otherwise use Compression.

## Concurrency and networks
```powershell
Set-VMHost -MaximumVirtualMachineMigrations 4 -MaximumStorageMigrations 2
Add-VMMigrationNetwork 10.10.50.0/24
Set-VMHost -UseAnyNetworkForMigration $false
```
In a cluster, the maximum parallel migrations come from the cluster property `(Get-Cluster).MaximumParallelMigrations`, which takes precedence over the host setting. Exclude networks from live migration through the Virtual Machine resource type's `MigrationExcludeNetworks` parameter (see the cluster live migration SMB bandwidth page).

## Protect storage traffic when using SMB
With S2D or SOFS, live migration over SMB competes with storage traffic:
```powershell
Install-WindowsFeature FS-SMBBW
Set-SmbBandwidthLimit -Category LiveMigration -BytesPerSecond 750MB
```
Microsoft's Azure Local guidance: cap live migration so it cannot consume the whole RDMA traffic class; the cmdlet takes bytes per second.

## Check RDMA
```powershell
Get-NetAdapterRdma | Where-Object Enabled
Get-SmbClientNetworkInterface | Where-Object RdmaCapable
```
During a migration, `Get-SmbMultichannelConnection` shows the connections in use.

## Gotchas
- With Kerberos authentication outside a cluster, constrained delegation must list `Microsoft Virtual System Migration Service` (to move VMs) and `cifs` (to move storage).
- Windows Server 2025 enables Credential Guard by default on domain-joined servers, which affects CredSSP-based live migration; see the setup page.

## Verify
Time a migration of a busy VM before and after the change and compare.

## Checked

Checked 2026-10-26 against the Windows Server 2025 `Set-VMHost` reference (accepted values TCPIP, Compression, SMB; `-MaximumVirtualMachineMigrations`, `-MaximumStorageMigrations`, `-UseAnyNetworkForMigration`), the Azure Local host network requirements page (5 Gbps threshold, 750MB SMB bandwidth limit example), and MicrosoftDocs/windowsserverdocs (cluster live migration SMB bandwidth, live migration setup with constrained delegation). Corrected: Compression is not documented as the default, and the "10 Gbps / 25 Gbps" rule of thumb is replaced by Microsoft's 5 Gbps guidance. Removed as undocumented: the perf counter name and the claim that SMB without RDMA loads the CPU like TCP. `Add-VMMigrationNetwork` is a documented companion of `Set-VMHost -UseAnyNetworkForMigration`.

Method: documentation only; no commands were run.
