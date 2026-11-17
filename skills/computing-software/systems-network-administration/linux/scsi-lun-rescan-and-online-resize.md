---
id: computing-software.systems-network-administration.linux.scsi-lun-rescan-and-online-resize
name: scsi-lun-rescan-and-online-resize
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lun-rescan, rescan-scsi-bus, scsi-rescan, lun-resize, multipath-resize, sg3-utils, san]
level: advanced
status: docs-checked
description: "Add, resize and remove SAN LUNs without rebooting: host scan via sysfs or rescan-scsi-bus.sh, rescanning device size, multipathd resize, and clean removal before unmapping."
sources:
  - https://manpages.debian.org/bookworm/sg3-utils/rescan-scsi-bus.sh.8.en.html
  - https://github.com/torvalds/linux/blob/master/drivers/scsi/scsi_sysfs.c
  - https://github.com/opensvc/multipath-tools/blob/master/multipathd/multipathd.8.in
  - https://github.com/open-iscsi/open-iscsi/blob/master/doc/iscsiadm.8.template
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUN rescan, resize and removal

## New LUN presented
```bash
for h in /sys/class/scsi_host/host*/scan; do echo "- - -" > "$h"; done   # channel target lun wildcards
rescan-scsi-bus.sh -a          # sg3_utils alternative (-a: scan all targets; -r/--remove: also remove gone devices)
lsblk ; multipath -ll           # new sdX paths and the multipath map
```
iSCSI: `iscsiadm -m session --rescan` (rescans all running sessions when no session id is given).

## LUN grown on the array
```bash
for d in sdc sdd sde sdf; do echo 1 > /sys/block/$d/device/rescan; done   # every path
multipathd resize map mpatha
pvresize /dev/mapper/mpatha     # if LVM PV; then lvextend -r ...
# partitioned: growpart <disk> <partition> (cloud-utils) before pvresize
```
`rescan-scsi-bus.sh -s` looks for resized disks and reloads associated multipath devices.

## Remove a LUN (before the storage team unmaps it)
```bash
umount /data ; vgchange -an vg_data ; vgexport vg_data       # stop all users
multipath -f mpatha                                          # flush the map
for d in sdc sdd sde sdf; do echo 1 > /sys/block/$d/device/delete; done
```
Then ask for unmapping, so the host no longer holds paths to the LUN (`multipath -ll` should list no leftover paths).

## Gotchas
- Wildcard scans on hosts with hundreds of LUNs take time; scan specific `H C T L` when known.
- Removing the wrong `sdX`: double-check with `multipath -ll` that all paths belong to the map you flushed.

## Verify
- [ ] `lsblk -o NAME,SIZE` shows the new size on all paths and the map; removed LUN leaves no stale `sd` devices.

## Checked
2026-10-27. Checked against the Linux kernel SCSI sysfs source (drivers/scsi/scsi_sysfs.c and scsi_scan.c, current master), the Debian rescan-scsi-bus.sh(8) page (sg3-utils 1.46), multipath-tools multipath(8) and multipathd(8) manual sources, and open-iscsi iscsiadm(8). Confirmed: the host scan attribute taking wildcard channel, target and LUN fields, the per-device rescan and delete attributes, rescan-scsi-bus.sh -a, -r and -s, multipathd resize map, multipath -f and -ll, iscsiadm --rescan; lvm2 manual sources for pvresize, lvextend -r (--resizefs), vgchange -a and vgexport; cloud-utils growpart usage (disk partition). Removed: parted resizepart, the issue_lip advice and the stale-path and hung-I/O consequence claim. The Red Hat documentation link in sources is not readable from this environment and was replaced by the kernel source files.

Method: documentation only; no commands were run.
