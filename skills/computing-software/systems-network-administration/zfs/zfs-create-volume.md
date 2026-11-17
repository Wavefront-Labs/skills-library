---
id: computing-software.systems-network-administration.zfs.zfs-create-volume
name: zfs-create-volume
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zvol, volume, volblocksize, sparse, block-device]
level: practitioner
status: docs-checked
description: "Create a ZFS volume (zvol) block device with zfs create -V, choose block size with -b, make it sparse with -s, and avoid swap on ZFS."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-create.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a volume

A volume is a block device backed by the pool.

```
zfs create [-ps] [-b blocksize] [-o property=value]... -V size volume
```

Example:

```
zfs create -V 20G -b 16K tank/vm-disk0
```

The device appears under `/dev/zvol/` with the dataset path.

## Details

- `-V size`: the logical size. It is rounded up to a multiple of the block size.
- `-b blocksize`: same as `-o volblocksize=blocksize`. Using both gives undefined behaviour, so pick one.
- By default a reservation equal to the volume size is created, so space is guaranteed. `-s` creates a sparse volume with no reservation; see `volsize` in zfsprops(7).
- `-p`, `-o`, `-n` and `-v` behave as for filesystems; `-P` reports the volume name and property lines, including `refreservation` when the volume is not sparse.

## Cautions

The man page states that swapping to a ZFS volume is prone to deadlock and not recommended, and that swapping to a file on a ZFS filesystem is not supported.

## Checked

2026-11-03. Confirmed against zfs-create(8): volume synopsis, `/dev/zvol/` path, default reservation, rounding to the block size, `-b` versus `-o volblocksize`, `-s`, `-P` and the swap warning. Removed the unsupported sparse-volume and block-size advice.
Method: documentation only; no commands were run.
