---
id: computing-software.systems-network-administration.linux.df-du-discrepancy
name: df-du-discrepancy
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, df-du-discrepancy, hidden-under-mount, disk-usage, deleted-open-files, reserved-blocks, df]
level: practitioner
status: docs-checked
description: "Explain why df says full but du finds little: deleted-but-open files, data hidden under mount points, reserved blocks, snapshots/CoW, and bind-mount checks to find it."
sources:
  - https://man7.org/linux/man-pages/man1/df.1.html
  - https://man7.org/linux/man-pages/man1/du.1.html
  - https://man7.org/linux/man-pages/man8/lsof.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# df vs du discrepancies

`df` asks the filesystem how many blocks are used; `du` adds up files it can reach by walking directories.
Gaps come from blocks with no reachable path.

## Checklist (in order of likelihood)
1. **Deleted but still open** (rotated logs held by a daemon):
   `lsof -nP +L1 /var` (files with a link count below 1) → restart or reload the process holding them.
2. **Files hidden under a mount point** (written before the mount, e.g. to `/var/log` while it wasn't mounted):
   ```bash
   mkdir -p /mnt/rootonly && mount --bind / /mnt/rootonly     # bind of / shows what's under submounts
   du -xsh /mnt/rootonly/var/log /mnt/rootonly/srv
   umount /mnt/rootonly
   ```
3. **Reserved blocks** (ext2/3/4 reserve a percentage for privileged processes, set with `tune2fs -m`): `tune2fs -l /dev/X` lists the reserved block count.
4. **Snapshots / CoW**: Btrfs/ZFS snapshots keep deleted data (`btrfs filesystem usage`, `zfs list -o space`).
5. **du crossing or not crossing filesystems**: use `du -xsh /` vs `df /` for the same filesystem only.
6. **Sparse files/apparent size**: `du --apparent-size` reports apparent sizes, which can be larger than disk usage for sparse files; plain `du` and `df` count allocated blocks.
7. **Filesystem metadata and journal** take some space that no file path accounts for.

## Quick totals
```bash
df -hT /var ; du -xsh /var
df -i /var                # inodes are another kind of "full"
```

## Verify
- [ ] After the fix, `df` Used drops to roughly `du -x` of the same mount (minus reserved/metadata).

## Checked

Documentation check. Checked 2026-10-27 against the df(1), du(1), tune2fs(8), mount(8) and lsof(8) pages (man7.org), the OpenZFS zfs-list(8) page and the btrfs-filesystem documentation: `lsof +L1` (link count below 1), `du -x` (skip other filesystems), `du --apparent-size`, `df -i`, `tune2fs -l` and `-m` for reserved blocks, `mount --bind olddir newdir`, `btrfs filesystem usage` and `zfs list -o space`. Removed the 5 percent default, the sort pipeline, the truncate-via-proc trick, the thin-pool remark and the journal-size remarks, which the pages do not state.
Method: documentation only; no commands were run.
