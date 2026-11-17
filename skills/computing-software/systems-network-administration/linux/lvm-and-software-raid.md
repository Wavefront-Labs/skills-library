---
id: computing-software.systems-network-administration.linux.lvm-and-software-raid
name: lvm-and-software-raid
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, raid, mdadm, software-raid, pv, vg, lv, lvextend, lvresize, thin-provisioning, lvm-snapshot, raid1, raid5, raid10, mdstat, superblock, degraded-array, storage, sysadmin, disk-management, mdadm-conf]
level: advanced
status: docs-checked
description: "Build, grow, snapshot, and recover LVM volumes and mdadm software RAID arrays, including degraded-array rebuild and common gotchas."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvextend.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/lvreduce.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmthin.7_main
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/md.4
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# LVM and software RAID — flexible storage that survives a disk failure

**Goal:** stack physical disks into resizable logical volumes (LVM), add
redundancy with mdadm software RAID, and know the exact commands to grow,
snapshot, and recover either layer without reaching for a rescue disk.

## 1. LVM stack: PV → VG → LV
```bash
pvcreate /dev/sdb /dev/sdc              # mark disks (or partitions) as physical volumes
vgcreate data_vg /dev/sdb /dev/sdc      # pool them into a volume group
lvcreate -n app_lv -L 50G data_vg       # carve a logical volume
mkfs.ext4 /dev/data_vg/app_lv
mount /dev/data_vg/app_lv /srv/app
```
Inspect with `pvs`, `vgs`, `lvs` (short) or `pvdisplay`/`vgdisplay`/`lvdisplay`
(verbose). `vgs -o +vg_free` shows free space before you promise it to an LV.

### Grow online, shrink only offline
```bash
vgextend data_vg /dev/sdd               # add a disk to the pool first
lvextend -L +20G /dev/data_vg/app_lv
resize2fs /dev/data_vg/app_lv           # ext4; use `xfs_growfs <mnt>` for XFS
```
`lvextend -r` (`--resizefs`) runs the filesystem-specific resize command for you (`resize2fs`, `xfs_growfs` or `btrfs`; it may involve mounting, unmounting or fsck).
**Shrinking is filesystem-first**: unmount, `e2fsck -f`,
`resize2fs` to the *smaller* size, then `lvreduce -L <size>`. XFS cannot shrink
at all — only grow. Data in the reduced area is lost, so the filesystem must be resized *before* `lvreduce`.

### Snapshots
```bash
lvcreate -s -n app_snap -L 5G /dev/data_vg/app_lv
mount -o ro /dev/data_vg/app_snap /mnt/snap
```
Classic (non-thin) snapshots are copy-on-write against a fixed-size exception
store: size it for the churn expected during the snapshot's life, not the
source LV's size. Watch the snapshot's `Data%` in `lvs` and extend the snapshot LV with `lvextend` (or enable `snapshot_autoextend_threshold`) before it fills.
Thin snapshots share blocks inside a thin pool and are created without a size; the thin pool needs its own free-space monitoring
(`lvs -o+data_percent` on the pool).

## 2. mdadm software RAID
```bash
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
mdadm --detail /dev/md0                 # state, rebuild %, which device is which
cat /proc/mdstat                        # quick view, [UU] = both members up, [U_] = degraded
```
Common levels: RAID1 (mirror), RAID5 (single parity: tolerates one failed disk, and a second failure
during a rebuild loses the array), RAID6 (double parity), RAID10 (striped mirrors; you choose the number of
replicas and a near, far or offset layout).

### Persist the array
```bash
mdadm --detail --scan >> /etc/mdadm.conf          # or /etc/mdadm/mdadm.conf (both locations are read)
update-initramfs -u    # or dracut -f — if the array is needed during early boot
```
If the array is needed during early boot, regenerate the initramfs after changing mdadm.conf (distribution-specific).

### Replace a failed disk
```bash
mdadm --detail /dev/md0                       # confirm which member failed
mdadm /dev/md0 --fail /dev/sdc1 --remove /dev/sdc1   # if not already auto-failed
# physically swap the disk, partition it to match, then:
mdadm /dev/md0 --add /dev/sdc1
watch cat /proc/mdstat                        # resync progress; don't reboot mid-rebuild
```
A degraded array (`[U_]`) still serves I/O but has zero fault tolerance left —
treat any degraded state as a page-now event, not a backlog item.

### LVM on top of RAID
Standard pattern: `mdadm` builds `/dev/md0`, then `pvcreate /dev/md0` and the
LVM stack sits on top. This gives you RAID's redundancy and LVM's flexible
resizing in one stack — don't confuse it with `lvcreate --type raid1`, LVM's
own built-in RAID (dm-raid; see lvmraid(7)).

## Gotchas
- `pvcreate` on a disk with a stray old filesystem signature silently
  succeeds unless you `wipefs -a /dev/sdX` first — ghost signatures can
  confuse tools later.
- mdadm metadata version 1.0 stores the superblock at the end of the device, 1.1 at the start and 1.2 (the default in current mdadm builds) 4K from the start.
- `lvremove`/`vgremove` have no confirmation-free undo: LVM keeps metadata backups and archives that `vgcfgrestore` can restore (see the metadata backup skill), but a data backup remains the real rollback.

## Verify
- [ ] `vgs`/`lvs` show expected free space after any extend/reduce.
- [ ] `resize2fs`/`xfs_growfs` (or `-r` flag) ran to match the new LV size — `df -h` confirms.
- [ ] `cat /proc/mdstat` shows `[UU]` (all members) with no `(F)` or `_` markers.
- [ ] `/etc/mdadm.conf` (or `mdadm.conf`) lists the array and the initramfs was rebuilt.
- [ ] A simulated single-disk failure (`mdadm --fail`) still serves reads before you trust production data to the array.

## Checked

Checked against the lvm2 main branch (lvextend(8) `--resizefs`, lvreduce(8), lvmthin(7)) and the mdadm main branch (mdadm.8.in metadata versions and examples, md.4 RAID10), repository pushes 2026-10-09 and 2026-10-08.
Confirmed: `--resizefs` behaviour and the shrink warning (resize the filesystem before lvreduce); thin snapshots need no size; `mdadm --detail --scan >> mdadm.conf`; metadata version placement (1.0 end, 1.1 start, 1.2 4K from start); both mdadm.conf locations; RAID10 replicas and near/far/offset layouts.
Fixed: the skill said RAID10 needs 4 disks (that is the LVM raid10 minimum, not mdadm's), claimed a 1.2 superblock collides with a GPT table (members are partitions with their own superblock), used a non-existent `Snapshot_data%` report name, and said LVM removals can only be rolled back from snapshots or backups (metadata archives can be restored). Removed unconfirmed claims: the 2 TB URE guidance and the "silently unusable" snapshot wording.

Method: documentation only; no commands were run.
