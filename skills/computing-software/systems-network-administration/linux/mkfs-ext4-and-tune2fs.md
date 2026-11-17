---
id: computing-software.systems-network-administration.linux.mkfs-ext4-and-tune2fs
name: mkfs-ext4-and-tune2fs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystems, ext4, mkfs-ext4, tune2fs, dumpe2fs, reserved-blocks, inode-ratio, fs-label, e2label, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Create ext4 filesystems with the right options (inode ratio, reserved blocks, labels, stride for RAID) and change them later with tune2fs; read the superblock with dumpe2fs."
sources:
  - https://github.com/tytso/e2fsprogs/blob/master/misc/mke2fs.8.in
  - https://github.com/tytso/e2fsprogs/blob/master/misc/tune2fs.8.in
  - https://github.com/tytso/e2fsprogs/blob/master/misc/mke2fs.conf.in
  - https://github.com/tytso/e2fsprogs/blob/master/misc/ext4.5.in
  - https://github.com/tytso/e2fsprogs/blob/master/resize/resize2fs.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mkfs.ext4 and tune2fs

**Goal:** an ext4 filesystem sized for its workload (many small files vs few big ones), with a
label/UUID you can mount by, and adjust it later without reformatting.

## 1. Create
```bash
mkfs.ext4 -L data /dev/vg0/data                    # defaults from /etc/mke2fs.conf
mkfs.ext4 -T news -L mail /dev/vg0/mail            # many small files: more inodes (usage types in mke2fs.conf)
mkfs.ext4 -T largefile4 /dev/vg0/media             # few huge files: 1 inode per 4 MiB
mkfs.ext4 -i 8192 /dev/sdb1                        # explicit bytes-per-inode
mkfs.ext4 -m 1 /dev/sdb1                           # reserved blocks 1 % instead of 5 %
mkfs.ext4 -E stride=16,stripe_width=48 /dev/md0    # RAID5 4 disks, 64k chunk, 4k blocks: stride=64/4, width=stride*3
mkfs.ext4 -E lazy_itable_init=0,nodiscard /dev/sdb1   # init everything now; skip discard on thin LUNs
mkfs.ext4 -n /dev/sdb1                             # dry run: display what would be done, without creating the filesystem
```
The bytes-per-inode ratio is **fixed at mkfs** — "No space left on device" with free blocks = out of
inodes (`df -i`). Choose `-T`/`-i` up front for maildirs, caches, package mirrors.

## 2. Inspect
```bash
dumpe2fs -h /dev/sdb1 | grep -E 'volume name|UUID|Inode count|Free inodes|Reserved block|Mount count|Check interval|features|state'
tune2fs -l /dev/sdb1     # same header info
```

## 3. Change with tune2fs (mostly online-safe)
```bash
tune2fs -L newlabel /dev/sdb1          # or e2label /dev/sdb1 newlabel
tune2fs -m 1 /dev/sdb1                 # reserved blocks percentage (mke2fs default 5 %)
tune2fs -r 50000 /dev/sdb1             # reserved blocks absolute
tune2fs -c 0 -i 0 /dev/sdb1            # disable periodic fsck by mount count / interval (shipped mke2fs.conf sets enable_periodic_fsck = 0)
tune2fs -U random /dev/sdb1            # new UUID (cloned disks); with metadata_csum, changing it while mounted needs the metadata_csum_seed feature
tune2fs -e remount-ro /dev/sdb1        # behaviour on errors: continue|remount-ro|panic
tune2fs -o acl,user_xattr /dev/sdb1    # default mount options stored in superblock
tune2fs -O ^has_journal /dev/sdb1      # remove the journal (clear the has_journal feature)
tune2fs -O metadata_csum /dev/sdb1     # store checksums in metadata blocks
```
Enabling some features can stop older kernels mounting the filesystem; read the `-O` section of tune2fs(8) and run `e2fsck` when it says so.

## Gotchas
- Changing the UUID means updating `/etc/fstab`, crypttab, GRUB/initramfs references.
- A filesystem larger than 2^32 blocks needs the `64bit` feature (ext4(5)); the shipped mke2fs.conf enables it for ext4.
- XFS cannot shrink, but `resize2fs` can shrink an unmounted ext4 filesystem — consider that when choosing.

## Verify
- [ ] `tune2fs -l` shows intended label, reserved count, inode count and error behaviour.
- [ ] `df -i` leaves headroom for the expected file count.
- [ ] fstab uses `LABEL=`/`UUID=` and `mount -a` succeeds.

## Checked
Checked 2026-10-26 against e2fsprogs master (misc/mke2fs.8.in, tune2fs.8.in, mke2fs.conf.in, ext4.5.in, resize/resize2fs.8.in).
Confirmed: `-T news` (4096 bytes/inode), `-T largefile4` (4 MiB/inode), `-i`, `-m` (default 5 %), `-E stride=,stripe_width=` with the RAID5 formula, `lazy_itable_init`, `nodiscard`, `-n`; tune2fs `-L`, `-m`, `-r`, `-c`, `-i`, `-U random`, `-e`, `-o`, `-O ^has_journal`, `-O metadata_csum`, `-O quota`/`-Q`; the bytes-per-inode ratio cannot be changed after creation (a resize keeps the ratio); enable_periodic_fsck is 0 in the shipped config; 64bit is in the ext4 feature list; resize2fs shrinks only unmounted filesystems.
Removed as unconfirmed: the 1 EiB / 16 TiB limits, advice on the reserved percentage for root filesystems, and the unmount / e2fsck -fD requirements for feature changes.
Method: documentation only; no commands were run.
