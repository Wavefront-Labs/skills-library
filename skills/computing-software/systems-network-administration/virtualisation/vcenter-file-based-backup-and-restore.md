---
id: computing-software.systems-network-administration.virtualisation.vcenter-file-based-backup-and-restore
name: vcenter-file-based-backup-and-restore
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-file-based-backup, vcenter-restore, vcenter-backup, vami, sftp, vcsa, vmware, vcenter, vsphere, backup-and-recovery]
level: practitioner
status: draft
description: "Schedule vCenter file-based backups from VAMI (SFTP/NFS/SMB), set retention, and restore by deploying a fresh VCSA with the installer's Restore option."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vCenter file-based backup and restore

**Goal:** be able to rebuild vCenter (inventory, config, optionally stats) after
corruption or loss, without relying on image backups of a running database.

## Configure (VAMI `https://<vcsa>:5480` → Backup)
- **Location:** `sftp://`, `ftps://`, `https://`, `nfs://`, `smb://` target outside the
  cluster vCenter manages (a backup that lives on a datastore it manages is unreachable
  in the disaster you are planning for).
- **Schedule:** daily is typical; keep 7-14 copies. Retention counts backups, not days.
- **Encrypt** with a password and store it in the vault; without it the backup is
  useless.
- **Data:** inventory and configuration are required; Stats, Events and Tasks are
  optional and can dwarf the rest.
- Use the API for scripting: `POST /api/appliance/recovery/backup/job`.

## Image backups are not enough on their own
Image-level backups of the VCSA VM work for simple cases, but the supported recovery
path for database corruption is the file-based restore. For Enhanced Linked Mode,
back up every node on the same schedule.

## Restore
1. Mount the VCSA installer ISO on a workstation; choose **Restore**.
2. Stage 1 deploys a new appliance of the **same build** (match the backup's version
   exactly) with the original FQDN and IP; power off or disconnect the broken one first.
3. Stage 2 reads the backup location and password, restores and starts services
   (can take an hour+ on large inventories).
4. After restore: ESXi hosts reconnect on their own; check vDS configuration consistency,
   reconcile VMs moved since the backup (they appear disconnected or orphaned), and
   re-run any vLCM/vSAN health checks.

## Gotchas
- SFTP servers that restrict ciphers or need keyboard-interactive auth fail silently;
  test the location with "Backup Now" right after setup.
- Backup fails when the target path contains characters VAMI rejects; keep it simple.
- Distributed switch: if hosts changed vDS config after the backup, you may need to
  restore the vDS from its own export (`Export Configuration` on the vDS).

## Verify
VAMI → Backup shows the last job successful and recent; once a year do a full restore
into an isolated network to prove the password and process work.
