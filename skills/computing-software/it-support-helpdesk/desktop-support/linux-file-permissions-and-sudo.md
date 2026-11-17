---
id: computing-software.it-support-helpdesk.desktop-support.linux-file-permissions-and-sudo
name: linux-file-permissions-and-sudo
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, linux-client, linux-permissions, chmod, chown, umask, sudoers, visudo, setfacl, permission-denied, groups, comptia-a-plus]
level: practitioner
status: draft
description: "Fix 'Permission denied' on Linux desktops: reading ls -l modes, chmod/chown, groups and newgrp, ACLs, and granting scoped sudo with visudo instead of full root."
sources:
  - "https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html"
  - "https://www.sudo.ws/docs/man/sudoers.man/"
  - "https://man7.org/linux/man-pages/man1/setfacl.1.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# linux-file-permissions-and-sudo

Goal: give users the access they need on Linux with the narrowest change,
and explain why "just chmod 777" is wrong.

## Read permissions
```bash
ls -l file      # -rw-r----- 1 alice finance 1204 ... report.csv
id alice        # uid, gid, groups
namei -l /srv/share/finance/report.csv   # permissions on every path component
```
`rwx` for owner / group / others; directories need `x` to enter and `r` to
list. A user blocked at any parent directory gets "Permission denied" even
if the file is world-readable — `namei -l` finds the blocking directory.

## Change, narrowly
```bash
sudo chown alice:finance report.csv
chmod 640 report.csv          # rw- r-- ---
chmod g+w shared-dir; chmod g+s shared-dir   # setgid: new files inherit the group
sudo usermod -aG finance bob  # -a or you REPLACE all groups
```
Group changes apply at next login (or `newgrp finance` in that shell).
Shared folders: setgid directory + `umask 002` for collaborators.

## ACLs for one-off access
```bash
setfacl -m u:bob:rX /srv/share/finance        # X = execute only on dirs
setfacl -d -m g:audit:rX /srv/share/finance   # default for new files
getfacl /srv/share/finance
```
`+` at the end of `ls -l` mode string means ACLs exist.

## sudo
- Check: `sudo -l -U alice`.
- Grant scoped rights with a drop-in, always via visudo (syntax checked):
  ```bash
  sudo visudo -f /etc/sudoers.d/helpdesk-printers
  # %helpdesk ALL=(root) /usr/sbin/lpadmin, /usr/bin/systemctl restart cups
  ```
- Full admin: add to `sudo` (Debian/Ubuntu) or `wheel` (Fedora/RHEL) group.
- Broken sudoers file locks everyone out of sudo — recover with
  `pkexec visudo` or single-user/recovery mode.

## Gotchas
- `chmod -R 777` exposes data and breaks tools that refuse world-writable
  files (ssh keys must be 600, `~/.ssh` 700).
- SELinux (Fedora/RHEL) denials look like permission errors: check
  `ausearch -m avc -ts recent`; fix context with `restorecon -Rv`.
- Network shares (CIFS/NFS) map permissions at mount time — `chmod` on the
  client may do nothing.

## Verify
The user performs the action without sudo (or with the scoped sudo only),
`namei -l` shows the expected modes, and no world-writable bits were added.
