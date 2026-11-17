---
id: computing-software.systems-network-administration.windows-server.iscsi-target-server-setup
name: iscsi-target-server-setup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iscsi, iscsi-target, new-iscsivirtualdisk, new-iscsiservertarget, fs-iscsitarget-server, initiator-ids, san]
level: practitioner
status: docs-checked
description: "Build an iSCSI Target Server: install the role, create iSCSI virtual disks, targets with initiator ACLs, map LUNs and dedicate storage NICs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-target-server
  - https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-target-server-limits
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/new-iscsivirtualdisk
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/new-iscsiservertarget
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/set-iscsitargetserversetting
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/checkpoint-iscsivirtualdisk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iSCSI Target Server: virtual disks and targets

## Install
```powershell
Get-WindowsFeature *iSCSI*          # confirm the exact feature name on your server
Install-WindowsFeature <ISCSI_TARGET_FEATURE_NAME> -IncludeManagementTools
```
The Server Core role table in Microsoft's docs lists the role service as iSCSI Target Server (name `iSCSITarget-Server`); confirm the name with the first command.

## Create a LUN and a target
```powershell
New-IscsiVirtualDisk -Path '<vol>:\iSCSI\SQL01-Data.vhdx' -SizeBytes 500GB -UseFixed
New-IscsiServerTarget -TargetName SQL01 -InitiatorIds 'IQN:<INITIATOR_IQN>'
Add-IscsiVirtualDiskTargetMapping -TargetName SQL01 -Path '<vol>:\iSCSI\SQL01-Data.vhdx' -Lun 0
```
- `-InitiatorIds` accepts `IQN:`, `IPAddress:`, `IPv6Address:`, `DNSName:` or `MACAddress:` prefixes. Use IQNs.
  For a cluster list every node's IQN on the same target (shared LUN).
- `-UseFixed` creates a fixed VHDX; without it a dynamic VHDX is created (dynamic is the default parameter set). The limits page notes dynamic VHDs are supported but Unmap is not, and that .vhdx needs Windows Server 2012 R2 or later.
- Get a client's IQN on the initiator: `(Get-InitiatorPort).NodeAddress` (Storage module).

## Network
- Put iSCSI on dedicated NICs or VLANs.
- Enable or disable the target portal per IP address so only storage NICs serve iSCSI:
```powershell
Get-IscsiTargetServerSetting
Set-IscsiTargetServerSetting -IP 10.10.10.5 -Enable $true
Set-IscsiTargetServerSetting -IP 192.168.1.5 -Enable $false
```
- `-Port` on `Set-IscsiTargetServerSetting` changes the portal's TCP port for an IP; allow that port in the firewall.

## Operations
- Extend: `Resize-IscsiVirtualDisk -Path ... -SizeBytes 800GB`, then extend the partition on the initiator.
- Snapshots: `Checkpoint-IscsiVirtualDisk -OriginalPath <vhdx>` creates a virtual disk snapshot (limit of 512 snapshots per independent iSCSI application volume).
- For high availability, run iSCSI Target Server in a failover cluster (shared storage required).

## Verify
- [ ] `Get-IscsiServerTarget | Format-List *` shows the target, its initiator ids and LUN mappings.
- [ ] The target shows a connected initiator once it logs in.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- iscsitarget cmdlet references: New-IscsiVirtualDisk (-SizeBytes, -UseFixed, dynamic default), New-IscsiServerTarget -InitiatorIds (DNSName, IPAddress, IPv6Address, IQN, MACAddress), Add-IscsiVirtualDiskTargetMapping -Lun, Set-IscsiTargetServerSetting -IP -Port -Enable, Resize-IscsiVirtualDisk -Path -SizeBytes, Checkpoint-IscsiVirtualDisk -OriginalPath.
- iSCSI Target Server overview and limits pages: clustering for high availability, 512 snapshots per independent iSCSI application volume, .vhdx on Windows Server 2012 R2 and newer, dynamic VHD supported without Unmap.
- Removed unconfirmed details: the FS-iSCSITarget-Server feature name (now looked up with Get-WindowsFeature), the jumbo-frame registry command, DNS and gateway advice, the default TCP port number, and the VSS description of checkpoints.

Method: documentation only; no commands were run.
