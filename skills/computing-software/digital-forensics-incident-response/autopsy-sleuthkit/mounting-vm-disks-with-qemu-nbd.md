---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.mounting-vm-disks-with-qemu-nbd
name: mounting-vm-disks-with-qemu-nbd
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [qemu-nbd, image-mounting, vm-acquisition, vmdk, dfir]
level: practitioner
status: docs-checked
description: "Expose virtual disk images as read-only /dev/nbd block devices with qemu-nbd, inspect backing chains and snapshots with qemu-img, and avoid untrusted-guest risks."
sources: ["https://www.qemu.org/docs/master/tools/qemu-nbd.html", "https://www.qemu.org/docs/master/tools/qemu-img.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mounting VM disks with qemu-nbd

**Goal:** analyse virtual disk files directly on a Linux workstation without converting them first.

## Steps
```bash
sudo modprobe nbd                                       # the page notes the nbd kernel module may need loading
qemu-img info --backing-chain disk.qcow2                # format, size, and every image in a backing chain
sudo qemu-nbd --read-only --connect=/dev/nbd0 disk.qcow2
# partitions found in the image may appear as /dev/nbd0p1 and so on
sudo qemu-nbd --disconnect /dev/nbd0
```
- `-r` / `--read-only` exports the disk read-only; `-c` / `--connect=DEV` binds the image to an NBD device (Linux only); `-d` / `--disconnect` releases it. Binding to a `/dev/nbd` device generally requires root.
- `-f FMT` / `--format=FMT` forces a block driver instead of auto-detecting.
- Caution from the QEMU documentation: do not use this method to mount file systems from an untrusted guest image, because a malicious guest may have prepared the image to trigger kernel bugs in partition probing or file system mounting. For untrusted images, use a disposable analysis environment.

## Snapshots and chains
- `qemu-img info --backing-chain FILE` enumerates each image in a backing chain (for example `base.qcow2 <- snap1.qcow2 <- snap2.qcow2`); JSON output is an array with `--output=json`.
- Internal snapshots of a qcow2 image: `qemu-img snapshot -l FILE` lists them. To export one with qemu-nbd use `-l` / `--load-snapshot=SNAPSHOT_PARAM` (`snapshot.id=` and `snapshot.name=` keys, or an id or name); that export is read-only unless `-s` is also used.
- `-s` / `--snapshot` uses the file as an external snapshot base and redirects writes to a temporary file, so the original is not modified by writes.

## Gotchas
- Always export with `--read-only`; otherwise a connected client can write to the image.
- Hash the image files before and after analysis. To make a raw copy: `qemu-img convert -O raw SRC OUT`, then hash it.

## Verify
Image file hashes are unchanged after analysis.

## Checked
Checked 2026-11-09 against the qemu-nbd and qemu-img documentation (options, snapshot and backing-chain behaviour, examples, caution about untrusted guests). Removed: the list of supported formats, ESXi and VMware descriptor/delta advice, mount options for ext4 and NTFS, LVM commands, `max_part=16`, encrypted VM notes, and a wrong `--snapshot=<name>` usage (internal snapshots use `-l`/`--load-snapshot`).
Method: documentation only; no commands were run.
