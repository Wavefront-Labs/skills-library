---
id: computing-software.systems-network-administration.bash.environment-d-and-pam-env
name: environment-d-and-pam-env
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, environment-d, pam-env, etc-environment, pam-env-conf, systemd-environment-generator, user-environment, session-environment, gui-environment, shell-environment, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Set environment variables outside shell rc files: /etc/environment and pam_env, systemd environment.d for user services, and systemctl set-environment."
sources:
  - https://man7.org/linux/man-pages/man8/pam_env.8.html
  - https://www.freedesktop.org/software/systemd/man/latest/environment.d.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.environment-generator.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# environment.d and pam_env — variables for sessions that never run a shell rc

**Goal:** make a variable visible to ssh commands, cron, GUI applications and user systemd
services, where `~/.bashrc` is never read.

## 1. /etc/environment (pam_env) — every PAM login
```
# /etc/environment  — KEY=VALUE only; no export, no $expansion, no quotes needed (quotes become literal in some versions)
LANG=en_US.UTF-8
http_proxy=http://proxy.example:3128
JAVA_HOME=/usr/lib/jvm/java-17
```
- Read by `pam_env.so` in `/etc/pam.d/{login,sshd,gdm,su,...}` (distro PAM stack names vary). Applies to ssh sessions (including
  `ssh host cmd`), console logins, display managers — it does not apply to system services.
- Changes need a new login. No expansion means `PATH=$PATH:/x` is literal — do PATH in profile.d.

## 2. /etc/security/pam_env.conf — with expansion (legacy)
```
PATH   DEFAULT=/usr/local/bin:/usr/bin:/bin  OVERRIDE=
EDITOR DEFAULT=vim
```
Supports `${VAR}` and `@{HOME}`; `user_readenv` (`~/.pam_environment`) is an optional pam_env feature: see pam_env(8) for your version before relying on it.

## 3. systemd user sessions: environment.d
```
# ~/.config/environment.d/10-tools.conf   (or /etc/environment.d/*.conf system-wide for users)
PATH=$HOME/.local/bin:$PATH
SSH_AUTH_SOCK=$XDG_RUNTIME_DIR/gcr/ssh
MOZ_ENABLE_WAYLAND=1
```
- Parsed by `systemd-environment-d-generator` for the **user manager** (`systemd --user`):
  user services, timers, and GUI apps launched by GNOME/KDE on Wayland get these.
- `$VAR` expansion is supported; order is lexicographic across both dirs.
- Inspect: `systemctl --user show-environment`.
- Not seen by terminal shells unless the desktop imports it; shells still read profile files.

## 4. Runtime changes
```bash
systemctl --user set-environment FOO=bar      # user manager; services started afterwards see it
systemctl --user import-environment PATH DISPLAY WAYLAND_DISPLAY   # from current shell into the manager
systemctl set-environment http_proxy=...      # system manager (pid 1) — affects services started later
systemctl show-environment
```
For a specific service use `Environment=`/`EnvironmentFile=` in the unit instead; manager
environment is global and easy to forget.

## 5. Choosing the mechanism
| need | put it in |
|---|---|
| proxies/locale for ssh + console logins | `/etc/environment` |
| PATH or anything needing expansion for shells | `/etc/profile.d/*.sh` |
| GUI apps and `systemctl --user` services | `~/.config/environment.d/` |
| one system service | unit `Environment=` |

## Failure modes
- Variable set in `/etc/environment` but missing in `ssh host cmd`: the PAM stack for sshd may not load `pam_env`, or quoting put literal quotes in the value.
- `environment.d` change has no effect: the user manager has not re-read it (log out and in), or the session did not start through the systemd user manager.
- `systemctl set-environment` lost after reboot: it is runtime-only; persist in a file.
- Do not put secrets in `/etc/environment`; use a secret store or a restricted `EnvironmentFile=`.

## Verify
- [ ] `ssh host env | grep VAR` shows the pam_env value without logging in interactively.
- [ ] `systemctl --user show-environment | grep VAR` shows the environment.d value after re-login.

## Checked
2026-11-02: confirmed against pam_env(8) (/etc/environment KEY=VAL file, pam_env.conf DEFAULT/OVERRIDE, user_readenv) and environment.d(5) / systemd-environment-d-generator (paths, lexicographic order, ${VAR} expansion). Removed: RHEL cron claim, pam 1.5 removal claim, distro stack names, daemon-reload behaviour, GUI-launch remarks.
Method: documentation only; no commands were run.
