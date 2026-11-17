---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.reconstructing-lvm-and-raid-volumes
name: reconstructing-lvm-and-raid-volumes
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [lvm-forensics, raid-reconstruction, mdadm, lvm2, synology-shr, read-only, linux-forensics, dfir]
level: advanced
status: draft
description: "Reassemble Linux md RAID, hardware RAID images and LVM logical volumes from individual disk images read-only so filesystems can be examined."
sources: ["https://raid.wiki.kernel.org/index.php/RAID_setup", "https://man7.org/linux/man-pages/man8/lvm.8.html", "https://kb.synology.com/en-global/DSM/tutorial/How_can_I_recover_data_from_my_DiskStation_using_a_PC"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reconstructing LVM and RAID volumes

**Goal:** turn per-disk images from a server or NAS into the logical volume the OS saw,
without writing to evidence.

## Rule zero
Work on images, attached through **read-only loop devices**, and stop the OS from
auto-assembling arrays or activating LVM on your examination host.

```bash
for i in disk1 disk2 disk3 disk4; do losetup -r -P -f --show $i.dd; done
lsblk -o NAME,SIZE,FSTYPE,LABEL       # md members show linux_raid_member, LVM shows LVM2_member
```

## Linux software RAID (mdadm, also Synology/QNAP)
```bash
mdadm --examine /dev/loop0p3          # array UUID, level, chunk size, device role, event count
mdadm --assemble --readonly /dev/md0 /dev/loop0p3 /dev/loop1p3 /dev/loop2p3 /dev/loop3p3
cat /proc/mdstat
```
- Mismatched event counts mean a member dropped earlier; assemble without it (degraded) to see
  the latest consistent state, and examine the stale member separately for older data.
- Never use `--create` on evidence unless reconstructing from known parameters on copies.

## LVM2
```bash
pvscan --readonly ; vgscan --readonly ; lvscan --readonly     # discover (or pvs/vgs/lvs)
vgchange -ay --readonly <vg>                                  # activate read-only
mount -o ro,noload /dev/<vg>/<lv> /mnt/lv                      # ext4: noload skips journal replay
```
- LVM metadata text backups sit near the start of each PV (first MiB) and in
  `/etc/lvm/archive/` on the host; they show LV creation/resizing history and **removed
  LVs**, whose extents can be rebuilt with a crafted `dmsetup` table.
- LVM snapshots (`-wi-s-`) are point-in-time copies; examine them too.
- Name collisions with the examination host's VG: use `vgimportclone` on copies, or a
  dedicated analysis VM without LVM.

## Hardware RAID (controller metadata not readable)
Determine stripe size, disk order, parity rotation and offset empirically: look for known
structures (GPT header, NTFS boot sector, superblocks) across disks, then reassemble virtually
with tools like `ReclaiMe Free RAID Recovery`, `UFS Explorer`, X-Ways/EnCase RAID
reconstruction, or `mdadm --build` with guessed parameters on loop devices. Validate by
checking that large files open and hash correctly across stripe boundaries.

## Synology SHR
SHR = md RAID per size tier + LVM (`vg1000`) + ext4/Btrfs. Assemble each md, then
`vgchange -ay --readonly vg1000`.

## Self-check
The reassembled volume mounts read-only, filesystem metadata is consistent, and you recorded
the array parameters and member order used.
