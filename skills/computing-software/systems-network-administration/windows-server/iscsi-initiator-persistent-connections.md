---
id: computing-software.systems-network-administration.windows-server.iscsi-initiator-persistent-connections
name: iscsi-initiator-persistent-connections
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iscsi, iscsi-initiator, connect-iscsitarget, new-iscsitargetportal, ispersistent, msiscsi, storage-network]
level: practitioner
status: docs-checked
description: "Connect Windows iSCSI initiators with persistent sessions: start MSiSCSI, add portals, connect per path with source IPs, bring disks online and survive reboots."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/connect-iscsitarget
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/new-iscsitargetportal
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/unregister-iscsisession
  - https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-target-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iSCSI initiator with persistent sessions

## Start the service
```powershell
Set-Service MSiSCSI -StartupType Automatic
Start-Service MSiSCSI
(Get-InitiatorPort).NodeAddress     # give this IQN to the storage admin
```

## Discover and connect
```powershell
New-IscsiTargetPortal -TargetPortalAddress 10.10.10.5 -InitiatorPortalAddress 10.10.10.21
Get-IscsiTarget
Connect-IscsiTarget -NodeAddress 'iqn.1991-05.com.microsoft:san01-sql01-target' `
  -TargetPortalAddress 10.10.10.5 -InitiatorPortalAddress 10.10.10.21 `
  -IsPersistent $true -IsMultipathEnabled $true
```
- `-IsPersistent $true` makes the connection persistent so it is restored after a restart; without it the session is not re-established.
- Specify `-InitiatorPortalAddress` so traffic uses the storage NIC, not the default route.
- Repeat per path (second NIC to second portal) for MPIO.

## Bring the disk online
```powershell
Get-Disk | ? BusType -eq iSCSI
Set-Disk -Number 3 -IsOffline $false; Initialize-Disk 3 -PartitionStyle GPT
```
For services that depend on the LUN (SQL, file shares), make sure they start only after the iSCSI volume is available (the iSCSI initiator's Volumes and Devices tab handles volume binding; `iscsicli` is not covered in the current Microsoft Learn reference).

## Disconnect cleanly
```powershell
Get-IscsiSession | Unregister-IscsiSession     # drop persistence (removes the persistent login)
Disconnect-IscsiTarget -NodeAddress <iqn> -Confirm:$false
```
Take volumes offline first to avoid data loss.

## Verify
- [ ] `Get-IscsiSession | Format-List *` shows IsPersistent and IsConnected True and the expected portal addresses.
- [ ] Reboot test: disk online and services started.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Connect-IscsiTarget: -NodeAddress, -TargetPortalAddress, -InitiatorPortalAddress, -IsPersistent, -IsMultipathEnabled; New-IscsiTargetPortal -TargetPortalAddress -InitiatorPortalAddress; Register-/Unregister-IscsiSession and Disconnect-IscsiTarget reference pages; Get-InitiatorPort exists in the Storage module.
- Removed unconfirmed details: the iscsicpl "favourite targets" wording, `iscsicli BindPersistentVolumes` (no reference page), and the exact session property list.

Method: documentation only; no commands were run.
