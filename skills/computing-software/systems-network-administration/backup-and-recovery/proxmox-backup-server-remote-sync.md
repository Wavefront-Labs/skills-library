---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-backup-server-remote-sync
name: proxmox-backup-server-remote-sync
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-sync-job, pbs-remote, proxmox-backup-server, offsite-backup, pull-sync, ransomware-resilience, proxmox-backup]
level: advanced
status: docs-checked
description: "Replicate PBS datastores off-site with remotes and sync jobs: pull vs push, least-privilege sync users, namespace and group filters, remove-vanished and schedules."
sources:
  - https://pbs.proxmox.com/docs/managing-remotes.html
  - https://pbs.proxmox.com/docs/user-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS remote sync jobs

**Goal:** a second, independent copy of backups at another site, protected from compromise of the primary.

## Pull model (preferred)
The **off-site** PBS pulls from the primary. The primary holds no credentials for the off-site server, so an attacker on the primary cannot delete the off-site copy.

## Set up on the off-site PBS
1. On the primary, create a read-only user/token for syncing (e.g. `sync@pbs` with `DatastoreReader` on the source datastore or namespace).
2. On the off-site PBS, add the remote:
```bash
proxmox-backup-manager remote create primary --host pbs1.example --auth-id 'sync@pbs!offsite' \
  --password '<token secret>' --fingerprint '<sha256 fingerprint of pbs1 certificate>'
```
3. Create the sync job:
```bash
proxmox-backup-manager sync-job create pull-primary --store offsite1 --remote primary \
  --remote-store store1 --schedule 'daily 05:00' --remove-vanished false
```
- `remove-vanished false` keeps snapshots on the target even after pruning on the source; set the target's own prune policy (often longer retention).
- `ns`/`remote-ns`/`max-depth` sync specific namespaces; `group-filter` limits to certain VMs or types.
- Rate limits (`rate-in`, `burst-in`) protect WAN links.

## Push model
Newer PBS releases also support push sync jobs from the primary to a remote. Use only if network rules prevent pull; it means the primary holds credentials that can write to the target, so restrict them (no prune/delete rights).

## Hardening the target
Separate authentication realm, no shared admins with the primary, firewall allowing only outbound pulls, verify jobs on the target datastore.

## Verify
Sync task logs succeed daily, target snapshot lists include the latest primary backups, and a restore from the off-site PBS works.

## Checked

2026-10-28

Confirmed: PBS managing-remotes docs and command syntax: remote create, sync-job create, DatastoreReader role, remove-vanished, ns/max-depth, group-filter, rate limits (burst-in), push sync direction.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
