---
id: computing-software.systems-network-administration.samba.vfs-acl-xattr
name: vfs-acl-xattr
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-acl-xattr, acl-xattr, ignore-system-acls, vfs, nt-acl]
level: advanced
status: docs-checked
description: "Store Windows NT ACLs in an xattr with vfs_acl_xattr: ignore system acls, default acl style, security_acl_name, and the masks it enforces."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_acl_xattr.8.html
  - https://wiki.samba.org/index.php/Setting_up_a_Share_Using_Windows_ACLs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs acl xattr
```
[share]
    path = /srv/share
    vfs objects = acl_xattr
    acl_xattr:ignore system acls = yes
    acl_xattr:default acl style = windows
```
Options:
- `acl_xattr:ignore system acls`: default `no`. When `yes`, no best-effort mapping to the POSIX ACL layer, and it enforces `create mask = 0666`, `directory mask = 0777`, `map archive/hidden/readonly/system = no`, `store dos attributes = yes`.
- `acl_xattr:default acl style`: default `posix`. Synthesises an ACL when no `security.NTACL` exists: `posix` (from mode bits plus SYSTEM full), `windows` (owner and SYSTEM only), `everyone` (full control for S-1-1-0).
- `acl_xattr:security_acl_name`: unset means `security.NTACL`, a protected xattr normal users cannot read. A `user.` name such as `user.NTACL` is readable by any user; use only if you understand the consequence.

Workflow on a domain member: add `vfs objects = acl_xattr` and `map acl inherit = yes` (see windows-acl-share), then set permissions from Windows. Use `acl_xattr:ignore system acls = yes` only if the data is accessed solely via Samba (the manual page says system ACLs stay useful for local or NFS access).

On an AD DC, extended ACL support is enabled automatically (do not enable it manually), and custom VFS lists must keep the defaults: `vfs objects = dfs_samba4 acl_xattr recycle`.

Inspect with `smbcacls` or `samba-tool ntacl get FILE`.

## Checked

2026-11-04. Confirmed against the vfs_acl_xattr(8) manual page: the three options, their defaults and the enforced masks, security.NTACL protection, default acl style behaviours; against the Samba wiki pages Setting up a Share Using Windows ACLs and the AD DC setup page: map acl inherit, automatic ACL support on a DC, the dfs_samba4 acl_xattr recycle list; against samba-tool(8): ntacl get. Removed the unconfirmed lock-out warning.
Method: documentation only; no commands were run.
