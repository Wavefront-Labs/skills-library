---
id: computing-software.systems-network-administration.bash.cpio-and-dd-images
name: cpio-and-dd-images
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, cpio, dd, disk-image, block-copy, initramfs-cpio, rpm2cpio, dd-progress, conv-sync-noerror, bs-blocksize, oflag-direct, usb-image, file-management, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Use cpio for copy-out, copy-in and pass-through archives, and dd for raw device and image copies: block sizes, status=progress, conv options, direct I/O, safe targeting."
sources:
  - https://www.gnu.org/software/cpio/manual/cpio.html
  - https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html
  - https://man7.org/linux/man-pages/man1/dd.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cpio and dd — the archivers underneath packages and boot images

**Goal:** know the two tools you meet inside packages, initramfs images and disk cloning,
and use dd without wiping the wrong disk.

## 1. cpio — three modes
```bash
# copy-out (create): list of files on stdin
find /etc -depth -print0 | cpio --null -ov -H newc > etc.cpio
# copy-in (extract)
mkdir x && cd x && cpio -idmv < ../etc.cpio       # -d make directories, -m preserve modification time
# pass-through (copy a tree)
find src -depth -print0 | cpio --null -pdmv /dest
```
- `-H format` selects the archive format. Copy-out defaults to `bin`; copy-in detects the
  format automatically. `newc` is the SVR4 portable format and supports file systems having
  more than 65536 i-nodes.
- `find -print0` with `cpio --null` passes file names safely even with special characters.

## 2. dd — copy blocks, not files
```bash
dd if=image.iso of=/dev/sdX bs=4M status=progress oflag=direct conv=fsync
dd if=/dev/sda of=/mnt/backup/sda.img bs=4M status=progress conv=sparse
dd if=/dev/zero of=/swapfile bs=1M count=4096 status=progress
```
Confirm the target device by name, size and model before every run.
- The default block size is 512 bytes (`ibs`/`obs`); set `bs=` larger for throughput, but
  values above a few megabytes are generally wasteful.
- `status=progress` periodically updates the last line of output; sending `USR1` to a
  running dd (INFO where available) makes it print I/O statistics.
- `oflag=direct` uses direct I/O, avoiding the buffer cache; the kernel may impose buffer-size
  restrictions (the manual's example: EINVAL on ext4 if the output buffer size is not a
  multiple of 512).
- `conv=fsync` synchronizes output data and metadata just before finishing.
- `conv=sparse` seeks rather than writing NUL output blocks; be careful combining it with
  `conv=notrunc` or `oflag=append`.
- `conv=notrunc` does not truncate the output file.

## 3. Rescuing failing disks
```bash
dd if=/dev/sdb of=sdb.img bs=64K conv=sync,noerror status=progress
```
`noerror` continues after read errors; `sync` pads each input block to the `ibs` size with
zero bytes, which keeps offsets aligned. The coreutils manual points to GNU ddrescue for
cases where dd is not enough.

## 4. Offsets
`skip=` applies to the input and `seek=` to the output, in blocks.

## Failure modes
- Wrote to the system disk: device names can change between boots and plug-ins; re-check the target immediately before running.
- cpio archive the consumer rejects: wrong `-H` format.

## Checked
2026-11-01: confirmed against the GNU cpio manual (modes, `--null`, `-d`, `-m`, `-H` formats and defaults) and the GNU coreutils dd manual (default block size, status=progress, USR1/INFO, conv sync/noerror/sparse/fsync/notrunc, oflag=direct, skip/seek, ddrescue pointer). Removed: RPM and initramfs tooling (rpm2cpio, lsinitrd, skipcpio), device-listing and verification commands, MBR and partition-extraction examples, and distro remarks.
Method: documentation only; no commands were run.
