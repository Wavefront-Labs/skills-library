---
id: computing-software.systems-network-administration.windows-server.smb-bandwidth-limits
name: smb-bandwidth-limits
category: computing-software
field: systems-network-administration
product: windows-server
tags: [scale-out-file-server, smb-bandwidth-limit, live-migration, smb-direct, hyper-v-over-smb]
level: practitioner
status: docs-checked
description: "Cap SMB traffic categories (Default, VirtualMachine, LiveMigration) with Set-SmbBandwidthLimit so live migration over SMB cannot starve storage traffic."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbbandwidthlimit
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/configure-live-migration-smb-bandwidth
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SMB bandwidth limits

When Hyper-V hosts use SMB for both VM storage (to an SOFS or S2D CSV) and live migration over the same RDMA NICs, a
burst of live migrations can saturate links and stall VM I/O. SMB Bandwidth Limit caps each category.

## Install and set
```powershell
Install-WindowsFeature FS-SMBBW
Set-SmbBandwidthLimit -Category LiveMigration -BytesPerSecond 750MB
Get-SmbBandwidthLimit
```
Categories:
- **Default**: all other SMB traffic.
- **VirtualMachine**: Hyper-V accessing VHDX over SMB.
- **LiveMigration**: live migration using SMB transport.
- **StorageReplication**: Storage Replica traffic.

A limit caps the bytes per second the SMB server sends for that category. Installing the feature creates a performance counter set with one instance per category.

## Sizing
In a failover cluster the limit can be set cluster-wide as a percentage of total bandwidth using the `SetSMBBandwidthLimitFactor` cluster parameter (factor = limit / total bandwidth x 10000; default 2500 = 25%). After FS-SMBBW is installed on a cluster node, SMB bandwidth is limited to that default 25% of the node's total bandwidth, which needs the 2022-09 cumulative update or later on Windows Server 2022.

## Prerequisite: live migration over SMB
```powershell
Set-VMHost -VirtualMachineMigrationPerformanceOption SMB
```
Without this, the LiveMigration category does nothing.

## Alternatives / complements
Network ATC can also manage SMB bandwidth limits; see the Microsoft live migration bandwidth page.

## Remove
```powershell
Remove-SmbBandwidthLimit -Category LiveMigration
```

## Verify
- [ ] The SMB performance counters (same counters as `SMB Client Shares`, one instance per category) during a migration show throughput at
  or below the limit, and VM storage latency stays flat.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Set-SmbBandwidthLimit reference: categories Default, VirtualMachine, LiveMigration and StorageReplication (StorageReplication was missing); BytesPerSecond is the maximum the server can send; FS-SMBBW installs the feature and adds a counter set with one instance per category.
- configure-live-migration-smb-bandwidth page: `Set-VMHost -VirtualMachineMigrationPerformanceOption SMB`, default cluster limit factor 2500 (25%), formula limit/total x 10000, 2022-09 update prerequisite.
- Removed unconfirmed details: RDMA applicability, the 2x25 GbE sizing example, MaximumVirtualMachineMigrations advice, DCB/QoS cmdlet claim and the `SMB Direct Connection` counter name.

Method: documentation only; no commands were run.
