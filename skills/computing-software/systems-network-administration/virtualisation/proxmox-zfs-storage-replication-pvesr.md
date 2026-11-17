---
id: computing-software.systems-network-administration.virtualisation.proxmox-zfs-storage-replication-pvesr
name: proxmox-zfs-storage-replication-pvesr
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pvesr, storage-replication, zfs-replication, zfs-send, replication-schedule, two-node-ha, pve-ha, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Replicate guests on local ZFS between Proxmox nodes with pvesr: schedules, rate limits, using replication with HA (data loss window), and fixing broken replication jobs."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pvesr
  - https://github.com/proxmox/pve-docs/blob/master/pvesr.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS storage replication (pvesr)

**Goal:** cheap HA-like resilience without shared storage: guests on local ZFS are copied
to another node every few minutes and can start there after a failure.

## Requirements
Replication copies guest volumes to another node so the data is available without shared storage. It uses snapshots and incremental transfer, after an initial full sync; only ZFS (`zfspool`) storage is supported, and the same storage ID must exist on the target node. Replication traffic uses the migration network, which defaults to the management network; set a dedicated one with `replication: secure,network=10.1.2.0/24` in `datacenter.cfg` or via Datacenter -> Options -> Replication Settings.

## Create jobs
```sh
pvesr create-local-job 100-0 pve1 --schedule "*/5" --rate 10
pvesr disable 100-0
pvesr update 100-0 --schedule '*/00'      # once per hour
pvesr list
pvesr status
```
A job ID is the VMID plus a job number (for example `100-0`) and must be given by hand only with the CLI. The default schedule is every 15 minutes; schedules use calendar-event syntax. `--rate` is a rate limit in megabytes per second to keep storage load acceptable. The GUI panel is under Datacenter, node and guest levels.

## With HA
After a node failure the guest data is still on the replication target, but only as recent as the last successful replication, so writes since then are lost; the loss window is the schedule interval plus transfer time. Acceptable for many services, not for databases without their own replication. Replication is not a substitute for backups.

## Migration
Migrating a guest to a node it already replicates to sends only the delta since the last sync; the replication direction switches automatically (a guest on A replicated to B, migrated to B, then replicates back to A). Migrating to a node without a replica sends the whole disk, and the job then continues from the new node.

## Fixing broken jobs
- A job that fails goes into an error state: the normal schedule is suspended and the replication is retried every 30 minutes until it succeeds, then the original schedule resumes.
- Common causes in the guide: network not working, no free space on the target storage, the storage ID missing on the target node. The replication log shows the cause.
- If a node is lost and the guest is stuck on it, see the manual recovery steps in the failover skill (check quorum, move the config files, start the guest).

## Gotchas
- Not a backup: deletions and corruption replicate too.
- Only guests whose volumes are on ZFS storage can replicate; keep the same storage ID on the source and target.

## Verify
`pvesr status` shows OK with last sync within the schedule; on the target
`zfs list -t snapshot | grep __replicate_120` shows recent snapshots; a test failover in a
window boots the guest on the target.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed in the storage replication chapter: snapshot-based incremental replication after an initial full sync; zfspool as the only listed plugin; default 15-minute schedule and calendar-event syntax; `pvesr create-local-job 100-0 pve1 --schedule "*/5" --rate 10`, `pvesr disable`, `pvesr update ... --schedule '*/00'`; rate limit in MB/s; job ID format; error state with 30-minute retries; the three listed common causes; delta-only migration and automatic direction switch; replication network settings. Removed as unconfirmed: the `pvesr run` command, the "destroy the stale target volume" repair, the `__replicate_` snapshot-name grep and the HA recovery description (the replication chapter does not cover HA).

Method: documentation only; no commands were run.
