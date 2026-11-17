---
id: computing-software.systems-network-administration.bash.profile-d-system-wide-shell-settings
name: profile-d-system-wide-shell-settings
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, profile-d, etc-profile-d, etc-profile, etc-bashrc, bash-bashrc, system-wide-environment, proxy-environment, umask-default, shell-environment, configuration-management, lpic-1, sysadmin]
level: practitioner
status: draft
description: "Set shell environment for every user with /etc/profile.d/*.sh: ordering, sh-compatible syntax, re-source guards, csh twins, and proxy/umask/EDITOR examples."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files
  - https://wiki.debian.org/EnvironmentVariables
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# /etc/profile.d — system-wide shell settings that survive upgrades

**Goal:** apply PATH, proxies, locale, editor and umask defaults to every login shell on a
host without editing `/etc/profile` (which the package manager owns).

## 1. How it is wired
`/etc/profile` ends with a loop like:
```sh
for i in /etc/profile.d/*.sh; do [ -r "$i" ] && . "$i"; done
```
- Only `*.sh` (and `*.csh` for tcsh users) are sourced, **alphabetically** — name files
  `10-proxy.sh`, `50-tools.sh` if order matters.
- Sourced by **login** shells of every POSIX shell (`bash -l`, `sh -l`, `dash` login,
  `zsh` via `/etc/zprofile` on some distros). Not by interactive non-login shells
  (new terminal tabs) unless the distro's `/etc/bashrc` also sources them — RHEL does,
  Debian does not. Put interactive-only settings (aliases, PS1) in `/etc/bash.bashrc`
  (Debian) or `/etc/bashrc` (RHEL) instead, or guard them in profile.d with `[ -n "$PS1" ]`.

## 2. Writing a safe file
```sh
# /etc/profile.d/50-site.sh  — POSIX sh syntax ONLY: no [[ ]], arrays, or bashisms (dash reads it)
export EDITOR=vim
export LESS=-R
export http_proxy=http://proxy.example:3128 https_proxy=http://proxy.example:3128
export no_proxy=localhost,127.0.0.1,.example
case ":$PATH:" in *:/opt/tools/bin:*) ;; *) PATH="/opt/tools/bin:$PATH" ;; esac
umask 027                       # applies to interactive sessions; services take theirs from systemd/pam
[ -n "$PS1" ] && alias ll='ls -alF'   # interactive only
```
- No `exit`/`return` at top level that could abort `/etc/profile`; no commands that can
  fail loudly or hang (network checks, `ssh-agent`).
- Mode 0644, owner root. Not executable (they are sourced).
- Test: `sh -n /etc/profile.d/50-site.sh` (dash: `dash -n`), then `bash -lc 'echo $EDITOR'`.

## 3. Companion locations
- `/etc/environment`: `KEY=value` lines read by pam_env for *all* PAM sessions (ssh, cron on
  some distros, GUI) — no shell expansion, no `export`. Good for proxies and locale.
- `/etc/locale.conf` (RHEL) / `/etc/default/locale` (Debian): LANG, read by systemd/pam.
- `~/.config/environment.d/*.conf`: per-user, systemd user sessions (GUI apps).
- `/etc/sudoers` `env_keep += "http_proxy https_proxy no_proxy"` so `sudo dnf` sees the proxy.

## 4. Package-provided examples worth knowing
`/etc/profile.d/lang.sh` (RHEL locale), `bash_completion.sh`, `vte.sh` (terminal cwd
tracking), `which2.sh`, `sh.local` (RHEL's blessed place for local changes), `gawk.sh`.
Do not edit package files; add your own numbered file.

## 5. Configuration management
Deploy with Ansible `copy`/`template` to `/etc/profile.d/`, `mode: '0644'`; no handler
needed (next login picks it up). Remove = delete the file.

## Failure modes
- Setting missing in a new terminal tab (Debian): non-login shell; use `/etc/bash.bashrc`
  or configure the terminal to run login shells.
- `/etc/profile.d/x.sh: line N: syntax error` on every login: bashism in a file that
  dash/sh also reads — stick to POSIX.
- Proxy set for users but `sudo apt` ignores it: `env_reset`; add `env_keep`.
- Variables doubled in PATH: no guard; or both `profile.d` and `~/.bashrc` add them.
- Changes not seen by services: they never read profile files — use unit `Environment=`.

## Verify
- [ ] `ssh host 'bash -lc "echo \$EDITOR \$PATH"'` shows the values for a fresh login.
- [ ] `dash -lc 'echo $EDITOR'` (Debian) works — proves POSIX compatibility.
