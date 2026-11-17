---
id: computing-software.it-support-helpdesk.desktop-support.fslogix-profile-container-support
name: fslogix-profile-container-support
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, fslogix, profile-container, vhdx, avd, rds, temporary-profile]
level: practitioner
status: gated
description: "Support FSLogix profile containers on AVD/RDS: core registry settings, share permissions, locked or full VHDX, temporary profiles, logs and safe compaction."
sources:
  - "https://learn.microsoft.com/en-us/fslogix/overview-what-is-fslogix"
  - "https://learn.microsoft.com/en-us/fslogix/reference-configuration-settings"
  - "https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions"
  - "https://learn.microsoft.com/en-us/fslogix/troubleshooting-events-logs-diagnostics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fslogix-profile-container-support

## How it works
At sign-in FSLogix attaches the user's VHDX from an SMB share and redirects the profile
into it, so the session host never keeps a local profile.

## Core settings (`HKLM\SOFTWARE\FSLogix\Profiles`)
| Value | Typical |
|---|---|
| `Enabled` | 1 |
| `VHDLocations` | `\\storage\profiles` (multi-string; list several for resilience only with care) |
| `VolumeType` | VHDX |
| `SizeInMBs` | 30000 default; raise per estate |
| `IsDynamic` | 1 (grows as used) |
| `DeleteLocalProfileWhenVHDShouldApply` | 1, so an old local profile does not block the container |
| `FlipFlopProfileDirectoryName` | 1 for readable `username_SID` folders |

## Share permissions
Users: Modify on "this folder only"; CREATOR OWNER: Modify on "subfolders and files only";
admins: Full control. Users must not be able to list or open others' folders.

## Common faults
| Symptom | Cause |
|---|---|
| Temporary profile / "profile could not be attached" | Share unreachable, wrong permissions, or VHDX locked |
| VHDX locked | Stale session on another host still holds it; sign that session out (concurrent access needs ProfileType setup) |
| Out of space errors in apps | Container at `SizeInMBs`; expand the disk or clean up |
| Slow logon | Storage latency, AV scanning the VHDX (exclude per Microsoft guidance) |

## Logs and tools
- `%ProgramData%\FSLogix\Logs\Profile\` text logs per day; event log
  Microsoft-FSLogix-Apps/Operational.
- `frxtray.exe` in the FSLogix program folder shows live container status in the session.
- Exclude admins with the local group "FSLogix Profile Exclude List".

## Compaction
Recent FSLogix versions compact the VHDX automatically at sign-out (`VHDCompactDisk`).
Never mount or edit a container while the user is signed in.

## Verify
User signs in with no temp profile, `frxtray` shows the container attached from the
expected path, and the day's log shows the attach and detach without errors.

## Checked

- Date: 2026-11-02.
- Confirmed against: registry value names Enabled, VHDLocations, VolumeType, SizeInMBs (default 30000), IsDynamic, DeleteLocalProfileWhenVHDShouldApply, FlipFlopProfileDirectoryName, VHDCompactDisk (default enabled); share ACLs (Domain Users Modify this folder only, CREATOR OWNER Modify subfolders and files only, admins Full Control); logs under ProgramData\FSLogix\Logs\Profile (Microsoft Learn FSLogix pages).
- Not confirmed: frxtray.exe and the FSLogix Profile Exclude List group name (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
