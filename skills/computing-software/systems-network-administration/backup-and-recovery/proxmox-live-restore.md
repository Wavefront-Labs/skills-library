---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-live-restore
name: proxmox-live-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [live-restore, proxmox-ve, proxmox-backup-server, qmrestore, instant-recovery, rto]
level: practitioner
status: docs-checked
description: "Use Proxmox VE live restore to start a VM as soon as a restore from Proxmox Backup Server begins while data copies in the background, with its read-speed and failure caveats."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html#vzdump_restore
  - https://pve.proxmox.com/pve-docs/qmrestore.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE live restore

**Goal:** get a large VM running sooner than a full restore allows.

## How it works
Restoring a large backup can take a long time, during which the guest is unavailable. For VM backups stored on a Proxmox Backup Server, the live-restore option starts the VM as soon as the restore begins. Data is copied in the background, prioritizing chunks the VM is actively accessing.

## Use
Tick the live-restore checkbox in the GUI, or pass `--live-restore` to `qmrestore`. The option is described as "Start the VM immediately from the backup and restore in background. PBS only."
```sh
qmrestore <archive> <vmid> --storage <storage ID> --live-restore 1
```
`<archive>` is the backup, `<vmid>` the new VM ID (100 to 999999999). `--storage` sets the default storage; without it volumes are allocated on the original storage. `--force` allows overwriting an existing VM, and `--bwlimit` overrides the I/O limit in KiB/s.

## Caveats (from the manual)
- During live-restore the VM runs with limited disk read speeds, because data must be loaded from the backup server. Once loaded, data is immediately available on the destination storage, so only the first access pays the penalty. Write speeds are largely unaffected.
- If the live-restore fails for any reason, the VM is left in an undefined state: not all data may have been copied, and data written during the failed restore most likely cannot be kept.

## When it fits
The manual says it is especially useful for large VMs where only a small amount of data is needed for initial operation, such as web servers: once the OS and necessary services have started the VM is operational while the background task copies seldom-used data.

## Related
Single file restore (File Restore button in the storage GUI's Backups tab) is available for backups on a Proxmox Backup Server only.

## Checked
2026-11-07. Read in full: the Restore, Bandwidth Limit, Live-Restore and Single File Restore sections of the PVE Backup and Restore chapter (9.2.13) and the whole qmrestore(1) page. Removed because the pages do not state them: the PBS archive path example, "containers not supported" (the pages say VM backups and "PBS only" but do not mention containers), "databases painfully slow", "do not use over flaky WAN", "many VMs saturate PBS", the claim that writes go to the target storage, and the invented Verify step.
Method: documentation only; no commands were run.
