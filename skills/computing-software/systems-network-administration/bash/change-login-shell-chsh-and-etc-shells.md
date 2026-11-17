---
id: computing-software.systems-network-administration.bash.change-login-shell-chsh-and-etc-shells
name: change-login-shell-chsh-and-etc-shells
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, chsh, etc-shells, login-shell, usermod-shell, zsh, nologin]
level: intro
status: docs-checked
description: "Change a user's login shell with chsh or usermod -s, how /etc/shells gates chsh and some FTP daemons, and safe testing before switching a shell."
sources:
  - https://man7.org/linux/man-pages/man1/chsh.1.html
  - https://man7.org/linux/man-pages/man5/shells.5.html
  - https://man7.org/linux/man-pages/man8/usermod.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing login shells

## Commands
```bash
cat /etc/shells                       # valid login shells
chsh -l                               # same list (util-linux)
chsh -s /usr/bin/zsh                  # own shell
usermod -s /bin/bash alice            # as root: set another user's login shell
```

## What /etc/shells controls
- `/etc/shells` lists the full pathnames of valid login shells and is consulted by `chsh`.
- `chsh` accepts the full path of any executable file, but by default unprivileged users may only choose shells
  listed in `/etc/shells`; for root it issues a warning. It can be compiled to only warn for all users.
- Some programs read the file to decide whether a user is a normal user: FTP daemons traditionally refuse users
  whose shell is not listed.

## Safety
- Test the new shell first (run it by hand from the current session) and keep a root session open when changing
  root's shell; a broken or missing shell locks you out.

## Central accounts
`chsh` supports non-local entries (Kerberos, LDAP) only if linked with libuser; otherwise use the tool for your
directory (the man page names ypchsh and lchsh).

## Verify
- [ ] New login lands in the new shell; the path exists on every host that uses the account.

## Checked
2026-11-01. Confirmed against the chsh(1), shells(5) and usermod(8) man pages (man7.org): `-s`, `-l`, `/etc/shells`
behaviour for unprivileged users and root, FTP daemon note, libuser note. Removed unconfirmed specifics: add-shell,
nologin paths and messages, pam_shells behaviour, SSSD options, sudo/su behaviour.
Method: documentation only; no commands were run.
