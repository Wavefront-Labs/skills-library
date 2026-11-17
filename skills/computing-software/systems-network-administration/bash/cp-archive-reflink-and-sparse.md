---
id: computing-software.systems-network-administration.bash.cp-archive-reflink-and-sparse
name: cp-archive-reflink-and-sparse
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, cp-reflink, cp-archive, cp-preserve, sparse-files, xattrs, file-management, cp]
level: practitioner
status: docs-checked
description: "Copy files faithfully with cp: -a vs -r, --preserve=all for ACLs/xattrs/SELinux, --reflink on Btrfs, --sparse, -u/-n behaviour and verifying the copy."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html
  - https://btrfs.readthedocs.io/en/latest/Reflink.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cp: archive, reflink and sparse copies

## Pick the right flags
| Need | Command |
|---|---|
| Faithful tree copy including symlinks as symlinks and hard links | `cp -a src/ dst/` (`-a` is the archive option; `-d` = `--no-dereference --preserve=links`) |
| Preserve everything explicitly | `cp --preserve=all` (the attribute list also includes mode incl. ACLs where possible, ownership, timestamps, links, context, xattr) |
| Adjust SELinux context to the system default for destination files | `cp -Z` (like `restorecon`) |
| Instant copy-on-write copy where the filesystem supports it (Btrfs documented) | `cp --reflink=always big.img copy.img` fails if unsupported; `--reflink=auto` falls back to a normal copy |
| Control holes in sparse files | `cp --sparse=always disk.raw backup.raw` (`auto` is the default; `never` writes full blocks) |
| Don't overwrite existing | `cp --update=none` (`-n`/`--no-clobber` is deprecated because of its exit status; `--update=none-fail` fails on skips) |
| Only newer | `cp -u` / `--update` (default `older` when `--update` is given with no value) |
| Hard-link instead of copy | `cp -l` / `--link` (`cp -al src/ snap/`) |

`--reflink=auto` is the default when no `--reflink` option is given, per the coreutils manual.

## Trailing slash semantics
`cp -a src dst/` puts the tree at `dst/src/...`; `cp -a src/. dst/` copies contents into existing `dst`.

## Gotchas
- Ownership can only be preserved by users with appropriate privileges; ordinary users may preserve group only if they are a member of it (coreutils manual).
- Reflinked copies share physical blocks and are independent: a change to one file does not affect the other (Btrfs docs). Reflink cannot cross filesystems.
- Btrfs: source and target must have the same NOCOW/checksum status for reflink to work.
- Without `--sparse`, `auto` makes the output sparse only if the input appears sparse; use `--sparse=always` to turn zero runs into holes, `never` to avoid holes (for example for a swap file).
- For huge trees or remote targets, use a tool built for that (rsync, not covered by these sources).

## Verify
- [ ] Compare source and destination (`diff -r`), and check that sparseness and attributes you need were kept.

## Checked
Date: 2026-11-02. Confirmed against the GNU coreutils cp manual (--preserve list, -d, -Z, --reflink and its default, --sparse modes, -n deprecation, --update modes, --link, ownership note) and the Btrfs Reflink page (block sharing, independence, cross-filesystem and NOCOW notes). Removed: coreutils 9.0+/9.2+ version gates, XFS reflink=1 and ZFS 2.2+ claims, "-a = -dR --preserve=all" equivalence (text not present in the fetched page), the cp -r ownership gotcha, silent non-root ownership behaviour, du double-counting, 100 GB thin-file claim, rsync -aHAX flags, getfacl/getfattr/du verify commands.
Method: documentation only; no commands were run.
