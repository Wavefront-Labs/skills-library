---
id: computing-software.cybersecurity-defensive.security-operations.linux-incident-triage
name: linux-incident-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, linux-incident-triage, linux-forensics, uac, live-response, bash-history, cron-persistence, systemd-persistence, ssh-authorized-keys, auth-log]
level: advanced
status: draft
description: "Triage a possibly compromised Linux host: volatile data first, then persistence, accounts, logs and suspicious binaries, without trusting local tools."
sources: ["NIST SP 800-86", "UAC (Unix-like Artifacts Collector) documentation", "SANS Linux incident response cheat sheet"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linux incident triage

**Goal:** decide quickly whether a Linux host is compromised and collect enough evidence to
scope it, while changing the host as little as possible.

## Before touching it
- Do not reboot or patch. Consider memory capture (AVML) first if rootkit or fileless activity is suspected.
- Run tools from trusted media or a static toolkit; a compromised host may have trojaned `ps`, `ls`, `netstat`.
- Prefer a collector: **UAC** (`./uac -p ir_triage /mnt/evidence`) gathers live data, logs and hashes in one pass.

## Volatile data (if collecting by hand, save each output to evidence storage)
```
date -u; uptime; who -a; w
ps -eo pid,ppid,user,lstart,cmd --forest
ss -antup
ls -l /proc/*/exe 2>/dev/null | grep -E '(deleted)|/tmp|/dev/shm'
lsof -nP +L1            # deleted-but-open files (common for dropped malware)
cat /proc/<pid>/environ | tr '\0' '\n'; ls -l /proc/<pid>/cwd
```
A running binary whose `/proc/<pid>/exe` points to `(deleted)` or `/dev/shm` is a strong lead:
copy it out with `cp /proc/<pid>/exe /mnt/evidence/pid.bin`.

## Persistence checklist
- Cron: `/etc/crontab`, `/etc/cron.*`, `/var/spool/cron/`.
- systemd: `systemctl list-unit-files --state=enabled`, unit files in `/etc/systemd/system` and `~/.config/systemd/user` recently modified.
- SSH: every `~/.ssh/authorized_keys` (including root and service accounts), `AuthorizedKeysCommand` in sshd_config.
- Shell init: `/etc/profile.d/`, `~/.bashrc`, `/etc/ld.so.preload` (should usually not exist).
- Accounts: UID 0 users other than root in `/etc/passwd`, new sudoers entries.
- Kernel modules: `lsmod`, compare with package-owned modules.

## Logs
- `/var/log/auth.log` or `/var/log/secure` (or `journalctl -u ssh`): logins, sudo.
- `last -f /var/log/wtmp`, `lastb` for failed logins.
- Web server access logs for web-shell requests (POSTs to odd files in upload dirs).
- `~/.bash_history` (often cleared or symlinked to /dev/null; that itself is an indicator).

## Integrity
`rpm -Va` or `debsums -c` / `dpkg --verify` flags changed package files.
`find / -xdev -newermt "2026-10-01" -type f -perm -u+x 2>/dev/null` for recent executables.

## Gotchas
- Containers: the host view (`/proc`) shows container processes; check `docker ps` and container filesystems separately.
- Timestamps in logs are local time unless configured otherwise; record the host timezone.
- Running many commands writes to bash history and logs; document every command you ran.

## Verify
- [ ] Evidence saved off-host with hashes and a command log.
- [ ] Every persistence location reviewed and recorded as clean or suspicious.
