---
id: computing-software.systems-network-administration.proxmox-ve.vzdump-modes-retention-and-jobs
name: vzdump-modes-retention-and-jobs
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [vzdump, backup-modes, prune-backups, backup-jobs]
level: practitioner
status: docs-checked
description: "Pick vzdump backup modes for VMs and containers, set prune-backups retention, and schedule backup jobs on Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/vzdump.1.html
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VM modes (option `mode`):

- `snapshot` has the lowest downtime at a small inconsistency risk. It uses Proxmox VE live backup, which works on any storage type. If the guest agent is enabled (`agent: 1`) and running, it calls guest-fsfreeze-freeze and guest-fsfreeze-thaw to improve consistency.
- `stop` gives the highest consistency with a short downtime: an orderly shutdown, then a background QEMU process backs up the data while the VM returns to operation.
- `suspend` exists for compatibility, and `snapshot` is recommended instead.

Container modes: `stop` stops the container for the duration. `suspend` rsyncs data to a temporary location (`--tmpdir`) before suspending. `snapshot` uses the storage's snapshots, so all backed up volumes must be on snapshot capable storage. Set `backup=no` on a mount point to skip it.

Retention uses `prune-backups`, a comma-separated list of `keep-last`, `keep-hourly`, `keep-daily`, `keep-weekly`, `keep-monthly`, `keep-yearly` (or `keep-all`, which allows no others). They are processed in that order and each option covers only backups not yet covered by an earlier one.

```
vzdump 777 --prune-backups keep-last=3,keep-daily=13,keep-yearly=9
```

It is often more sensible to set this on the storage.

Scheduled jobs are stored in `/etc/pve/jobs.cfg` and run by the `pvescheduler` daemon, for all nodes or one node, using systemd calendar event style schedules. Enable `repeat-missed` to run jobs missed while the host was offline. `bwlimit` limits IO bandwidth, and `zstd` sets compressor threads.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/vzdump.1.html, https://pve.proxmox.com/pve-docs/chapter-vzdump.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
