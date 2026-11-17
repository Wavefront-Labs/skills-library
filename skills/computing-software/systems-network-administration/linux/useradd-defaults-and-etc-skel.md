---
id: computing-software.systems-network-administration.linux.useradd-defaults-and-etc-skel
name: useradd-defaults-and-etc-skel
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, useradd, useradd-defaults, etc-default-useradd, skel, etc-skel, home-directory, user-provisioning, rhcsa, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Control what every new account gets: useradd -D and /etc/default/useradd (shell, home base, inactive, groups), /etc/skel contents, and how adduser on Debian differs."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/useradd.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/login.defs.5.xml
  - https://manpages.debian.org/trixie/adduser/adduser.conf.5.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# useradd defaults and /etc/skel

**Goal:** new accounts are created consistently — right shell, home location, default
groups, starter dotfiles — without remembering a long useradd line.

## 1. Where defaults come from
- `/etc/default/useradd` — `useradd -D` shows it (newer shadow also prints `GROUPS`, `USRSKEL` and `LOG_INIT`); `-D` with `-b`, `-e`, `-f`, `-g` or `-s` updates
  `HOME` (base dir), `EXPIRE`, `INACTIVE`, `GROUP`, `SHELL`. The file also holds `SKEL` and `CREATE_MAIL_SPOOL`.
- `/etc/login.defs` — UID/GID ranges, `CREATE_HOME`, `UMASK`/`HOME_MODE`, `USERGROUPS_ENAB`,
  password aging defaults, `ENCRYPT_METHOD`.
- Command-line options override both.
```bash
useradd -D                                 # show
useradd -D -s /bin/bash                    # set default shell
useradd -D -b /srv/home                    # home base directory
useradd -D -f 30                           # disable account 30 days after password expiry (INACTIVE)
useradd -D -e 2027-12-31                   # default account expiry date
```
`HOME_MODE` (login.defs) sets the mode of new home directories made by useradd and newusers; if it
is unset, `UMASK` is used. For example `HOME_MODE 0700` makes new homes private. Debian's `adduser`
uses `DIR_MODE` (default 0700) instead. Check the value your distribution ships.

## 2. /etc/skel
Copied into each new home **at creation only**:
```bash
ls -la /etc/skel                 # .bashrc .bash_profile .bash_logout …
install -d -m 700 /etc/skel/.ssh
cp company-bashrc-additions /etc/skel/.bashrc.d/10-company.sh   # if your .bashrc sources ~/.bashrc.d
useradd -m -k /etc/skel-contractors -s /bin/bash contractor1    # alternative skeleton per user type
```
Existing users don't receive later skel changes — push those with config management or
`/etc/profile.d/` (system-wide) instead. Ownership is set to the new user automatically.

## 3. A full creation
```bash
useradd -m -c "Alice Ops" -G wheel,adm -s /bin/bash alice     # use a group that exists on your system
passwd alice    ||    chage -d 0 alice   # force password change at first login
id alice; ls -la ~alice
```
Debian/Ubuntu `adduser` is a friendlier Perl wrapper with its own config
(`/etc/adduser.conf`: `DSHELL` (default `/bin/bash`), `DHOME` (`/home`), `SKEL` (`/etc/skel`), `DIR_MODE` (`0700`),
`EXTRA_GROUPS` (`users`), `ADD_EXTRA_GROUPS`; non-zero adds new users to `EXTRA_GROUPS`). In Debian 13 `/etc/adduser.conf` holds only commented examples and a plain `adduser` user was still put in group `users` (gid 100), so check `id` on a test user.
`useradd` creates the home only with `-m` or `CREATE_HOME yes`; `-k` is only valid together with `-m`.

## Gotchas
- `useradd -D -g` sets `GROUP`, which is used only when `USERGROUPS_ENAB` is `no` (or `-N` is given); with `yes` (or `-U`) each user gets a private group.
- System accounts: `useradd -r` uses the `SYS_UID_MIN`-`SYS_UID_MAX` range, creates no home even when `CREATE_HOME` is `yes` (an explicit `-m` still creates one), and leaves the aging fields empty (the last-change date is still set).
- `-m` and `-M` together are refused; Debian 13 ships `HOME_MODE 0700` and no `CREATE_HOME`, so `useradd` without `-m` makes no home.
- Homes on NFS/automount: `-M` skips home creation even when `CREATE_HOME` is `yes`.

## Verify
- [ ] `useradd -D` shows the intended defaults.
- [ ] A test user gets the expected shell, groups, home mode (`stat -c %a`) and skel files.

## Checked

2026-10-26. shadow-utils man pages from the shadow-maint/shadow repository (master, commit of 2026-10-20, release 4.20.3): useradd -D options and the variables they set, -k only with -m, -M, -r behaviour, USERGROUPS_ENAB and GROUP, HOME_MODE and UMASK in login.defs. Debian adduser.conf(5) for trixie: DSHELL, DHOME, SKEL, DIR_MODE, EXTRA_GROUPS and ADD_EXTRA_GROUPS with defaults. Removed unconfirmed per-distribution defaults and the pam_mkhomedir remark.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (shadow 4.17.4, adduser 3.152): useradd -D and its rewrite of /etc/default/useradd by -s/-b/-f/-e/-g, home modes from HOME_MODE (Debian ships `HOME_MODE 0700`) and UMASK when it is unset (755), -k without -m refused, -m with -M refused, CREATE_HOME yes with and without -M and -r, -N and -U with GROUP, /etc/skel copied at creation only (including a 700 .ssh), later skel changes not reaching existing homes, chage -d 0, adduser home mode 700. Not run: -D -g effect on USERGROUPS_ENAB no, NFS homes, per-user-type skeleton directories beyond -k /etc/skel.
