---
id: computing-software.systems-network-administration.linux.mdadm-failed-disk-replacement-and-hot-spares
name: mdadm-failed-disk-replacement-and-hot-spares
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mdadm, software-raid, raid-replace, raid-disk-replacement, hot-spare, raid-rebuild, spare-group, degraded-array, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Replace a failed mdadm RAID member without losing the array: identify the bad disk, fail/remove/add, rebuild speed, hot spares and spare-groups, and boot disks."
sources:
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/md.4
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.conf.5.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mdadm: replace a failed disk, hot spares

**Goal:** get a degraded array back to full redundancy quickly, pulling the right physical disk.

## 1. Identify
```bash
cat /proc/mdstat                     # [U_] = one member missing; (F) = faulty
mdadm --detail /dev/md0              # State: clean, degraded; which slot is "faulty"/"removed"
smartctl -i /dev/sdb                 # shows the serial number — match it to the label on the drive
ls -l /dev/disk/by-id/ | grep sdb
```

## 2. Swap
```bash
mdadm --manage /dev/md0 --fail /dev/sdb1      # if not already marked faulty
mdadm --manage /dev/md0 --remove /dev/sdb1
# repeat for every array with a partition on sdb (md1 → sdb2 …)
# physically replace (hot-swap if the controller/backplane supports it), then:
# copy the partition layout from a healthy member with your partitioning tool (the new partition must be at least as large)
mdadm --manage /dev/md0 --add /dev/sdb1
watch cat /proc/mdstat                        # shows recovery progress
```
`mdadm /dev/md0 --replace /dev/sdb1 --with /dev/sdc1` (`--with` devices must already be spares in the array) rebuilds onto the
spare while the old device stays in service, and marks the old device faulty when done — keeps
redundancy during the copy; use it for proactive replacement of a disk with rising SMART errors.

## 3. Rebuild speed
```bash
cat /proc/sys/dev/raid/speed_limit_min /proc/sys/dev/raid/speed_limit_max   # KiB/s per device (default min 1000)
sysctl -w dev.raid.speed_limit_min=100000     # rebuild faster (more impact on I/O)
echo 32768 > /sys/block/md0/md/stripe_cache_size   # RAID5/6 only; pages per device, default 256, max 32768 (uses RAM)
```
A write-intent bitmap (`mdadm --grow --bitmap=internal /dev/md0`) makes re-adding a briefly
disconnected disk resync only changed regions.

## 4. Hot spares
```bash
mdadm --manage /dev/md0 --add /dev/sdd1       # on a healthy array, the new disk becomes a spare
mdadm --detail /dev/md0 | grep -i spare
```
Rebuild onto a spare starts automatically on failure. Share spares between arrays with
`spare-group=`: in `/etc/mdadm.conf` (or `/etc/mdadm/mdadm.conf`) give each ARRAY line
`spare-group=pool1` and run `mdadm --monitor` (mdmonitor.service where systemd manages it) — it moves a spare from one array in the group to a degraded one.
Monitoring/alerts: `MAILADDR root@example.com` in mdadm.conf;
`mdadm --monitor --scan --test --oneshot` generates a TestMessage alert for every array.

## 5. Boot disks
If the failed disk held the bootloader or an EFI system partition, recreate them on the new disk with your distribution's bootloader tools (not part of mdadm). Otherwise the next failure of the other disk leaves the box unbootable.

## Gotchas
- A second failure beyond the array's redundancy during rebuild loses the array — replace quickly.
- Adding the new disk to the wrong md (partition mismatch) — check `lsblk` after copying the layout.
- Don't `--zero-superblock` the surviving members.

## Verify
- [ ] `/proc/mdstat` shows `[UU]`/`[UUUU]` and `mdadm --detail` State: clean.
- [ ] The `--test` alert arrives; spare count is as designed.
- [ ] Boot test with the *other* disk removed (lab/maintenance window) if it's a boot array.

## Checked

Checked against the mdadm main branch (mdadm.8.in, md.4, mdadm.conf.5.in, Makefile), repository last pushed 2026-10-08.
Confirmed: `--replace` and `--with` semantics (old device stays in service, then marked faulty); `--test`/`--oneshot` generate TestMessage; spare-group migration through `mdadm --monitor`; default config file names; `speed_limit_min` is KiB/s per device (default 1000); `stripe_cache_size` is RAID5/6 only, default 256, range 17 to 32768.
Removed unconfirmed claims: ledctl, the sfdisk/sgdisk partition-copy commands, example rebuild speeds, GRUB and efibootmgr commands, and the RAID5 URE remark.

Method: documentation only; no commands were run.
