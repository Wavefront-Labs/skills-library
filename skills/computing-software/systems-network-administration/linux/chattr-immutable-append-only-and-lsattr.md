---
id: computing-software.systems-network-administration.linux.chattr-immutable-append-only-and-lsattr
name: chattr-immutable-append-only-and-lsattr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, file-attributes, chattr, lsattr, immutable, append-only, nocow, file-hardening, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Make files immutable (+i) or append-only (+a) even against root mistakes, list attributes with lsattr, and diagnose root's 'Operation not permitted' errors."
sources:
  - https://github.com/tytso/e2fsprogs/blob/master/misc/chattr.1.in
  - https://github.com/tytso/e2fsprogs/blob/master/misc/lsattr.1.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# chattr/lsattr: immutable and append-only

**Goal:** protect critical files from accidental change or deletion, keep logs append-only, and
recognise when an attribute is why root gets "Operation not permitted".

## 1. List
```bash
lsattr /etc/resolv.conf
lsattr -d /srv/data          # the directory itself, not its contents
lsattr -R /etc 2>/dev/null | grep -E '^[^ ]*[ia]'    # find immutable/append-only files (-R recurses)
```
Output like `----i---------e------- file`: `i` immutable, `a` append-only, `e` extents (the file maps blocks with extents; chattr cannot remove it). `lsattr` lists ext2/ext3/ext4 attributes.

## 2. Immutable (+i)
```bash
chattr +i /etc/resolv.conf     # cannot be modified, deleted or renamed, no links, no write-open — even by root
chattr -i /etc/resolv.conf
```
Setting or clearing it requires `CAP_LINUX_IMMUTABLE` (superuser). Use cases: freeze a known-good config during an
incident, protect a file from a misbehaving script (for tools that rewrite a file, configure them properly instead).
Setting `a` or `i` does not affect writes through file descriptors that are already open.

## 3. Append-only (+a)
```bash
chattr +a /var/log/app/audit.log   # can only be opened in append mode for writing
```
Rotation that renames or truncates such a file will be refused, so clear the flag around rotation or skip rotation
for these files. Good for local audit trails where tampering by a compromised service account should be hard.

## 4. Other attributes worth knowing
`+C` no copy-on-write (set on new or empty files; only on copy-on-write filesystems such as Btrfs),
`+A` no atime updates, `+d` skip in dump(8) backups, `+S` synchronous updates, `+D` synchronous directory updates.
`c`, `s` and `u` are not honoured by ext2/3/4 in mainline kernels. Not all flags are supported by all filesystems; see the
filesystem's own man page.

## 5. Diagnosing
Root getting `Operation not permitted` (not "Permission denied") on rm/mv/write → check
`lsattr` before suspecting SELinux. Package updates failing on a file ("cannot open: Operation not
permitted") → someone set `+i`. An unexpected immutable binary is worth investigating.

## Gotchas
- Check that your copy or backup tool preserves attributes; re-apply after a restore if it does not.
- The superuser can clear them (`chattr -i`); they guard against mistakes, not a determined root attacker.

## Verify
- [ ] `lsattr <file>` shows the flag; `rm` as root fails with "Operation not permitted".
- [ ] For append-only logs, `echo x >> file` works and `> file` fails; your rotation setup handles it.

## Checked

2026-10-26. e2fsprogs master (last commit 2026-09-07): chattr(1) attribute letters and meanings (a, A, C, d, D, e, i, S, s, u, c), CAP_LINUX_IMMUTABLE requirement, the note that a and i do not affect open file descriptors, the limitation that c, s and u are not honoured by ext2/3/4, C only for copy-on-write filesystems and new or empty files on Btrfs; lsattr(1) -R, -d, ext2/3/4 scope. Removed unconfirmed directory semantics, XFS attribute list, NFS/tmpfs remarks, logrotate directives and the rootkit statement.

Method: documentation only; no commands were run.
