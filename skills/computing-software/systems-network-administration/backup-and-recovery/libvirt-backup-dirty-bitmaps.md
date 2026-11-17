---
id: computing-software.systems-network-administration.backup-and-recovery.libvirt-backup-dirty-bitmaps
name: libvirt-backup-dirty-bitmaps
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [virsh-backup, dirty-bitmap, kvm-backup, libvirt, qemu, incremental-backup]
level: advanced
status: docs-checked
description: "Back up KVM guests with libvirt backup-begin and checkpoints: full and incremental push/pull backups using QEMU persistent dirty bitmaps, NBD export and virtnbdbackup."
sources:
  - https://libvirt.org/kbase/live_full_disk_backup.html
  - https://libvirt.org/formatbackup.html
  - https://libvirt.org/formatcheckpoint.html
  - https://github.com/abbbi/virtnbdbackup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libvirt backups with dirty bitmaps

**Goal:** consistent, incremental image backups of running KVM guests without external snapshot juggling.

## Requirements
- libvirt 7.2.0+ and QEMU 4.2+ for `virDomainBackupBegin()` (`virsh backup-begin`). Incremental backups are supported only for the QEMU driver with qcow2 disks at the active layer; use `<disks>` with `checkpoint='no'` to exclude non-qcow2 disks from a checkpoint.
- A running guest agent if you want a filesystem freeze (`virsh domfsfreeze`).

## Full push backup
```sh
virsh backup-begin vm1                        # full push backup; libvirt names files by appending a timestamp suffix
virsh domjobinfo vm1                          # progress; --completed after finish
```
With an XML to choose targets and create a checkpoint for later incrementals:
```xml
<domainbackup>
  <disks><disk name='vda' type='file'><target file='/backup/vm1-vda.full.qcow2'/><driver type='qcow2'/></disk></disks>
</domainbackup>
```
```xml
<domaincheckpoint><name>cp-2026-10-17</name></domaincheckpoint>
```
`virsh backup-begin vm1 backup.xml checkpoint.xml`

## Incremental
Add `<incremental>cp-2026-10-17</incremental>` to the backup XML and a new checkpoint XML. In push mode only the changes since the named checkpoint are written to the destination, so restoring needs the full backup plus every incremental in order. The default destination format is qcow2; a `<driver type=.../>` under `<target>` selects another.
```sh
virsh checkpoint-list vm1
virsh checkpoint-delete vm1 cp-2026-09-01      # merges its changed-block record into the parent checkpoint
```

## Pull mode
`<domainbackup mode='pull'><server transport='unix' socket='/run/vm1-nbd.sock'/>...` exports disks over NBD; a backup tool reads changed extents itself. Each disk needs a `<scratch>` file for temporary storage until the backup completes. virtnbdbackup wraps this (`virtnbdbackup -d vm1 -l full -o /backup/vm1`, then `-l inc`), and `virtnbdrestore` rebuilds images.

## Gotchas
- Creating a checkpoint while external snapshots exist is forbidden, so do not mix external snapshots with checkpoint-based backups.
- Starting with libvirt 11.10, `virsh backup-begin --preserve-domain-on-shutdown` keeps the guest paused instead of terminating it if the guest OS shuts down mid-backup; without it a shutdown ends the backup job.
- To see which bitmaps an image carries use `qemu-img info` (add `-U` / `--force-share` for an image in use).

## Verify
Restore the full + incrementals to a new image, `qemu-img check` it, and boot a test VM from it.

## Checked

Checked 2026-10-27 against the libvirt documentation in the libvirt/libvirt repository (docs/kbase/live_full_disk_backup.rst, docs/formatbackup.rst, docs/formatcheckpoint.rst, docs/manpages/virsh.rst), the QEMU qemu-img manual and the virtnbdbackup README (abbbi/virtnbdbackup). Confirmed: libvirt 7.2.0 and QEMU 4.2 for the backup API, the qcow2-at-active-layer requirement for incremental backups, timestamp-suffixed default file names, `<incremental>` semantics in push and pull mode, the pull-mode `<server>` and `<scratch>` elements, `checkpoint-delete` merging into the parent checkpoint, the ban on checkpoints with external snapshots, `--preserve-domain-on-shutdown` (libvirt 11.10), and the `virtnbdbackup -l full|inc` and `virtnbdrestore` commands. Removed claims about bitmap loss after unclean shutdowns and about the incremental image's backing file because the documentation does not state them.

Method: documentation only; no commands were run.
