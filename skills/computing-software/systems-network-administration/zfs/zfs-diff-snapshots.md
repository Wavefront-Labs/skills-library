---
id: computing-software.systems-network-administration.zfs.zfs-diff-snapshots
name: zfs-diff-snapshots
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, diff, snapshot, changes, file-types]
level: practitioner
status: docs-checked
description: "Compare a ZFS snapshot with a later snapshot or the live filesystem using zfs diff, and read the change and file-type characters."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-diff.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zfs diff

```
zfs diff [-FHth] snapshot snapshot|filesystem
```

The first argument is an earlier snapshot; the second is a later snapshot or the current filesystem.

```
zfs diff -F tank/test@before tank/test
```

## Output

Each line begins with a change character:

- `-` path removed
- `+` path created
- `M` path modified
- `R` path renamed (new path follows, shown with `->`)

A link-count change appears as `(+N)`.

## Flags

- `-F`: add a file-type column: `B` block device, `C` character device, `/` directory, `>` door, `|` named pipe, `@` symbolic link, `P` event port, `=` socket, `F` regular file.
- `-H`: parsable tab-separated output without headers and arrows.
- `-t`: show the path's inode change time first.
- `-h`: do not escape non-ASCII paths in the `\0ooo` style.

## Permissions

The delegated permission `diff` is needed for unprivileged users, since it does path lookup by object number.

## Checked

2026-11-03. Confirmed against zfs-diff(8) (synopsis, change characters, `-F` type characters, `-H`, `-t`, `-h`, example output with `(+1)` and `->`) and zfs-allow(8) (`diff` permission). Removed the generic use-case list.
Method: documentation only; no commands were run.
