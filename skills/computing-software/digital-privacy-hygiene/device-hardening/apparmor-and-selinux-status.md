---
id: computing-software.digital-privacy-hygiene.device-hardening.apparmor-and-selinux-status
name: apparmor-and-selinux-status
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, apparmor, selinux, linux-hardening, mandatory-access-control]
level: practitioner
status: draft
description: "Check that AppArmor or SELinux is enabled and enforcing on a Linux desktop, read denials, and fix them without switching protection off."
sources:
  - "https://ubuntu.com/server/docs/apparmor"
  - "https://docs.fedoraproject.org/en-US/quick-docs/selinux-getting-started/"
  - "https://wiki.archlinux.org/title/AppArmor"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AppArmor and SELinux status

**Goal:** the distribution's mandatory access control is on and enforcing, so a compromised app is confined.

## Which one
Ubuntu, Debian, openSUSE (older) use **AppArmor**; Fedora, RHEL and derivatives use **SELinux**.

## AppArmor
```
sudo aa-status          # loaded profiles, enforce vs complain counts
sudo aa-enforce /etc/apparmor.d/usr.bin.foo
sudo aa-complain /etc/apparmor.d/usr.bin.foo   # log only, for debugging
journalctl -k | grep -i apparmor | grep DENIED
```
Confirm `apparmor` is in the kernel command line or enabled by default (`cat /sys/module/apparmor/parameters/enabled`
shows `Y`).

## SELinux
```
getenforce                  # Enforcing / Permissive / Disabled
sestatus
sudo ausearch -m avc -ts recent
sudo restorecon -Rv /path   # fix wrong file labels (the usual cause)
```
Permanent mode is in `/etc/selinux/config` (`SELINUX=enforcing`).

## When something breaks
1. Find the denial in the log.
2. Common fixes: wrong labels after moving files (`restorecon`), a boolean (`getsebool -a | grep httpd`,
   `setsebool -P ...`), or an AppArmor profile in complain mode while you adjust it.
3. Never set SELinux to disabled or uninstall AppArmor to "fix" an app; switch only that domain or profile to
   permissive/complain while you investigate.

## Verify
After reboot, `getenforce` says Enforcing or `aa-status` lists profiles in enforce mode.
