---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-backup-fleecing
name: proxmox-backup-fleecing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-fleecing, proxmox-ve, vzdump, proxmox-backup-server, backup-performance, guest-io-impact]
level: advanced
status: docs-checked
description: "Enable backup fleecing in Proxmox VE so VM writes during a backup go to a fleecing image instead of waiting on the backup target; pick storage and know the space cost."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html#_vm_backup_fleecing
  - https://pve.proxmox.com/pve-docs/vzdump.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE backup fleecing

**Goal:** reduce guest I/O stalls during VM backups to a slow target.

## The problem
When a VM backup starts, QEMU installs a "copy-before-write" filter in its block layer. On a new guest write, the old data still needed for the backup is sent to the backup target first. The guest write blocks until that finishes, so guest IO to not-yet-backed-up sectors is limited by the speed of the backup target.

## Fleecing
With fleecing, that old data is cached in a fleecing image instead of being sent directly to the backup target. This can help guest IO performance and even prevent hangs in certain scenarios, at the cost of more storage space. It applies to VMs only.

## Enable
Option syntax: `fleecing: [[enabled=]<1|0>] [,storage=<storage ID>]`; `enabled` defaults to 0.
```sh
vzdump 123 --fleecing enabled=1,storage=local-lvm
```
Set it per backup job (UI: Advanced tab when editing the job) or as a node-wide fallback in the configuration options. The global file is `/etc/vzdump.conf`, one `OPTION: value` per line, used as defaults and overridable on the command line, so the node-wide form is `fleecing: enabled=1,storage=local-lvm`.

## Choosing the fleecing storage
- Fast, local, with thin provisioning and discard support. Documented examples: LVM-thin, RBD, ZFS with `sparse 1` in the storage configuration, many file-based storages.
- Ideally a dedicated storage: if it runs full, other guests are unaffected and the backup just fails.
- Backed-up parts of the image are discarded to keep space usage low.
- File-based storage without discard (for example NFS before 4.2): set preallocation off in the storage configuration. The image uses qcow2 automatically when the storage supports it, so allocated parts can be reused.
- Not thin (for example LVM or ZFS without sparse): the full size of the original disk is reserved up front. On thin storage the image grows to the original size only if the guest rewrites a whole disk while the backup is busy with another disk.

## Checked
2026-11-07. Read in full: the "VM Backup Fleecing" section of the PVE Backup and Restore chapter (version 9.2.13) and the fleecing option text in its Configuration section; the vzdump.1 page carries the same fleecing text and option, and I confirmed that by search only, not a full read. Removed because neither page states them: "PVE 8.2+", the `--mode snapshot` and `--storage pbs1` command form, the GUI path "Datacenter -> Backup", the claim that guest writes "only wait for local storage", the monitoring and "avoid same slow disks" gotchas, the claim that containers use a different method (the pages say only that the option is VM only) and the invented fio Verify step.
Method: documentation only; no commands were run.
