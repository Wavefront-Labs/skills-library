---
id: computing-software.systems-network-administration.linux.doas-minimal-sudo-alternative
name: doas-minimal-sudo-alternative
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, doas, opendoas, privilege-escalation, sudo-alternative, doas-conf]
level: practitioner
status: docs-checked
description: "Replace or complement sudo with doas (OpenDoas): doas.conf rule syntax, persist, nopass, keepenv, PAM, validating config and safe rollout without locking yourself out."
sources:
  - https://github.com/Duncaen/OpenDoas/blob/master/doas.conf.5
  - https://github.com/Duncaen/OpenDoas/blob/master/doas.1
  - https://github.com/Duncaen/OpenDoas/blob/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# doas as a minimal sudo alternative

**Goal:** a tiny, auditable privilege-escalation tool for hosts that don't need sudo's policy engine (containers, Alpine, Arch desktops, appliances).

## Install
Install your distribution's OpenDoas package or build it from source (https://github.com/Duncaen/OpenDoas). The binary is
installed setuid root; the config file is `doas.conf` in the build's `--sysconfdir` (default `/etc`).

## Rule syntax
`permit|deny [options] identity [as target] [cmd command [args ...]]` - **last matching rule wins**.
```
# admins: persist = do not ask again for some time (needs --with-timestamp)
permit persist keepenv :wheel
# backup user may run exactly one command as root, no password
permit nopass backup as root cmd /usr/bin/rsync args -a --delete /srv/ /mnt/backup/
# explicit deny placed AFTER the broad permit wins
deny alice as root cmd /bin/sh
```
- `:group` prefix for groups; numeric IDs are accepted. Omitting `as` allows any target user (the default target when running is root); omitting `cmd` allows all commands; no rule matching means denied.
- `persist` is disabled unless OpenDoas was built with `--with-timestamp`; `nopass` skips authentication; `nolog` skips success logging.
- `args` with nothing after it means "no arguments allowed"; omitting `args` allows any.
- `setenv { PATH=/usr/sbin:/usr/bin }` sets or keeps listed variables (`-NAME` removes one); `keepenv` retains variables other than those doas(1) lists, so it is risky.
- Use absolute paths for `cmd`; a relative path is searched only in a restricted PATH.

## Validate before you rely on it
```bash
doas -C /etc/doas.conf && echo ok                    # parse and check the file
doas -C /etc/doas.conf rsync -a --delete /srv/ /mnt/backup/   # prints permit, permit nopass or deny for that command
```
Keep a root shell open while testing; never remove sudo until `doas -C` and a real `doas id` succeed for the admin account.

## Differences from sudo that bite
- Options are only `-L`, `-n`, `-s`, `-C config` and `-u user`; there is no `sudo -i` or `-E` equivalent (`-s` runs the shell from `SHELL`).
- The rule grammar has no host matching, no directory-sourced rules and no I/O logging; `nolog` is the only logging control.
- Scripts that call `sudo` with other flags break when `sudo` is aliased to doas.
- PAM: OpenDoas does not ship PAM configuration; its README suggests starting from the distribution's sudo PAM file.

## Verify
- [ ] `doas -C` reports `permit` for intended commands and `deny` for others.
- [ ] A user without a matching rule is refused.

## Checked
Checked 2026-10-25 against the OpenDoas repository (master; last commit 2024-06) doas.conf(5), doas(1), README and configure script.
Confirmed: rule grammar and options (nopass, nolog, persist, keepenv, setenv), `:group` identity, `as` and `cmd` defaults, bare `args` meaning no arguments, last-match-wins and default deny, `-C` output (permit, permit nopass, deny), `-L`, `-n`, `-s`, `-u`, persist built only with `--with-timestamp`, default sysconfdir /etc, PAM configuration not shipped.
Removed as unconfirmed: distribution install commands, the 5-minute persist time, the trailing-newline claim, file mode advice, the error message text and the sudo-symlink flag compatibility.

Method: documentation only; no commands were run.
