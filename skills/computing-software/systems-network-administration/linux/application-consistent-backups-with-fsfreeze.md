---
id: computing-software.systems-network-administration.linux.application-consistent-backups-with-fsfreeze
name: application-consistent-backups-with-fsfreeze
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fsfreeze, application-consistent, crash-consistent, pre-snapshot-hook, lvm-snapshot, qemu-guest-agent]
level: practitioner
status: docs-checked
description: "Take application-consistent snapshots on Linux: flush databases, fsfreeze around cloud or hypervisor snapshots, guest-agent freeze hooks, and avoiding hung frozen filesystems."
sources:
  - https://man7.org/linux/man-pages/man8/fsfreeze.8.html
  - https://www.qemu.org/docs/master/interop/qemu-ga.html
  - https://www.postgresql.org/docs/current/backup-file.html
  - https://libvirt.org/manpages/virsh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Application-consistent backups

- **Crash-consistent**: like pulling the power. Journaling filesystems and databases with WAL recover, but the restore needs crash recovery and may lose in-flight transactions.
- **Application-consistent**: the application flushed and paused writes before the snapshot; restore starts clean.

## Pattern
1. Tell the app to flush/quiesce (or use its native backup mode).
2. `fsfreeze -f` the filesystem(s) to flush dirty pages and block new writes.
3. Take the snapshot (LVM, ZFS, EBS, hypervisor) - seconds, not minutes.
4. `fsfreeze -u` immediately, in a trap, whatever happens.
5. Release the app.

## Script skeleton
```bash
#!/bin/bash
set -euo pipefail
MNT=/srv/data
thaw() { fsfreeze -u "$MNT" 2>/dev/null || true; }
trap thaw EXIT
quiesce_app                      # application-specific: flush and pause writes
fsfreeze --freeze "$MNT"         # not needed for LVM/device-mapper snapshots: they freeze the fs themselves
snapshot_cmd                     # hardware RAID, SAN or cloud snapshot of the volume
fsfreeze --unfreeze "$MNT"
resume_app
```
PostgreSQL documents that a frozen snapshot of the volume holding the data directory works while the server runs: on restore it replays WAL as after a crash, and a `CHECKPOINT` beforehand shortens recovery. If data, WAL or tablespaces sit on different file systems the snapshots must be simultaneous; otherwise use a continuous-archiving base backup (`pg_backup_start()`/`pg_backup_stop()`).

## Never freeze root carelessly
- Freezing `/` (or the filesystem holding the script, logs, or `/tmp`) can deadlock the shell running the thaw. Run the controller from another host (guest agent) or keep the script on an unfrozen filesystem.
- Always set a timeout watchdog: `timeout 60 lvcreate ... || true` then thaw.
- `fsfreeze` works only on filesystems with freeze support (btrfs, ext2/3/4, f2fs, gfs2, jfs, nilfs2, xfs per the util-linux man page); the device-mapper/LVM layer freezes the filesystem itself when a snapshot is created.

## Hypervisor and cloud integration
- KVM/libvirt: `qemu-guest-agent` in the guest; `virsh snapshot-create-as vm snap --disk-only --quiesce` or `virsh domfsfreeze`/`domfsthaw`. qemu-ga must be started with `-F`/`--fsfreeze-hook`; its hook script runs the executables in a `fsfreeze-hook.d` directory beside it with `freeze` (before the filesystem is frozen) or `thaw` (after it is thawed). The default location is under `/etc/qemu/` unless `-F` names a path.
- Cloud and VMware snapshot tooling has its own quiesce hooks; read the vendor documentation.

## Restore test
Mount the snapshot elsewhere and start the database read-only; the log should show no crash recovery.

## Verify
- [ ] Freeze window measured (log timestamps) and under a few seconds.
- [ ] A restored snapshot starts without recovery messages; thaw always runs even when the snapshot command fails.

## Checked

Checked 2026-10-27 against util-linux fsfreeze(8) man page source, QEMU qemu-ga documentation and fsfreeze-hook script, libvirt virsh manual and PostgreSQL backup documentation (all current development branches, 2026-10-27). Confirmed: fsfreeze --freeze/--unfreeze usage and mountpoint argument, supported filesystem list, device-mapper automatic freeze, qemu-ga -F hook behaviour with freeze/thaw arguments, virsh domfsfreeze/domfsthaw and snapshot --quiesce, PostgreSQL frozen-snapshot and multi-volume guidance. Removed or softened: MySQL and EBS command examples, EBS point-in-time claim, RHEL hook path, VMware Tools and AWS backup paths.

Method: documentation only; no commands were run.
