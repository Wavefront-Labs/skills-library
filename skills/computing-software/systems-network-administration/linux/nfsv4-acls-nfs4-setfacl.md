---
id: computing-software.systems-network-administration.linux.nfsv4-acls-nfs4-setfacl
name: nfsv4-acls-nfs4-setfacl
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nfs4-acl, nfs4-setfacl, nfs4-getfacl, nfsv4, acls, nfs-acl-tools]
level: advanced
status: docs-checked
description: "Read and set NFSv4 ACLs on NFS mounts with nfs4_getfacl/nfs4_setfacl: ACE format, inheritance flags, allow/deny ordering, and how they map from POSIX ACLs on Linux servers."
sources:
  - https://man7.org/linux/man-pages/man5/nfs4_acl.5.html
  - https://man7.org/linux/man-pages/man1/nfs4_setfacl.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NFSv4 ACLs

On NFSv4 mounts, POSIX `getfacl`/`setfacl` may not apply; use the `nfs4-acl-tools` commands `nfs4_getfacl` and
`nfs4_setfacl` (`nfs4_editfacl` is the same as `nfs4_setfacl -e`).

## Read
```bash
nfs4_getfacl /mnt/share/project
# A::OWNER@:rwatTnNcCy
# A:g:GROUP@:rtncy
# A::EVERYONE@:rtncy
```
ACE format `type:flags:principal:permissions` (the first three fields of the example above are `A`, flags, principal):
- type `A` allow, `D` deny, `U` audit, `L` alarm (audit and alarm are server-dependent and need `S` and/or `F` flags)
- flags `g` principal is a group; `d` directory-inherit, `f` file-inherit, `n` no-propagate-inherit, `i` inherit-only
  (inheritance flags only in a directory's ACL); `I` inherited (NFSv4.1 or newer, with `--dacl`/`--sacl`)
- principal `OWNER@`, `GROUP@`, `EVERYONE@`, or `user@nfsdomain` (a group needs the `g` flag)
- permissions `r` read-data/list, `w` write-data/create-file, `a` append/create-subdirectory, `x` execute/change-directory,
  `d` delete, `D` delete-child (directories only), `t`/`T` read/write attributes, `n`/`N` read/write named attributes,
  `c`/`C` read/write ACL, `o` write-owner, `y` synchronize. Generic shorthand letters such as `RX` appear in the
  man page examples.
- `EVERYONE@` always matches, unlike POSIX "other", which excludes the owner and group.

## Set
```bash
nfs4_setfacl -a "A:g:engineers@example.com:rxtncy" /mnt/share/project     # add (inserted at position 1 by default)
nfs4_setfacl -a "A:fdg:engineers@example.com:rxtncy" /mnt/share/project   # file- and directory-inherit
nfs4_setfacl -x "A:g:contractors@example.com:rxtncy" /mnt/share/project   # delete matching ACEs
nfs4_setfacl -e /mnt/share/project                                        # edit in your editor
nfs4_getfacl /mnt/share/template | nfs4_setfacl -S - /mnt/share/project   # replace ACL from stdin
nfs4_setfacl --test -x A::EVERYONE@:rtncy /mnt/share/project              # preview without applying
```
`-s`/`-S` replace the whole ACL, `-R` recurses. Use `--test` before a recursive change.

## Evaluation and deny ACEs
NFSv4 ACLs are default-deny: a permission not granted by an Allow ACE is denied. ACEs are evaluated in order and each
permission is decided by the first ACE that addresses it, so ordering matters when Deny ACEs are present. The man page
advises avoiding Deny ACEs where possible. A server may return an ACL slightly different from the one you set (extra
read-attributes, merged or reordered ACEs), but should not make it more permissive.

## Principals
Names must map through idmapping with the same NFSv4 domain on client and server, otherwise they appear as numbers
or `nobody`.

## Verify
- [ ] `nfs4_getfacl` shows the ACE; a test user in the group can create a file and the new file inherits the ACE.

## Checked
2026-10-28. Confirmed in the nfs4_acl(5) and nfs4_setfacl(1) man pages: ACE format, types, flags, principals, permission
letters, evaluation order and deny warning, server-altered ACLs, `-a -x -s -S -e -R --test`, default insert position 1.
Removed as unconfirmed: Linux knfsd POSIX-ACL translation claims, NetApp/Isilon/ZFS statements, `Operation not supported`
errors, `nfs4_setfacl -R -s` with command substitution, `RWX` shorthand.
Method: documentation only; no commands were run.
