---
id: computing-software.systems-network-administration.samba.roaming-profiles
name: roaming-profiles
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, roaming-profiles, profilepath, profiles-share, windows-acls, file-sharing]
level: practitioner
status: docs-checked
description: "Host Windows roaming profiles on Samba: the profiles share with acl_xattr and csc policy, root permissions, how to assign the profile path in AD, GPO or NT4."
sources:
  - https://wiki.samba.org/index.php/Roaming_Windows_User_Profiles
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# roaming profiles
Recommended Windows ACL method (also for AD DCs):
```
[profiles]
    comment = Users profiles
    path = /srv/samba/profiles/
    ;browseable = No
    read only = No
    csc policy = disable
    vfs objects = acl_xattr
```
Keep `browseable = No` commented while setting permissions in RSAT, then enable it.
```
mkdir -p /srv/samba/profiles
chown root:"Domain Admins" /srv/samba/profiles
chmod 0770 /srv/samba/profiles
```
NTFS permissions on the share root (disable inheritance): Domain Users traverse/list/create folder on this folder only; CREATOR OWNER full control on subfolders and files only; Domain Admins and SYSTEM full control on all.

POSIX alternative (domain members only) adds `force create mode = 0600`, `force directory mode = 0700`, `store dos attributes = yes`, with `chgrp -R "Domain Users"` and `chmod 1750`, then `smbcontrol all reload-config`.

Assign the path with no version suffix and no trailing backslash:
- ADUC Profile tab: `\\server\profiles\demo`
- GPO: User Profiles, "Set roaming profile path for all users logging onto this computer": `\\server\profiles\%USERNAME%`
- `ldbedit` on a DC: add `profilePath: \\server\profiles\demo`
- NT4 domain `[global]`: `logon path = \\%L\Profiles\%U`

The smb.conf `logon path` default is `\\%N\%U\profile`; the smb.conf page says it must not include a reference to the homes share, and not to quote the value.

## Checked
2026-11-04: share definitions, permissions, profile-path assignment methods and NT4 logon path compared with the Roaming Windows User Profiles wiki page; the logon path default and warnings compared with the smb.conf man page. Nothing removed.
Method: documentation only; no commands were run.
