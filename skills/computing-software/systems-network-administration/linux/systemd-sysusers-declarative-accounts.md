---
id: computing-software.systems-network-administration.linux.systemd-sysusers-declarative-accounts
name: systemd-sysusers-declarative-accounts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysusers-d, systemd-sysusers, system-account, service-users, dynamicuser, packaging]
level: practitioner
status: docs-checked
description: "Declare system users and groups with sysusers.d instead of useradd in scripts: syntax, fixed IDs and ranges, systemd-sysusers, and DynamicUser."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/sysusers.d.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-sysusers.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#DynamicUser=
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sysusers.d

**Why:** idempotent, declarative service accounts that packages, image builds and `systemd-sysusers` create
consistently at package installation or boot time.

## Syntax (`/etc/sysusers.d/myapp.conf` or `/usr/lib/sysusers.d/` for packages)
```
#Type Name    ID             GECOS              Home           Shell
u     myapp   -              "MyApp daemon"     /var/lib/myapp /usr/sbin/nologin
u     backup  950:950        "Backup agent"     -              -
g     myappdata -
m     myapp   myappdata                         # add user to group
r     -       900-949                           # range used for dynamically allocated IDs
u!    locked  -              "Locked account"                  # '!' = fully locked account
```
`ID` `-` = allocate a free system ID; `950:950` fixed UID:GID; `950:myappdata` primary group by name; a path = take the ID from that file's owner.

## Apply
```bash
systemd-sysusers                          # all configs
systemd-sysusers /etc/sysusers.d/myapp.conf
getent passwd myapp
```
Packages normally ship their file in `/usr/lib/sysusers.d/`.

## Alternative: DynamicUser=
For services that need no persistent identity: `DynamicUser=yes` + `StateDirectory=myapp` — UID allocated at start. No account management at all.

## Gotchas
- Fixed IDs must be unique across the fleet if files are shared (NFS) — document them.

## Verify
- [ ] `systemd-sysusers` run twice reports nothing new; `id myapp` shows the expected groups.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: line types u, u!, g, m and r and their field order, `-` for automatic IDs, `uid:gid` and `uid:groupname` forms, an ID taken from a file owner, and `u!` creating a fully locked account (`sysusers.d`); `systemd-sysusers` takes config files; `DynamicUser=` with `StateDirectory=` (`systemd.exec`). Removed the `--cat-config` option (not in the `systemd-sysusers` man page), the distro packaging helpers, the `/var/lib/private` path, the 252 version gate and the home-directory remark because no documentation confirmed them.

Method: documentation only; no commands were run.
