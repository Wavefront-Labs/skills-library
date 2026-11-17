---
id: computing-software.systems-network-administration.windows-server.hyper-v-over-smb-share-delegation
name: hyper-v-over-smb-share-delegation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, sofs, hyper-v-smb-delegation, hyper-v-over-smb, constrained-delegation, smb-share-permissions]
level: advanced
status: docs-checked
description: "Set up Hyper-V over SMB: SOFS share permissions for Hyper-V host computer accounts, constrained delegation for remote management, and placing VMs on UNC paths."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/jj134187(v=ws.11)
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V over SMB share and delegation setup

VMs can live on a continuously available SMB 3 share (Scale-Out File Server or clustered file server). Hosts access
the share as their **computer accounts**; admins managing remotely need delegation.

## Share permissions
Grant Full Control (share and NTFS) to:
- Each Hyper-V host computer account (`AD\HV01$`, or a group `AD\GG-HyperV-Hosts` containing them).
- The Hyper-V cluster name object if clustered (`AD\HVCLUSTER$`).
- Hyper-V administrators (user accounts) and SYSTEM.
```powershell
New-SmbShare -Name VMs01 -Path '<CSV_PATH>\Shares\VMs01' -FullAccess 'AD\GG-HyperV-Hosts','AD\HVCLUSTER$','AD\GG-HyperV-Admins' `
  -ContinuouslyAvailable $true
Set-SmbPathAcl -Name VMs01       # copy share ACL to the folder NTFS ACL
```

## Remote management (the double hop)
Creating a VM on `\\SOFS01\VMs01` from your workstation via Hyper-V Manager makes the host access the share with
**your** credentials: second hop. Configure Kerberos constrained delegation on each host computer object for the
SOFS (see the constrained delegation section of the Hyper-V over SMB deployment page).
Running management locally on the host (PowerShell Direct, remoting into the host) avoids the hop.

## Place VMs
```powershell
New-VM -Name APP01 -Path \\SOFS01\VMs01 -Memory 1GB -VHDPath \\SOFS01\VMs01\APP01.VHDX
```

## Verify
- [ ] VM starts from the share, survives a SOFS node failover, and remote creation works.

## Checked

2026-10-28. Confirmed against: Hyper-V over SMB deployment page (New-SmbShare -FullAccess with host computer accounts and cluster account, Set-SmbPathAcl, constrained delegation section, New-VM -Path on a UNC share) and the New-SmbShare reference (ContinuouslyAvailable). Removed (not confirmable from the cited pages): ScopeName and CachingMode values, reboot/klist note, SPN and live-migration service names, Set-ADComputer delegation commands, resource-based delegation, VHD size and generation flags.

Method: documentation only; no commands were run.
