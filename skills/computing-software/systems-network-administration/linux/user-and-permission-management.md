---
id: computing-software.systems-network-administration.linux.user-and-permission-management
name: user-and-permission-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users, groups, useradd, usermod, groupadd, passwd, chage, system-account, nologin, permissions, chmod, chown, umask, setgid, sticky-bit, setuid, acl, setfacl, getfacl, default-acl, sudo, sudoers, visudo, sudoers-d, ssh-keys, authorized-keys, shared-directory, least-privilege, selinux-context, sysadmin, suid-audit]
level: practitioner
status: docs-checked
description: "Manage Linux users, groups and file access: system vs login accounts, chmod/umask/setgid shared dirs, POSIX ACLs with defaults, sudoers drop-ins with visudo, and auditing."
sources:
  - https://man7.org/linux/man-pages/man8/useradd.8.html
  - https://man7.org/linux/man-pages/man1/setfacl.1.html
  - https://www.sudo.ws/docs/man/sudoers.man/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Users and permissions: groups grant access, sudo grants power, both get audited

**Goal:** create the right kind of account, give a team a shared directory that stays writable for everyone, delegate
narrow root rights, and be able to prove who can do what.

## 1. Accounts
```bash
useradd -m -s /bin/bash -c "Jane Doe" -G devs <USER>      # human login account
useradd -r -s <NOLOGIN_SHELL> -d /var/lib/myapp myapp      # system/service account
```
- useradd(8) options used: `-m` create the home directory, `-r` system account, `-s` login shell, `-G` supplementary
  groups, `-c` comment, `-d` home directory.
- Whether `useradd` creates a per-user group, the default UMASK and the UID ranges come from `/etc/login.defs`
  (`USERGROUPS_ENAB`, `UMASK`, `UID_MIN`/`UID_MAX`) and differ by distribution. Read the file on the host.
- Directory-backed users (SSSD/LDAP/AD) may not be in `/etc/passwd`: query them with `getent passwd` and `id <USER>`.
- Group membership changes apply at the next login; restart running services.
- For password ageing, locking and leaver offboarding, use the `usermod`, `chage` and `passwd` man pages for your
  distribution, and remember that locking a password does not by itself remove SSH key access.

## 2. Mode bits that matter
`chmod 750 dir` = owner rwx, group r-x, others none. For directories, `x` means "may traverse". `umask` sets defaults
for new files. A setgid directory (`chmod 2775`) makes new files inherit the directory's group, the key to shared team
folders; the sticky bit (`chmod 1777`, as on `/tmp`) stops users deleting others' files. Audit setuid binaries on a
schedule.

## 3. Shared team directory (the pattern)
```bash
groupadd projx
install -d -o root -g projx -m 2770 /srv/projx
setfacl -m g:projx:rwx /srv/projx
setfacl -d -m g:projx:rwx /srv/projx      # default ACL: new files and directories inherit it
setfacl -m g:auditors:rx -R /srv/projx    # read-only extra group
getfacl /srv/projx
```
setfacl(1): `-m` modifies ACL entries, `-x` removes them, `-d` makes the operation apply to the default ACL, and `-R`
recurses. The ACL **mask** limits the effective rights of group and named-user entries, so check it with `getfacl` after
any `chmod`. Without a default ACL, a member's `umask 022` creates files teammates cannot edit.

## 4. sudo, narrowly
Edit sudoers with `visudo`, which syntax-checks before saving. The `@includedir` directive creates a `sudoers.d`
directory for drop-in files; visudo will not edit files in it unless one has a syntax error. Place your rule in a
drop-in file and check it with `visudo`.
```
%webops ALL=(root) /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx
```
- sudoers(5): group commands with `Cmnd_Alias`. Wildcards in command arguments need care; read the section on
  wildcards before using them.
- Use `sudoedit` to grant file edits rather than granting an editor; tags such as `NOEXEC` limit what a permitted
  program can run, but do not rely on them as the only control. Avoid granting shells, editors, interpreters and file
  managers.
- `sudo -l -U <USER>` lists what another user may run (requires the "list" privilege).
- Drop-in file naming and permission requirements: see the `@includedir` section of sudoers(5).

## 5. Audit
- Who is an admin: the group named in sudoers (commonly `sudo` on Debian, `wheel` on RHEL; check the host).
- Extra UID 0 accounts, recent logins and orphaned files: use `getent`, `last` and `find -nouser` according to your
  distribution's tools.
- On SELinux systems, correct modes can still be denied by a wrong context; see `permission-denied-triage`.

## Verify
- [ ] `id <USER>` shows the expected groups after re-login.
- [ ] A file created by user A in the shared directory is editable by user B (default ACL works).
- [ ] `sudo -l -U <USER>` lists only the intended commands.
- [ ] No unexpected UID-0 accounts or new setuid binaries.

## Checked
2026-10-28. Confirmed in useradd(8), setfacl(1) and sudoers(5): the useradd options listed, `login.defs` variables,
`setfacl -m/-x/-d/-R` and the mask, `@includedir`, `Cmnd_Alias`, wildcard caution, `sudoedit`, `NOEXEC` tag,
`sudo -l -U`. Removed as unconfirmed: `usermod -aG` and `-L`/`-e` details, `chage`, `newgrp`, the `find -perm -4000`
and `awk` audit commands, the sudoers.d file-name ignore rule and 0440 mode, GTFOBins reference, `cp -a` and ACL
backup remarks, `nologin` path.
Method: documentation only; no commands were run.
