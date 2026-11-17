---
id: computing-software.systems-network-administration.backup-and-recovery.endpoint-and-laptop-backup
name: endpoint-and-laptop-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [endpoint-backup, laptop-backup, onedrive-known-folder-move, veeam-agent, remote-workers, byod]
level: practitioner
status: draft
description: "Protect laptops and endpoints: decide between sync (OneDrive KFM) and true backup agents, policy for remote users, encryption, retention, and restoring a lost device."
sources:
  - https://learn.microsoft.com/en-us/sharepoint/redirect-known-folders
  - https://helpcenter.veeam.com/docs/backup/agents/agent_policy.html
  - https://www.cisecurity.org/controls/data-recovery
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endpoint and laptop backup

## Decide what you need
| Approach | Covers | Misses |
|---|---|---|
| Sync to cloud (OneDrive Known Folder Move, Google Drive) | Desktop/Documents/Pictures, versioning, ransomware rollback (Files Restore 30 d) | Files outside known folders, local apps, PST files, long retention |
| Endpoint backup agent (Veeam Agent, Druva, Code42-style) | Selected folders or full image, long retention, admin restore | Cost, bandwidth, agent management |
| Reimage + sync | Fast replacement with Autopilot | Anything stored locally outside sync |

Most organisations: KFM for everyone + agent for roles with local data (engineering, finance, executives) + Microsoft 365 backup for the cloud copy.

## Policy
- Users store work in synced/managed locations; local-only storage is unsupported (say so in the AUP).
- Agents: file-level backup of user profile minus caches; image backup only where rebuild is slow.
- Schedule on network connect / every few hours, throttle on metered connections, back up over internet to cloud or a gateway (Veeam Cloud Connect, vendor cloud).
- Encrypt backups with organisation keys; BitLocker on the device itself.
- Retention 30-90 days versions; leavers' data retained per records schedule.

## Deploy with Intune
- KFM via OneDrive policy (`KFMSilentOptIn` with tenant ID) and "Prevent users from moving folders back".
- Agent via Win32 app with config file; Veeam Agent can be managed by B&R protection groups.

## Restore a lost laptop
New device via Autopilot -> sign in -> OneDrive restores known folders -> restore agent backup to the new device for the rest.

## Verify
Report of devices with no backup in 7 days; quarterly test restore of a user's folder.
