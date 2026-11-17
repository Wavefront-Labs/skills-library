---
id: computing-software.systems-network-administration.windows-server.fslogix-profile-containers-for-rds
name: fslogix-profile-containers-for-rds
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-desktop-services, rds, fslogix, profile-containers, vhdlocations, odfc, user-profiles, cloud-cache]
level: practitioner
status: draft
description: "Configure FSLogix profile containers for RDS session hosts: install, VHDLocations share permissions, registry or GPO settings, exclusions, and troubleshooting logs."
sources:
  - https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSLogix profile containers on RDS

FSLogix mounts each user's profile from a VHDX on a share at logon, so the profile looks
local to Windows and apps (Outlook OST, Teams, OneDrive cache work). Replaces User
Profile Disks and roaming profiles. Licensed with Microsoft 365/RDS CAL entitlements.

## Install
FSLogix Apps installer on every session host (included in Windows 11 multi-session
images; servers need the install). Keep the agent version consistent.

## Share and permissions (SMB, Azure Files, or SOFS)
| Principal | Share | NTFS |
|---|---|---|
| Users group (RDS users) | Change | Modify, this folder only |
| Creator Owner | | Modify, subfolders and files only |
| Admins | Full | Full |
Users then see only their own folder.

## Settings (registry `HKLM\SOFTWARE\FSLogix\Profiles` or ADMX GPO)
```powershell
$k='HKLM:\SOFTWARE\FSLogix\Profiles'
New-Item $k -Force | Out-Null
Set-ItemProperty $k Enabled 1 -Type DWord
Set-ItemProperty $k VHDLocations '\\fs01\fslogix$' -Type MultiString
Set-ItemProperty $k VolumeType 'VHDX' -Type String
Set-ItemProperty $k SizeInMBs 30000 -Type DWord
Set-ItemProperty $k IsDynamic 1 -Type DWord
Set-ItemProperty $k DeleteLocalProfileWhenVHDShouldApply 1 -Type DWord
Set-ItemProperty $k FlipFlopProfileDirectoryName 1 -Type DWord   # folders named user_SID
Set-ItemProperty $k PreventLoginWithFailure 1 -Type DWord
Set-ItemProperty $k PreventLoginWithTempProfile 1 -Type DWord
```
- Exclude local admins/service accounts with the local groups `FSLogix Profile Exclude List`.
- HA: Cloud Cache (`CCDLocations`) writes to two locations; plain VHDLocations with
  multiple paths is not replication.
- One container per user per host at a time; concurrent sessions need
  `ProfileType` read-write/read-only configuration.

## Troubleshoot
- Logs: `%ProgramData%\FSLogix\Logs\Profile`, event log `Microsoft-FSLogix-Apps/Operational`.
- `frx list-redirects`, `frx` CLI for container management.
- Temp profile or slow logon: share permissions, SMB latency, VHD locked by another
  host (stale session), antivirus scanning VHDX (exclude `*.vhdx` on the share and
  `%ProgramFiles%\FSLogix\Apps\frxdrv.sys` paths per guidance).

## Verify
- [ ] User logs on to two different hosts and keeps settings; the profile folder is a
  mounted VHDX (`Get-Disk` shows the virtual disk).
