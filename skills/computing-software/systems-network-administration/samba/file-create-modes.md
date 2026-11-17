---
id: computing-software.systems-network-administration.samba.file-create-modes
name: file-create-modes
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, file-create-modes, force-user, create-mask, inherit-permissions, smb-conf]
level: practitioner
status: docs-checked
description: "Set Unix permissions on files Samba creates: create mask, directory mask, force create and directory mode, force user and group, inherit permissions, DOS attribute mapping."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# file create modes
Per-share parameters and defaults:
- `create mask`: `0744`. ANDed with the Unix mode on file creation.
- `directory mask`: `0755`. Removes group/other write by default; example `0775`.
- `force create mode`: `0000`. ORed on after the create mask.
- `force directory mode`: `0000`. ORed on after the directory mask.
- `force user`: none; all file operations run as this Unix user (clients still authenticate).
- `force group`: none; a leading `+` applies it only to users already in that group.
- `inherit permissions`: `no`; yes makes new directories take the parent's mode and files its read/write bits (setuid never inherited).
- `inherit acls`: `no`; yes sets mode 0777 on creation so default directory ACLs propagate.
- `dos filemode`: `no`; yes lets any user with write access change permissions.
- `store dos attributes`: `yes` (since 4.9.0), kept in `user.DOSATTRIB`; overrides `map archive` (`yes`), `map hidden` (`no`), `map system` (`no`) and `map readonly` (`no`). On Linux the filesystem needs `user_xattr`.
- `inherit owner`: `no`; `windows and unix` (or `yes`) sets both owners from the parent directory, `unix only` sets only the UNIX owner.

Order: the mask removes bits, then the force mode adds bits.

Example for a team share:
```
[team]
   path = /srv/samba/team
   read only = no
   create mask = 0660
   directory mask = 0770
   force group = teamgroup
```

## Checked
2026-11-04: defaults and behaviour of each parameter compared with the smb.conf man page. Removed: a claim that acl_xattr:ignore system acls forces create and directory masks, and a generic verify line, neither stated on the page.
Method: documentation only; no commands were run.
