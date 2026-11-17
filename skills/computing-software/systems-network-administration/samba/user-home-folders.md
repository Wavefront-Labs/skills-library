---
id: computing-software.systems-network-administration.samba.user-home-folders
name: user-home-folders
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, user-home-folders, home-folders, homedirectory, file-sharing, active-directory]
level: practitioner
status: docs-checked
description: "Provide per-user home folders on Samba with a users share instead of homes: smb.conf, directory permissions, Windows ACLs, and assigning the home drive in AD."
sources:
  - https://wiki.samba.org/index.php/User_Home_Folders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# user home folders
The wiki says do not name the share `homes`; use `users`:
```
[users]
    path = /srv/samba/users/
    read only = no
    force create mode = 0600
    force directory mode = 0700
```
POSIX ACL setup (not usable on an AD DC):
```
mkdir -p /srv/samba/users/
chgrp -R "Domain Users" /srv/samba/users/
chmod 2750 /srv/samba/users/
mkdir /srv/samba/users/demo/
chown user_name /srv/samba/users/demo/
chmod 700 /srv/samba/users/demo/
smbcontrol all reload-config
```
Windows ACL setup on the share root (Security tab): Domain Users read & execute on this folder only; CREATOR OWNER full control on subfolders and files only; Domain Admins full control on this folder, subfolders and files.

Assign the home in AD:
- ADUC Profile tab: Connect, a drive letter, and `\\server\users\demo\`.
- `ldbedit -H /usr/local/samba/private/sam.ldb 'sAMAccountName=demo'` and add `homeDrive: H:` and `homeDirectory: \\server\users\demo\`.
- NT4 domain `[global]`: `logon drive = H:` and `logon home = \\server\users\%U`.

If ADUC warns that the home folder was not created, the page says the users share's Windows ACLs were set incorrectly (fix them), or, with a POSIX ACL share, to create the directory manually.

## Checked
2026-11-04: share definitions, POSIX and Windows ACL setup, ADUC, ldbedit and NT4 home assignment compared with the User Home Folders wiki page. Reworded the final warning note to what the page states.
Method: documentation only; no commands were run.
