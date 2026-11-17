---
id: computing-software.systems-network-administration.linux.fix-setlocale-and-locale-warnings
name: fix-setlocale-and-locale-warnings
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, locale-errors, setlocale, lc-all, locale-gen, sendenv-lc, c-utf-8]
level: practitioner
status: docs-checked
description: "Fix setlocale: LC_ALL cannot change locale and perl/bash locale warnings: generate missing locales, SSH SendEnv/AcceptEnv forwarding, containers and C.UTF-8 defaults."
sources:
  - https://wiki.debian.org/Locale
  - https://man7.org/linux/man-pages/man7/locale.7.html
  - https://man.openbsd.org/ssh_config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fix setlocale/locale warnings

Typical messages:
```
-bash: warning: setlocale: LC_ALL: cannot change locale (en_GB.UTF-8)
perl: warning: Setting locale failed. ... LANG = "en_US.UTF-8" are supported and installed on your system.
locale: Cannot set LC_CTYPE to default locale: No such file or directory
```
They all mean: the process environment asks for a locale that isn't compiled on **this** machine.

## Diagnose
```bash
locale                 # what the environment requests (and errors for missing ones)
locale -a              # what is actually available
env | grep -E '^(LANG|LC_|LANGUAGE)'
cat /etc/locale.conf /etc/default/locale 2>/dev/null   # system default
```

## The common cause: SSH forwards your laptop's locale
OpenSSH clients can send variables listed in `SendEnv` (distributions commonly ship `SendEnv LANG LC_*` in `/etc/ssh/ssh_config`) and servers copy those allowed by `AcceptEnv` in `sshd_config`. A laptop with `en_GB.UTF-8` can land on a server that only has `en_US.UTF-8`.
Fixes (pick one):
- Generate the locale on the server (below) - friendliest.
- Client: remove `SendEnv LANG LC_*` from your ssh config, or `Host *` + `SetEnv LC_ALL=C.UTF-8`.
- Server: drop `AcceptEnv` in sshd_config (affects everyone).

## Generate locales
```bash
# Debian/Ubuntu
sed -i 's/^# *\(en_GB.UTF-8\)/\1/' /etc/locale.gen && locale-gen
dpkg-reconfigure locales                       # interactive
# RHEL/Fedora
dnf install glibc-langpack-en                  # or glibc-all-langpacks
localectl set-locale LANG=en_GB.UTF-8
# Arch
uncomment in /etc/locale.gen; locale-gen
```

## Containers and minimal images
- Many images only have `C`, `C.UTF-8` (an installed locale since glibc 2.35) and `POSIX`. Set `ENV LANG=C.UTF-8` in the Dockerfile rather than a country locale.
- Debian-based images: install the `locales` package, uncomment the locale in `/etc/locale.gen` and run `locale-gen`.

## Don't
- Don't set `LC_ALL` system-wide in `/etc/environment`; it overrides every category and user preference. Use `LANG` and specific `LC_*`.

## Verify
- [ ] `locale` prints no errors in a fresh SSH session.

## Checked
2026-10-27. Checked against man-pages locale(7), glibc NEWS for 2.35 (C.UTF-8 added and not built in, must be installed), Debian Locale wiki (SendEnv and AcceptEnv LANG LC_*, dpkg-reconfigure locales, manual /etc/locale.gen plus locale-gen), Debian locale-gen(8), systemd localectl(1), and OpenSSH ssh_config(5) with SetEnv and the dash clearing of SendEnv. Removed: update-locale, the Alpine remark, the PERL_BADLANG and Python encoding remarks and the cron claim, which the documentation does not cover. The Debian wiki and the OpenSSH page replace the OpenBSD anchor link in sources.

Method: documentation only; no commands were run.
