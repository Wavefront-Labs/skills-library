---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-vzdump-modes-and-backup-jobs
name: proxmox-vzdump-modes-and-backup-jobs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [vzdump-mode, snapshot-mode, vzdump, proxmox-backup, backup-jobs, fleecing, proxmox-ve]
level: practitioner
status: docs-checked
description: "Back up Proxmox VE guests with vzdump: snapshot, suspend and stop modes for VMs and containers, scheduled backup jobs, retention, fleecing, bandwidth limits and protected backups."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html
  - https://pve.proxmox.com/pve-docs/vzdump.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vzdump modes and backup jobs

**Goal:** consistent backups of Proxmox VMs and containers with minimal guest impact.

## Modes
| Mode | VMs | Containers |
|---|---|---|
| `snapshot` | Live backup: data blocks are copied while the VM runs. If the guest agent is enabled (`agent: 1`) and running, vzdump calls `guest-fsfreeze-freeze` and `guest-fsfreeze-thaw` for consistency. Small inconsistency risk, lowest downtime | Uses the storage's snapshot facilities; all backed-up volumes must be on snapshot-capable storage (`backup=no` on a mount point excludes a volume from the requirement) |
| `suspend` | Kept for compatibility: suspends the VM, then runs snapshot mode. Longer downtime and no sure consistency gain, so snapshot is recommended | rsync to a temporary location (`--tmpdir`), then suspend and rsync changed files, then resume: minimal downtime |
| `stop` | Orderly shutdown, then a background QEMU process backs up the data and the VM returns to operation once the backup has started: highest consistency, short downtime | Same idea: consistent, with downtime |

```bash
vzdump 101 --mode snapshot --storage pbs-main --notes-template '{{guestname}} nightly'
vzdump 200 --mode stop --storage local --compress zstd
```

## Scheduled backup jobs
Datacenter > Backup (or the `/cluster/backup` API) writes job entries to `/etc/pve/jobs.cfg`, run by the `pvescheduler` daemon. A job selects all nodes or one node, guests, a schedule (systemd calendar event format; see the calendar events section of the docs), storage, mode, and retention, e.g. `--prune-backups keep-last=3,keep-daily=7,keep-weekly=4,keep-monthly=6`. It is often more sensible to set `prune-backups` on the storage than per job.

## Performance and impact
- **Fleecing** (VMs): old data that the guest is about to overwrite is cached in a fleecing image instead of being sent straight to the backup target. This can help guest I/O and prevent hangs, at the cost of more storage. Enable with `vzdump 123 --fleecing enabled=1,storage=local-lvm`, or in the job's Advanced tab. Use fast local, thin-provisioned storage with discard support.
- `bwlimit` limits I/O bandwidth (default 0, no limit); `ionice` applies when the BFQ I/O scheduler is used. Global defaults live in `/etc/vzdump.conf`.

## Protected backups and notes
Mark a backup **protected** to stop its removal from the UI, CLI or API; pruning ignores protected backups and they do not count toward retention. This is enforced by Proxmox VE, not the file system. The storage option `max-protected-backups` limits how many protected backups a guest may have on a storage.

## Gotchas
- Container `snapshot` mode needs every volume on storage that supports snapshots; otherwise use `suspend` or `stop`.

## Verify
Task logs show successful jobs for all guests, and a periodic test restore boots.

## Checked
2026-10-28. Confirmed against the Proxmox VE vzdump chapter (modes, fleecing, jobs.cfg, pvescheduler, prune-backups keys, bwlimit, ionice, vzdump.conf, protected backups, max-protected-backups). Removed because the page does not state them: the PVE 8.2 version gate for fleecing, the example `sun 01:00`, the list of container snapshot storages (ZFS, LVM-thin, Ceph), the PBS dirty-bitmap claims and the KiB/s unit for backup bwlimit.
Method: documentation only; no commands were run.
