---
id: computing-software.systems-network-administration.virtualisation.hyper-v-shared-nothing-live-migration
name: hyper-v-shared-nothing-live-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-live-migration, shared-nothing-live-migration, move-vm, enable-vmmigration, migration-networks, hyper-v, windows-server]
level: practitioner
status: docs-checked
description: "Move running VMs between standalone Hyper-V hosts with shared-nothing live migration: enable migration, authentication choice, networks, Move-VM with storage, and common errors."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/move-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V shared-nothing live migration

**Goal:** move a running VM and its disks from one non-clustered Hyper-V host to another
with no downtime.

## Enable on both hosts
```powershell
Enable-VMMigration
Set-VMHost -VirtualMachineMigrationAuthenticationType Kerberos `
           -VirtualMachineMigrationPerformanceOption SMB
Add-VMMigrationNetwork 10.70.0.0/24          # restrict to the migration network
Set-VMHost -UseAnyNetworkForMigration $false
```
- **Kerberos** needs constrained delegation configured in AD (by a Domain Admin) on each host's computer account:
  `cifs` to move storage and `Microsoft Virtual System Migration Service` to move VMs. It lets you start migrations
  without signing in to the source server. **CredSSP** (the default) needs no delegation but you must sign in to
  the source server, and again to the other server when moving the VM back.
- Performance option: TCPIP, Compression (the default; compresses memory over TCP/IP) or SMB (highest
  throughput).
- The default number of simultaneous live migrations is 2.

## Move
```powershell
Move-VM -Name app01 -ComputerName hv01 -DestinationHost hv02 `
  -IncludeStorage -DestinationStoragePath '<DATA_VOL>\Hyper-V\app01'
# Per-disk placement:
Move-VM -Name app01 -DestinationHost hv02 -IncludeStorage -VirtualMachinePath '<DATA_VOL>\VMs\app01' `
  -VHDs @(@{SourceFilePath='<DATA_VOL>\VMs\app01\os.vhdx'; DestinationFilePath='<VHD_VOL>\VHD\app01-os.vhdx'})
Compare-VM -Name app01 -DestinationHost hv02 -IncludeStorage   # pre-check report
```

## Requirements
- The same processor manufacturer: running VMs cannot move between Intel and AMD hosts even with processor
  compatibility. Enable **processor compatibility** on the VM (powered off) if CPU generations differ.
- The destination must support the VM's configuration version (use an equal or newer Hyper-V version).
- You need Hyper-V Administrators or Administrators membership on both hosts.

## Common errors
| Error | Cause |
|---|---|
| "Failed to establish a connection with host ... No credentials are available in the security package 0x8009030E" | CredSSP and you are not signed in to the source server |
| Processor feature mismatch | enable compatibility mode on the VM |
| Kerberos failure | constrained delegation missing for `cifs` or `Microsoft Virtual System Migration Service` |

## Verify
`Get-VM app01 -ComputerName hv02` shows Running; `Get-VMHardDiskDrive` shows disks at the destination paths; the
source folder no longer holds the VM files.

## Checked

Date checked: 2026-10-27. Documentation: "Set up hosts for live migration without Failover Clustering" (windowsserverdocs main branch), Move-VM, Compare-VM and Set-VMHost reference (Windows Server 2025 docset).
Confirmed: Enable-VMMigration and Add-VMMigrationNetwork syntax (-Subnet, -Priority); authentication types and CredSSP default; performance options and Compression default; default of 2 simultaneous migrations; Move-VM parameters including -VHDs with SourceFilePath and DestinationFilePath; delegated services; Intel to AMD limit; the 0x8009030E message.

Method: documentation only; no commands were run.
