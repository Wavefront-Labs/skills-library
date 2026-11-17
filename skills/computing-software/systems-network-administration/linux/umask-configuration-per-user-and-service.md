---
id: computing-software.systems-network-administration.linux.umask-configuration-per-user-and-service
name: umask-configuration-per-user-and-service
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, umask-config, umask, pam-umask, login-defs, systemd-umask, default-permissions]
level: practitioner
status: docs-checked
description: "Set default umask where it actually applies: login.defs/pam_umask, shell rc files, systemd UMask=, sftp/samba specifics and checking it."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_umask/pam_umask.8.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
  - https://github.com/openssh/openssh-portable/blob/master/sftp-server.8
  - https://github.com/shadow-maint/shadow/blob/master/man/login.defs.d/UMASK.xml
  - https://www.kernel.org/doc/html/latest/filesystems/proc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring umask

umask is inherited per process; there is no single global setting. Each entry point sets its own.

## Interactive and SSH logins
- `/etc/login.defs`: `UMASK 027` — the default for login and pam_umask; useradd and newusers use it for new home directories when `HOME_MODE` is unset.
- PAM: `session optional pam_umask.so` (session type only). Lookup order: `umask=` in the GECOS other field, the `umask=` argument, `UMASK` in login.defs, then `UMASK=` in /etc/default/login.
  `pam_umask.so umask=0027 usergroups` — `usergroups` copies the owner bits to the group bits for a non-root user whose name equals the primary group name.
- A shell rc file that calls `umask` later (for example `/etc/profile`) replaces the PAM value, because the last call wins.

## Services (systemd)
Services ignore login settings. Set per unit:
```ini
[Service]
UMask=0027
```
System units default to 0022; user units inherit from the per-user service manager. Check: `systemctl show nginx -p UMask`.

## Other daemons
- sftp: the sftp server takes `-u umask` (`Subsystem sftp internal-sftp -u 0027` in sshd_config).
- Cron jobs and other daemons: set `umask` in the script or unit rather than relying on defaults.

## Verify effective values
```bash
umask ; umask -S                        # current shell
grep Umask /proc/<pid>/status           # any running process (field listed in proc(5))
sudo -u alice bash -lc umask            # what a login shell gets
```

## Gotchas
- `umask 077` on build/deploy accounts produces unreadable files for web servers.

## Verify
- [ ] New files created by each path (SSH session, service, sftp) have the intended mode.

## Checked

2026-10-26. Linux-PAM pam_umask(8) source: session-only, lookup order, usergroups, umask= argument. shadow login.defs UMASK and HOME_MODE descriptions. systemd.exec UMask= (default 0022 for system units). OpenSSH portable sftp-server(8) -u option. Linux kernel proc documentation lists the Umask status field. Removed Debian and RHEL specifics, Samba create mask, NFS and cron umask claims and the kernel version number.

Method: documentation only; no commands were run.
