---
id: computing-software.systems-network-administration.linux.gpasswd-newgrp-and-group-membership
name: gpasswd-newgrp-and-group-membership
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, gpasswd, newgrp, group-membership, usermod-ag, sg, supplementary-groups, group-admin, rhcsa, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Manage group membership correctly: usermod -aG vs -G, gpasswd add/remove/set and group admins, why changes need a new login, and newgrp/sg to use a new group immediately."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/gpasswd.1.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/newgrp.1.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/usermod.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/sg.1.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# gpasswd, newgrp and group membership

**Goal:** add and remove people from groups without wiping their other memberships, delegate
membership management, and have the change take effect.

## 1. Add/remove
```bash
usermod -aG docker,wheel alice      # APPEND to supplementary groups
usermod -G docker alice             # REPLACES all supplementary groups with just docker — classic mistake
gpasswd -a alice docker             # add one user to one group
gpasswd -d alice docker             # remove from one group
gpasswd -M alice,bob,carol devs     # set the full member list
getent group devs
```

## 2. Delegate
```bash
gpasswd -A teamlead devs            # teamlead can now run gpasswd -a/-d for devs without root
```
Group passwords (`gpasswd devs` with no option) let non-members `newgrp devs` with the
password while members need none — rarely a good idea; `gpasswd -r devs` removes the password and `-R` sets the password field to `!` so only members can use `newgrp` into the group.

## 3. When does it take effect?
Group list is read at login and inherited by processes. After adding alice to `docker`:
- Existing shells/sessions **don't** have it (`id` shows it from the DB; `id -Gn` in the
  shell shows the process's groups — compare). New SSH login: yes.
- Use it now without logging out:
```bash
newgrp docker            # starts a NEW shell with docker as primary group (exit to return)
sg docker -c 'docker ps' # run one command with that group
```
- Long-running services must be restarted to pick up new groups (e.g. after adding `www-data`
  to `ssl-cert`).
- systemd user sessions/GUI: full logout/login (or reboot) needed.

## 4. Primary vs supplementary
Primary group (`passwd` GID field) owns newly created files; change with `usermod -g devs alice`.
Setgid directories (`chmod g+s`) are usually better for shared folders than changing primary
groups.

## Gotchas
- `gpasswd GROUP` (set a password) fails with `Not a tty` when stdin is not a terminal.
- `usermod -G` without `-a` silently drops `wheel`/`sudo` → user loses admin rights.
- Central directory groups (LDAP/AD) are managed there; local gpasswd changes only `/etc/group`.

## Verify
- [ ] `getent group devs` lists the intended members.
- [ ] In a fresh login `id -nG` includes the group; access to a group-owned resource works.

## Checked

2026-10-26. shadow-maint/shadow master (last commit 2026-10-20, release 4.20.3): gpasswd -a, -d, -M, -A, -r, -R and group password behaviour; newgrp changes the real group ID and starts a new shell, password rules for members and non-members; usermod -G replaces the supplementary list and -a appends; sg exists as a separate command. Removed the groupmems line (no man page found in the repository), the 65536 supplementary-group figure and the NFS 16-group claim, which were not confirmed.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (shadow 4.17.4): usermod -G replacing and -aG appending, gpasswd -a/-d/-M/-A (group admin recorded in /etc/gshadow and allowed to add to its own group but refused on another), gpasswd -r and -R changing the gshadow password field, newgrp and sg giving the group as primary, usermod -g. Not run: setting a group password (gpasswd needs a terminal), contrast between a stale session's id and the database, services picking up new groups.
