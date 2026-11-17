---
id: computing-software.systems-network-administration.samba.windows-acl-share
name: windows-acl-share
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, windows-acl-share, windows-acls, sediskoperatorprivilege, acl-xattr, file-sharing]
level: practitioner
status: docs-checked
description: "Set up a Samba share managed from Windows ACLs: acl_xattr and map acl inherit settings, directory ownership, Windows tool steps, SeDiskOperatorPrivilege, ignore system acls."
sources:
  - https://wiki.samba.org/index.php/Setting_up_a_Share_Using_Windows_ACLs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows acl share
Check ACL support: `smbd -b | grep HAVE_LIBACL`.

Domain member `[global]`:
```
vfs objects = acl_xattr
map acl inherit = yes
store dos attributes = yes
```
(`store dos attributes` is only needed before Samba 4.9.0.) On an AD DC these are automatic; do not add them. Share:
```
[Demo]
   path = /srv/samba/Demo/
   read only = no
```
Set no other share parameters. Directory (group `Unix Admins` for the `ad` backend, else `Domain Admins`):
```
mkdir -p /srv/samba/Demo/
chown root:"Domain Admins" /srv/samba/Demo/
chmod 0770 /srv/samba/Demo/
smbcontrol all reload-config
```
Windows: Computer Management, connect to the Samba host, Shared Folders > Shares > Properties. Leave Share Permissions at Everyone; use the Security tab (Edit) to grant groups like Domain Users.

Rules: only owner/group members of the directory edit Security; only SeDiskOperatorPrivilege holders edit Share Permissions (list: `net rpc rights list privileges SeDiskOperatorPrivilege -U "SAMDOM\administrator"`; grant to a group on this server).

Optional, only after permissions are set: `acl_xattr:ignore system acls = yes`. ACLs live in `security.NTACL`.

With the `ad` idmap backend, do not give Domain Admins a gidNumber (the page says it breaks the mapping in idmap.ldb); create a group such as `Unix Admins` with a gidNumber instead.

## Checked
2026-11-04: ACL support check, global settings, SeDiskOperatorPrivilege handling, share and directory setup, Windows tool steps and ACL storage compared with the Setting up a Share Using Windows ACLs wiki page. Nothing removed.
Method: documentation only; no commands were run.
