---
id: computing-software.systems-network-administration.bash.bashrc-profile-and-login-shell-order
name: bashrc-profile-and-login-shell-order
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, bashrc, bash-profile, profile, login-shell, interactive-shell, non-interactive, bash-logout, bash-env, startup-files, shell-environment, ssh-environment, cron-environment, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Know which bash startup file runs when: login vs interactive vs non-interactive shells, the profile/bashrc chain, BASH_ENV, and the sshd case."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files
  - https://man7.org/linux/man-pages/man1/bash.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bash startup files — why your alias works in a terminal but not over ssh

**Goal:** put each setting in the file that runs for the shells that need it, and diagnose
"it works here but not there" in one look.

## 1. The decision tree
| shell type | reads |
|---|---|
| **login** interactive, or non-interactive with `--login` | `/etc/profile`, then the first readable of `~/.bash_profile`, `~/.bash_login`, `~/.profile`; on exit `~/.bash_logout` |
| **interactive non-login** (new terminal tab, `bash`) | `~/.bashrc` |
| **non-interactive** (`bash script.sh`) | the file named by `$BASH_ENV`, if set |
| **non-interactive, stdin on a network connection** (rshd, sshd) | `~/.bashrc`, if readable (not when invoked as `sh`) |
| invoked as `sh` | login: `/etc/profile`, `~/.profile`; interactive non-login: the file named by `$ENV` |

`--noprofile` skips the login files, `--norc` skips `~/.bashrc`, `--rcfile file` uses another
file in place of `~/.bashrc`. Because login shells do not read `~/.bashrc`, a common pattern
is for `~/.bash_profile` to source it:
```bash
# ~/.bash_profile
[[ -f ~/.bashrc ]] && . ~/.bashrc
```

## 2. Where things go
- **Environment variables, PATH additions** go in the login files (read once per login,
  inherited by children).
- **Aliases, functions, prompt, shopt, completion** go in `~/.bashrc` (read by each
  interactive non-login shell; not inherited).
- Guard `~/.bashrc` so non-interactive shells that read it (the sshd case above) do nothing
  noisy: test `$-` for `i` and return early. Output from `.bashrc` can break file-transfer
  tools that run over ssh.

## 3. Diagnosing
```bash
shopt login_shell  # on = login shell
echo $-            # contains i = interactive
bash --noprofile --norc   # clean shell to reproduce a problem
bash --rcfile file        # test a replacement rc file
```

## 4. Special cases
- **BASH_ENV**: set it in the environment to have non-interactive bash scripts source a file.
- Aliases are expanded only in interactive shells by default, so scripts and `ssh host cmd`
  do not see your aliases; put the logic in a script on the PATH.

## 5. Hygiene
- Keep `.bashrc` fast: every new interactive shell pays for it.
- Guard PATH additions so nested shells do not grow PATH repeatedly.

## Failure modes
- Changes in `.bash_profile` not applied in new tabs: tabs are non-login; use `.bashrc` or start a login shell.
- Login shell ignores `.bashrc`: the sourcing line in `.bash_profile` is missing, or
  `~/.bash_login` exists and shadows `~/.profile` (only the first found is read, and `~/.bash_profile` wins over both).

## Verify
- [ ] `bash -lic 'type myalias'` and `bash -ic 'type myalias'` both succeed; `bash -c 'type myalias'` fails (expected).

## Checked
2026-11-01: confirmed against the Bash Reference Manual (Bash Startup Files) and the bash man page: login, interactive, non-interactive and sshd/rshd startup behaviour, `sh` invocation, `--noprofile`, `--norc`, `--rcfile`, `BASH_ENV`, `shopt login_shell`, `$-`. Removed: distro-specific file names, `/etc/profile.d`, pam_env, sshd and cron options, sudo/su and systemd behaviour.
Method: documentation only; no commands were run.
