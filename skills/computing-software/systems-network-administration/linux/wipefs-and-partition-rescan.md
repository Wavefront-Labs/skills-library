---
id: computing-software.systems-network-administration.linux.wipefs-and-partition-rescan
name: wipefs-and-partition-rescan
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, partitioning, wipefs, partprobe, partition-rescan, partx, blockdev-rereadpt, scsi-rescan, disk-reuse, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Prepare reused disks and make the kernel see changes: remove stale filesystem/RAID/LVM signatures with wipefs, and re-read partition tables or rescan LUNs without a reboot."
sources:
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/wipefs.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/partx.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/blockdev.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/disk-utils/sfdisk.8.adoc
  - https://github.com/torvalds/linux/blob/master/drivers/scsi/scsi_sysfs.c
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/nvme-ns-rescan.txt
  - https://github.com/opensvc/multipath-tools/blob/master/multipathd/multipathd.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wipefs and partition rescans

**Goal:** repurpose a disk without old signatures resurrecting (LVM, mdadm and ZFS will
happily auto-assemble stale metadata), and get the kernel to notice new partitions or a resized
LUN without rebooting.

## 1. wipefs
```bash
wipefs /dev/sdb                 # list signatures: offset, type (xfs, LVM2_member, linux_raid_member, gpt, PMBR…)
wipefs /dev/sdb1
wipefs -a -b /dev/sdb1          # erase all signatures on the partition, backup to ~/wipefs-sdb1-<offset>.bak
wipefs -a /dev/sdb              # whole disk: partition table signatures too
wipefs -o 0x438 /dev/sdb1       # erase only one signature at an offset
```
Restore from backup: `dd if=~/wipefs-sdb1-0x00000438.bak of=/dev/sdb1 seek=$((0x438)) bs=1 conv=notrunc`.
wipefs erases signatures (magic strings), not the data; use a dedicated erase tool when data must be unrecoverable.
Stop arrays and deactivate volume groups that use the device before wiping it.

## 2. Re-read the partition table
```bash
partx -u /dev/sdb               # update the kernel's view of existing partitions
partx -a /dev/sdb               # add the partitions found on the disk to the kernel's view
blockdev --rereadpt /dev/sdb    # BLKRRPART: reread the whole table; expect failure while the disk is in use
udevadm settle                  # wait for /dev nodes to appear in scripts
```
If the disk is in use, `partx -u` tells the kernel about changed partitions without rereading the whole
table (sfdisk does the same for `-N` and `--append` since util-linux 2.43).

## 3. New or resized disks/LUNs
```bash
echo '- - -' > /sys/class/scsi_host/host0/scan          # discover new LUNs (each hostN)
rescan-scsi-bus.sh -a                                     # sg3_utils, all hosts
echo 1 > /sys/class/block/sdb/device/rescan              # size change of an existing disk
nvme ns-rescan /dev/nvme0                                 # NVMe namespaces
multipathd resize map mpatha                              # then resize the multipath map
```

## Gotchas
- `wipefs -a /dev/sdb` on the wrong disk is instant data loss: check `lsblk -o NAME,SIZE,SERIAL,MOUNTPOINTS` first.
- Leftover GPT backup header at the disk end makes tools think GPT exists after an MBR write — `wipefs -a` the disk removes both.

## Verify
- [ ] `wipefs /dev/sdb` prints nothing before you create the new layout.
- [ ] `lsblk` shows new partitions/size immediately after rescan; no reboot needed.

## Checked
Checked 2026-10-26 against util-linux master (wipefs, partx, blockdev, sfdisk man page sources), the kernel scsi_sysfs.c source, nvme-cli's nvme-ns-rescan documentation and multipathd(8).
Confirmed: `wipefs`, `-a`, `-b` backup file name `wipefs-<dev>-<offset>.bak` in `$HOME`, `-o` offset with `0x` prefix, the dd restore example, additional magic strings for GPT; `partx -u/-a`; `blockdev --rereadpt`; the sysfs `scan` file on SCSI hosts (`-` is the wildcard) and the `rescan` file on SCSI devices; `nvme ns-rescan`; `multipathd resize map`.
Removed as unconfirmed: partprobe behaviour, growpart advice, the VMware remark, the blkdiscard and mdadm/pvremove ordering advice.
Method: documentation only; no commands were run.
