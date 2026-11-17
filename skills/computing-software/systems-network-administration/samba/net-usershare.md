---
id: computing-software.systems-network-administration.samba.net-usershare
name: net-usershare
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-usershare, usershare, user-shares, net, file-sharing]
level: practitioner
status: docs-checked
description: "Let non-root users create shares with net usershare: smb.conf usershare parameters and defaults, command syntax, ACL letters, and directory requirements."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net usershare
smb.conf `[global]` (all disabled by default):
- `usershare max shares`: default `0` (user shares ignored). Set e.g. `10`.
- `usershare path`: default `${prefix}/var/locks/usershares`; must be owned by root, no access for other, writable only by its group owner, sticky bit set. Members of the group owner may create usershares.
- `usershare owner only`: default `yes` (path must be owned by the creating user).
- `usershare allow guests`: default `no`.
- `usershare prefix allow list`: absolute roots users may export, for example `/home /data /space`; `usershare prefix deny list` is the opposite and is processed first.

Commands:
```
net usershare add <sharename> <path> [comment] [acl] [guest_ok=[y|n]]
net usershare delete <sharename>
net usershare info [--long] [wildcard]
net usershare list [--long] [wildcard]
```
ACL entries are `user:permission` where permission is `F` (full), `R` (read) or `D` (deny); the default is `Everyone:R`. Example: `net usershare add docs /data/docs "Team docs" Everyone:R,alice:F`.

There is no modify command: rerun `net usershare add` with the same share name. smbd notices changes at connect time, so no restart is needed; deleting a share does not disconnect current users. Without `--long`, `info` and `list` show only shares created by the current user.

## Checked
2026-11-04: parameters, defaults, command syntax, ACL letters and behaviour compared with the net and smb.conf man pages. Removed: a testparm verification line the pages do not state.
Method: documentation only; no commands were run.
