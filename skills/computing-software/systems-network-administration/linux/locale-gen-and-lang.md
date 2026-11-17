---
id: computing-software.systems-network-administration.linux.locale-gen-and-lang
name: locale-gen-and-lang
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, locale, locale-gen, lang, lc-all, localectl, glibc-langpack, utf-8, localisation, i18n, ssh-sendenv, sysadmin]
level: practitioner
status: docs-checked
description: "Set system and user locales on Linux: generating locales (locale-gen, glibc-langpack), LANG vs LC_* vs LC_ALL, localectl, SSH-forwarded locales, and fixing 'cannot set LC_ALL' warnings."
sources:
  - https://man7.org/linux/man-pages/man7/locale.7.html
  - https://www.freedesktop.org/software/systemd/man/latest/localectl.html
  - https://manpages.debian.org/stable/locales/locale-gen.8.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locales: locale-gen and LANG

**Goal:** every program sees a valid UTF-8 locale, sorting/number/date formats are what
users expect, and SSH sessions stop printing locale warnings.

## 1. Variables and precedence
`LC_ALL` (overrides everything; debugging only) > individual `LC_*` (`LC_TIME`, `LC_NUMERIC`,
`LC_COLLATE`, `LC_MONETARY`, `LC_MESSAGES`, ...) > `LANG` (default for all).
`C.UTF-8` (provided by glibc 2.35 and later, installed with the locale files) and `C` are the neutral locales for scripts and servers.
```bash
locale              # effective values (quoted = inherited from LANG)
locale -a           # locales actually available
```

## 2. Make a locale available
Debian/Ubuntu (compiled locales):
```bash
sed -i 's/^# *\(en_GB.UTF-8\)/\1/' /etc/locale.gen && locale-gen
# or: dpkg-reconfigure locales     (interactive)
```
RHEL/Fedora (packaged):
```bash
dnf install glibc-langpack-en      # or glibc-all-langpacks
```
Arch: uncomment in `/etc/locale.gen`, run `locale-gen`.

## 3. Set the system default
```bash
localectl set-locale LANG=en_GB.UTF-8
localectl set-locale LANG=en_GB.UTF-8 LC_TIME=C.UTF-8   # e.g. ISO-ish dates in logs
localectl status
```
Writes `/etc/locale.conf` (systemd locale.conf(5)); Debian and Ubuntu read their system default from `/etc/default/locale`. Applies to
new logins and services started afterwards. Per user: `export LANG=...` in `~/.bashrc`.

## 4. SSH sessions
`SendEnv LANG LC_*` (client `ssh_config`) + `AcceptEnv LANG LC_*` (server) forward your laptop's locale.
If the server lacks it: `warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)` / perl
"Setting locale failed". Fix by generating that locale on the server, or stop forwarding (a `-` prefix such as `SendEnv -LC_*` clears earlier SendEnv patterns / remove `AcceptEnv`).

## Gotchas
- Scripts parsing command output should set `LC_ALL=C` — `sort`, `ls`, decimal separators (`1,5` vs `1.5`) and messages change with locale.
- Containers usually have only `C`/`C.UTF-8`; set `LANG=C.UTF-8` in the image rather than installing all locales.

## Verify
- [ ] `locale` shows no errors and the intended values; `locale -a` includes them.
- [ ] A fresh SSH login prints no locale warnings; `date` and `printf "%'d\n" 1234567` format as expected.

## Checked
2026-10-27. Checked against man-pages locale(7) and locale(1) (man-pages 5.12 mirror, 2021-03-22), systemd localectl(1) and locale.conf(5), glibc NEWS for 2.35, Debian locale-gen(8) and the Debian Locale wiki, and OpenSSH ssh_config(5) and sshd_config(5). Confirmed: LC_ALL overrides the other variables; locale -a lists available locales and locale prints inherited values quoted; localectl and /etc/locale.conf; locale-gen reads /etc/locale.gen and dpkg-reconfigure locales exists; C.UTF-8 was added in glibc 2.35 and must be installed; SendEnv, AcceptEnv and the leading dash to clear SendEnv patterns; glibc-langpack package names are as stated by the vendor and were not rechecked. Removed: locale-gen with arguments on Ubuntu, the ~/.config/locale.conf path, the en_US codeset remark and the Python and Java encoding remark, which the documentation does not cover.

Method: documentation only; no commands were run.
