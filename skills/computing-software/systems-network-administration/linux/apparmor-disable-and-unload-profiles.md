---
id: computing-software.systems-network-administration.linux.apparmor-disable-and-unload-profiles
name: apparmor-disable-and-unload-profiles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apparmor, aa-disable, profile-unload, apparmor-parser, aa-status, complain-mode, disable-directory, ubuntu, debian, security, sysadmin]
level: practitioner
status: docs-checked
description: "Disable or unload a single AppArmor profile safely: aa-disable vs complain mode, apparmor_parser -R, the disable/ directory, re-enabling, and why disabling AppArmor entirely is the wrong fix."
sources:
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-disable.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-enforce.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/utils/aa-complain.pod
  - https://gitlab.com/apparmor/apparmor/-/blob/master/parser/apparmor_parser.pod
  - https://github.com/docker/docs/blob/main/content/manuals/engine/security/apparmor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling and unloading AppArmor profiles

**Goal:** take one misbehaving profile out of the way (temporarily or permanently)
without turning off AppArmor for every other confined service.

## 1. Choose the least drastic option
1. **Complain mode** — still loaded, logs would-be denials, blocks nothing: `aa-complain /etc/apparmor.d/usr.sbin.mysqld`.
   Best for "is AppArmor the cause?" and for collecting rules with `aa-logprof`.
2. **Disable one profile** — unloaded now and not loaded at boot: `aa-disable`.
3. **Unload only until next boot/reload** — `apparmor_parser -R`.
Never `systemctl disable apparmor` or `apparmor=0` on the kernel command line to fix one app.

## 2. Disable a profile
```bash
# install your distribution's AppArmor utilities package first
aa-status                                           # loaded profiles, enforce/complain, confined processes
aa-disable /etc/apparmor.d/usr.sbin.cupsd
# what it does:
#   ln -s /etc/apparmor.d/usr.sbin.cupsd /etc/apparmor.d/disable/
#   apparmor_parser -R /etc/apparmor.d/usr.sbin.cupsd
systemctl restart cups
aa-status | grep cupsd                              # should be gone
```
Manual equivalent when apparmor-utils isn't installed: create that symlink and run `apparmor_parser -R`.

## 3. Re-enable
```bash
aa-enforce /etc/apparmor.d/usr.sbin.cupsd           # removes the disable symlink and loads in enforce mode
# or manually:
rm /etc/apparmor.d/disable/usr.sbin.cupsd
apparmor_parser -r /etc/apparmor.d/usr.sbin.cupsd   # -r = replace/load
```

## 4. Profiles for processes already running
After disabling a profile, restart the service and check `aa-status` to see which profiles and processes are still listed.

## Gotchas
- Package upgrades may ship a new profile but the `disable/` symlink persists — re-check after upgrades whether the reason still applies.
- Disabling a profile often hides a one-line fix in `/etc/apparmor.d/local/<profile>`; prefer that.
- Docker containers run under their own profile (`docker-default`); disabling a host profile does not change it.

## Verify
- [ ] `aa-status` no longer lists the profile; the service works after restart.
- [ ] `ls -l /etc/apparmor.d/disable/` documents every disabled profile, with a ticket/reason recorded elsewhere.

## Checked
Checked 2026-10-26 against the AppArmor sources on GitLab (master, latest commit 2026-10-23): utils/aa-disable.pod, aa-enforce.pod, aa-complain.pod, apparmor_parser.pod, the aa-disable and aa.py utilities (disable symlink directory), and the Docker AppArmor page.
Confirmed: aa-disable unloads the profile and prevents it loading at startup; aa-enforce and aa-complain reverse it; `apparmor_parser -r` replaces and `-R` removes; the `disable` subdirectory of the profile directory is created and removed by the utilities; `docker-default` is the default container profile.
Removed as unconfirmed: the apt package name and the snapd profile directory.
Method: documentation only; no commands were run.
