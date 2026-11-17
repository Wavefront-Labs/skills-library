---
id: computing-software.systems-network-administration.bash.hard-and-symbolic-links
name: hard-and-symbolic-links
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, ln, hardlinks, symlinks, symbolic-links, hard-links, readlink, realpath, inode, dangling-symlink, relative-symlink, ln-sfn, file-management, lpic-1, lfcs, sysadmin]
level: practitioner
status: docs-checked
description: "Create and manage hard links and symlinks with ln: relative vs absolute targets, replacing a link with ln -sfn, resolving with readlink, inode semantics and dangling links."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html
  - https://man7.org/linux/man-pages/man7/symlink.7.html
  - https://man7.org/linux/man-pages/man1/readlink.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hard links and symlinks — two different things that both say "link"

**Goal:** choose the right link type, create it without the classic argument-order and
directory-target mistakes, and resolve links reliably.

## 1. The model
- **Hard link**: another name for an existing file; link and original share the same inode and
  are indistinguishable. Hard links cannot cross file system boundaries, and most systems
  prohibit hard links to directories.
- **Symlink**: a special file whose contents are the pathname of another file. It can refer to
  directories and cross filesystems, and the target need not exist (a dangling link). On Linux
  the permissions of an ordinary symlink are not used and are always 0777.

```bash
ln  /srv/data/file.txt /srv/mirror/file.txt      # hard
ln -s /srv/data/file.txt /srv/mirror/file.txt    # symbolic:  ln -s TARGET LINKNAME
```

## 2. Symlink targets: relative or absolute?
- An absolute symlink always points to the same file, even if the link's directory is moved.
- A relative symlink is resolved relative to the directory containing the link, not your cwd,
  so a string typed from another directory resolves differently. The coreutils manual suggests
  changing to the link's directory first.
- `-r` / `--relative` (only with `-s`) makes the target relative to the link location.

```bash
cd /opt/app && ln -s releases/2026-10-16 current
ln -sr /srv/data/file.txt /srv/mirror/link
```

## 3. Replacing links
- `ln` does not replace existing files unless `-f` / `--force` is used.
- If the destination is a symlink to a directory, `ln` by default treats it like a directory and
  creates the link inside it. `-n` / `--no-dereference` treats it as a normal file instead, so
  `ln -sfn releases/new current` replaces the `current` link itself.
- Per the coreutils manual, without `-b` there is no brief moment when the destination does not
  exist.

## 4. Inspecting and resolving
```bash
readlink current       # print the link's contents
readlink -f current    # canonicalize, following every symlink in every component
readlink -e current    # canonicalize, all components must exist
readlink -m current    # canonicalize, no components need exist
```
The exact existence rules for `-f` are in readlink(1).

## Failure modes
- "File exists" when linking: you wanted `-f` (and `-n` for a directory link).
- Link created inside the target directory instead of replacing it: missing `-n`.
- A symlink cycle: symlink(7) says loop detection is an upper limit on links followed, and an
  error results when it is exceeded.
- Hard link across filesystems or to a directory: not allowed (see section 1).

## Verify
- [ ] `readlink -f link` prints the intended target.

## Checked
2026-11-01. Confirmed against the coreutils `ln` manual page, symlink(7) and readlink(1):
hard link and symlink semantics, `-s`, `-f`, `-n`, `-r`, relative resolution, the
no-gap-without-`-b` statement, and the `readlink -f/-e/-m` option names. Removed: the claim that
`ln -sfn` is not atomic and the `mv -T` recipe (the coreutils manual says otherwise for `ln -f`),
the cp/tar/rsync/chmod/du table, editor and web-server notes, and error-message strings none of
the sources state.
Method: documentation only; no commands were run.
