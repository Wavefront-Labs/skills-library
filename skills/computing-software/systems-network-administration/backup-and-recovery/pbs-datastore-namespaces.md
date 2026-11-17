---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-datastore-namespaces
name: pbs-datastore-namespaces
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-namespace, proxmox-backup-server, namespaces, multi-cluster-backup, pbs, proxmox]
level: practitioner
status: docs-checked
description: "Use Proxmox Backup Server datastore namespaces to separate clusters, sites or tenants in one deduplicated datastore, with per-namespace ACLs, prune, sync and PVE mapping."
sources:
  - https://pbs.proxmox.com/docs/storage.html#backup-namespaces
  - https://pve.proxmox.com/wiki/Storage:_Proxmox_Backup_Server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS datastore namespaces

**Goal:** several PVE clusters or tenants share one datastore (and its dedup) without VMID collisions or seeing each other's backups.

## Concept
Namespaces are a hierarchy inside a datastore (`max-depth` takes 0 to 7 levels below a namespace): `site-a/cluster1`, `site-b/cluster1`. Backup groups (`vm/100`) are unique per namespace, so two clusters each with VM 100 do not collide.

## Create and use
```sh
proxmox-backup-client namespace create site-a --repository root@pam@pbs1:store1
proxmox-backup-client namespace create site-a/cluster1 --repository root@pam@pbs1:store1
proxmox-backup-client namespace list --repository root@pam@pbs1:store1
```
In PVE, the namespace is set on the Proxmox Backup Server storage entry (see the Proxmox VE storage documentation for the option).

## Permissions
ACL paths include the namespace: `/datastore/store1/site-a`. Grant each cluster's token DatastoreBackup on its own namespace only:
```sh
proxmox-backup-manager acl update /datastore/store1/site-a DatastoreBackup --auth-id 'pve-a@pbs!cluster1'
```

## Jobs per namespace
- Prune jobs and verify jobs take `--ns` and `--max-depth`.
- Sync jobs map `--remote-ns` to a local `--ns` (e.g. pull remote root into local `offsite/site-a`).
- Tape backup jobs can select a namespace.

## Gotchas
- Garbage collection runs per datastore (`proxmox-backup-manager garbage-collection start <store>`).

## Verify
Each PVE cluster lists only its own backups in the storage view; `proxmox-backup-client snapshot list --ns site-a/cluster1` shows the expected groups.

## Checked

2026-10-28

Confirmed: PBS maintenance docs and command syntax: prune and sync --ns and --max-depth, remote-ns mapping, acl update syntax, tape namespaces, garbage-collection start per store.

Removed or corrected: cross-namespace dedup claim, pvesm namespace command, PBS 2.2 gate, 8-level claim, root-access and move gotchas.

Method: documentation only; no commands were run.
