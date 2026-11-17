---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.linux-persistence-mechanisms
name: linux-persistence-mechanisms
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [linux-persistence, cron-persistence, systemd-persistence, ssh-authorized-keys, ld-preload, linux-forensics, dfir]
level: practitioner
status: draft
description: "Hunt Linux persistence: cron, systemd units and timers, rc scripts, shell profiles, SSH authorized_keys, ld.so.preload, PAM modules, kernel modules and udev rules."
sources: ["https://attack.mitre.org/tactics/TA0003/", "https://www.sans.org/cyber-security-courses/linux-threat-hunting-incident-response/", "https://github.com/tclahr/uac"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linux persistence mechanisms

**Goal:** enumerate every autostart and access-persistence location on a Linux host and spot
attacker additions.

## Locations
| Mechanism | Where |
|---|---|
| Cron | `/etc/crontab`, `/etc/cron.d/`, `/etc/cron.{hourly,daily,weekly,monthly}/`, `/var/spool/cron/crontabs/<user>` (Debian) or `/var/spool/cron/<user>` (RHEL), `/etc/anacrontab`, `at` jobs `/var/spool/at` |
| systemd | `/etc/systemd/system/`, `/usr/lib/systemd/system/`, `/lib/systemd/system/`, `~/.config/systemd/user/`; `*.service` with `ExecStart`, `*.timer`, drop-ins `*.d/*.conf`; generators |
| SysV/rc | `/etc/init.d/`, `/etc/rc.local`, `/etc/rc*.d/` |
| Shell init | `/etc/profile`, `/etc/profile.d/`, `/etc/bash.bashrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.zshrc` |
| SSH | `~/.ssh/authorized_keys` (incl. root), `/etc/ssh/sshd_config` (`AuthorizedKeysFile`, `PermitRootLogin`) |
| Preload | `/etc/ld.so.preload`, `LD_PRELOAD` in environment files: userland rootkits (libprocesshider) |
| PAM | `/etc/pam.d/*` referencing unusual modules, modified `pam_unix.so` (hash vs package) |
| Kernel | `/etc/modules`, `/etc/modules-load.d/`, `lsmod` vs on-disk modules (LKM rootkits) |
| udev | `/etc/udev/rules.d/` with `RUN+=` |
| Accounts | New UID 0 accounts in `/etc/passwd`, sudoers additions `/etc/sudoers.d/` |
| Web | Web shells in document roots (see web shell skill) |

## Method
1. Collect with UAC or Velociraptor `Linux.Sys.Crontab`, `Linux.Sys.Services`, `Linux.Ssh.AuthorizedKeys`.
2. Timeline file mtimes/ctimes of these paths (`find /etc /var/spool /root /home -newermt "2026-09-01" -ls`).
3. Verify package-owned files (`rpm -Va`, `debsums -c`) to spot modified binaries/configs.
4. Stack across the fleet: rare cron entries, unit names, authorized keys.

## Gotchas
- Attackers timestomp with `touch -r`; ctime still changes (cannot be set without
  changing clock).
- Containers: persistence may live in images or orchestrator (CronJobs, DaemonSets).

## Verify
Every suspicious entry has a creation/modification time placed in the incident timeline and
a link to the payload it runs.
