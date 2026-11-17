---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.mounting-e01-images-read-only
name: mounting-e01-images-read-only
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ewfmount, image-mounting, e01, loop-device, arsenal-image-mounter, dfir]
level: practitioner
status: docs-checked
description: "Mount E01 and raw forensic images read-only on Linux and Windows: ewfmount, read-only loop devices with offsets or partition scan, and Arsenal Image Mounter."
sources: ["https://github.com/libyal/libewf/wiki/Mounting", "https://arsenalrecon.com/products/arsenal-image-mounter", "https://man7.org/linux/man-pages/man8/losetup.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mounting E01 images read-only

**Goal:** browse an image's filesystems with ordinary tools without any chance of modifying
the evidence.

## Linux
```bash
mkdir -p /mnt/ewf /mnt/evid
ewfmount evid001.E01 /mnt/ewf          # FUSE mount; exposes /mnt/ewf/ewf1 as a raw image
# find the partition start offset (for example with mmls from the Sleuth Kit), then:
sudo mount -o loop,ro,offset=<BYTE_OFFSET> /mnt/ewf/ewf1 /mnt/evid
# or create partition loop devices
sudo losetup -r -P -f --show /mnt/ewf/ewf1   # -r read-only, -P scan partitions
```
- The offset is in bytes from the start of the device file to the start of the file system
  (sector number times sector size).
- `losetup -r` sets up a read-only loop device; `-P`/`--partscan` scans for partitions and
  `-o` moves the data start by an offset.
- By default FUSE prevents root accessing the mount point; if needed pass `-X allow_root`
  to ewfmount (and check `/etc/fuse.conf`).
- Unmount with `umount /mnt/ewf` or `fusermount -u /mnt/ewf`; detach loop devices with `losetup -d`.
- For dirty or hibernated file systems and journal replay, check the mount options of the
  file system driver in use and work on a **copy**, or analyse with Sleuth Kit without mounting.

## Windows
- **Arsenal Image Mounter**: mounts disk images as real disks and offers temporary write
  support with replayable differencing files, BitLocker identify/unlock, and Volume Shadow
  Copy access (see the product page for supported formats and current features).
- `ewfmount` can also run on Windows (for example `ewfmount image.E01 x:` per the libewf wiki).

## Verify
After unmounting, re-hash the image and compare to the acquisition hash.

## Checked
2026-11-01. Confirmed in the libewf Mounting wiki (ewfmount, `ewf1`, `mount -o loop,ro,offset=`,
`-X allow_root`, `fusermount -u`, Windows drive-letter usage), the losetup man page (`-r`, `-P`,
`-o`) and the Arsenal product page (temporary write with differencing files, BitLocker, VSS).
Removed: NTFS `show_sys_files`/`streams_interface`/`remove_hiberfile` options, ext4 `noload`,
the `ewfverify` step, FTK Imager and the image-format list, which the fetched pages do not confirm.
Method: documentation only; no commands were run.
