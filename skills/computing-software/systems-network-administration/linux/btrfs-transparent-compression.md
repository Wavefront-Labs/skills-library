---
id: computing-software.systems-network-administration.linux.btrfs-transparent-compression
name: btrfs-transparent-compression
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, btrfs, btrfs-compression, compress-zstd, compsize, btrfs-property, defragment]
level: practitioner
status: docs-checked
description: "Enable Btrfs transparent compression: compress vs compress-force with zstd levels, per-directory properties, recompressing via defragment, and compsize."
sources:
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-compression.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-mount-options.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-file-attributes.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-property.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-filesystem.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-swapfile.rst
  - https://github.com/kilobyte/compsize/blob/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Btrfs transparent compression

## Enable
fstab: `UUID=... / btrfs defaults,compress=zstd:3,noatime 0 0` (remount: `mount -o remount,compress=zstd:3 /`).
- `compress=` — if the first blocks written to a file are not compressible, the whole file is marked to skip compression (heuristic); with no type given, zlib is used.
- `compress-force=` — always attempts compression; data may still end up uncompressed if compression would make it larger.
- Algorithms: `zstd` (levels 1-15; negative levels -15..-1 since kernel 6.15; default 3), `lzo` (no levels; fast, lower ratio), `zlib` (levels 1-9, default 3). Compression mount options are shared by all mounts of the same filesystem.
Only new writes are affected.

## Per file/directory
```bash
btrfs property set /srv/logs compression zstd      # per-inode property; a level cannot be set this way
btrfs property set /var/lib/libvirt/images compression none
chattr +c file   # legacy interface, selects zlib; chattr +m = no compression (needs e2fsprogs 1.46.2+)
```
Files with `nodatacow` are not compressed; `chattr +C` on a directory is inherited by new files, and on files it can only be set while they are empty.

## Compress existing data
`btrfs filesystem defragment -r -czstd /srv/data` — rewrites files compressed with that algorithm, regardless of mount options (`-L` sets a level in btrfs-progs 6.14+).
Warning: defragment breaks reflinks (snapshots, `cp --reflink`, deduplicated data), so space usage can grow.

## Measure
```bash
compsize /srv/data
# Type  Perc  Disk Usage  Uncompressed Referenced
# TOTAL  42%     4.2G        10G         10G
# zstd   35%  ...
```
compsize reports the effective compression ratio (it needs root).

## Gotchas
- Data are split into 128 KiB chunks before compression.
- Swap files on btrfs must not be compressed (and must be NOCOW).
- Higher zstd levels need more CPU and memory and may not improve the ratio much.

## Verify
- [ ] `findmnt -o OPTIONS /` shows compress; compsize reports a ratio below 100% for new data.

## Checked
Checked 2026-10-26 against btrfs-progs Documentation (master, pushed 2026-10-23): ch-compression, ch-mount-options, ch-file-attributes, btrfs-property, btrfs-filesystem, ch-swapfile, and the compsize README.
Confirmed: compress and compress-force semantics and the first-blocks heuristic; zstd, zlib and lzo level ranges and defaults; 128 KiB chunks; defragment `-c` and `-L`; `chattr +c` (zlib), `+m`, `+C`; swapfiles must be NODATACOW and so uncompressed; compsize columns.
Wrong in the draft: zstd levels are -15..15 (negative since 6.15), `-c`/compress-force wording, and `-v` on defragment is deprecated.
Removed as unconfirmed: directory inheritance of the compression property, the decompression-speed claim and the performance advice for VM images.
Method: documentation only; no commands were run.
