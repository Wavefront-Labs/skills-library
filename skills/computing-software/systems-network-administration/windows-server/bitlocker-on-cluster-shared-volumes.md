---
id: computing-software.systems-network-administration.windows-server.bitlocker-on-cluster-shared-volumes
name: bitlocker-on-cluster-shared-volumes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, bitlocker, bitlocker-csv, cluster-shared-volumes, failover-clustering, cno-protector, adaccountorgroup-protector]
level: advanced
status: docs-checked
description: "Encrypt Cluster Shared Volumes and clustered disks with BitLocker: maintenance mode, recovery password plus CNO protector, re-adding to CSV and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/bitlocker-on-csv-in-ws-2022
  - https://learn.microsoft.com/en-us/powershell/module/bitlocker/add-bitlockerkeyprotector
  - https://learn.microsoft.com/en-us/powershell/module/bitlocker/enable-bitlocker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BitLocker on Cluster Shared Volumes

Clustered volumes are managed with PowerShell or `manage-bde` (CSVs are mount points and do not appear in the BitLocker
Control Panel item). Failover Clustering needs the Active Directory-based protector (`ADAccountOrGroup`, bound here to
the Cluster Name Object) so every node can unlock the volume. Windows Server 2022 and later can also generate and keep
its own key protector in the cluster database, which works for Active Directory-less (workgroup) clusters.

## Prerequisites
- BitLocker feature on every node, then restart:
  `Install-WindowsFeature -Name BitLocker -IncludeAllSubFeature -IncludeManagementTools`.
- With the AD protector, a reachable domain controller is needed at unlock: an unresponsive or unavailable DC slows or
  fails volume unlock and the online process after failover.
- With the cluster-managed key (2022+), BitLocker-protect the system volume on every node too; the cluster database
  that holds the key is stored there. Failover Clustering logs a warning event if the system drive is not encrypted.

## Encrypt a CSV (AD protector)
```powershell
# 1. Put the CSV into maintenance mode (this stops the clustered roles that use it)
Get-ClusterSharedVolume 'Cluster Disk 1' | Suspend-ClusterResource
# 2. Encrypt via the CSV mount path
$mp = "$env:SystemDrive\ClusterStorage\Volume1"
Enable-BitLocker -MountPoint $mp -RecoveryPasswordProtector
# 3. Add the CNO as an AD account protector (cluster name followed by $)
Add-BitLockerKeyProtector -MountPoint $mp -ADAccountOrGroupProtector -ADAccountOrGroup 'CLUSTER01$'
# 4. Resume once encryption has finished
Get-ClusterSharedVolume 'Cluster Disk 1' | Resume-ClusterResource
```
Save the numerical recovery password in a secure place away from the computer.

## Encrypt with a cluster-managed recovery key (2022+)
After `Enable-BitLocker ... -RecoveryPasswordProtector` on the node that owns the volume, store the protector ID and
recovery password in the disk's `BitLockerProtectorInfo` parameter, formatted `<protector-id>:<recovery-password>`,
before leaving maintenance mode; the cluster then keeps the key encrypted in its database and removes the parameter:
```powershell
Get-ClusterSharedVolume 'Cluster Disk 1' | Set-ClusterParameter -Name BitLockerProtectorInfo -Value '<protector-id>:<recovery-password>' -Create
```
If the resource does not come online, check that the parameter holds the correct protector information.

## Operations
```powershell
Get-BitLockerVolume -MountPoint $mp | Select VolumeStatus,EncryptionPercentage,KeyProtector
manage-bde -status "$env:SystemDrive\ClusterStorage\Volume1"
```

## Verify
- [ ] Failover the CSV to each node: it comes online without prompting.
- [ ] Key protectors show the recovery password and the AD account protector (or the cluster-managed key).

## Checked

Confirmed 2026-10-25 against the Windows Server docs (bitlocker-on-csv-in-ws-2022, repository last commit 2026-10-23) and the Windows Server 2025 PowerShell reference for Enable-BitLocker and Add-BitLockerKeyProtector (MountPoint, RecoveryPasswordProtector, ADAccountOrGroupProtector, ADAccountOrGroup): put the resource in maintenance mode before enabling BitLocker (this stops the roles using the volume), the ADAccountOrGroup protector is required for cluster disks and the CNO is the protector account, the AD protector depends on a reachable domain controller at unlock, Windows Server 2022 adds a cluster-managed key stored in the cluster database (system volumes should also be encrypted), the recovery-key path needs the BitLockerProtectorInfo disk parameter, and the BitLocker feature install command. Removed unconfirmed claims about encryption method options, key backup to AD, CNO rename effects, S2D specifics and backup behaviour.

Method: documentation only; no commands were run.
