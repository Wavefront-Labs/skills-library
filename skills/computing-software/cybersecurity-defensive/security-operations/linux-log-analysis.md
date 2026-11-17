---
id: computing-software.cybersecurity-defensive.security-operations.linux-log-analysis
name: linux-log-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, linux-log-analysis, auth-log, journalctl, sshd-logs, sudo-logs, wtmp, btmp, rsyslog, brute-force-detection]
level: practitioner
status: draft
description: "Investigate Linux activity from auth.log/secure, the systemd journal, wtmp/btmp and sudo logs: logins, brute force, privilege use and service changes."
sources: ["NIST SP 800-92 Guide to Computer Security Log Management", "systemd journalctl manual", "OpenSSH sshd manual (LogLevel)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linux log analysis

**Goal:** answer who logged in, from where, what they ran with privilege, and what changed,
using the logs a standard Linux host already writes.

## Where things are
| Distro family | Auth log | System log |
|---|---|---|
| Debian/Ubuntu | `/var/log/auth.log` | `/var/log/syslog` |
| RHEL/Fedora/SUSE | `/var/log/secure` | `/var/log/messages` |
| journald-only | `journalctl` | `journalctl` |
Binary login records: `/var/log/wtmp` (`last`), `/var/log/btmp` (`lastb`), `/var/log/lastlog` (`lastlog`).

## Common questions
Successful SSH logins and method:
```
grep -E "sshd\[[0-9]+\]: Accepted" /var/log/auth.log | awk '{print $1,$2,$3,$9,$11,$7}'
journalctl -u ssh -u sshd --since "2026-10-01" | grep Accepted
```
Brute force / spraying:
```
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head
```
`Invalid user` lines show attempts on non-existent accounts (spraying from lists).
Sudo usage: `grep -E "sudo: .*COMMAND=" /var/log/auth.log`.
Account changes: `useradd`, `usermod`, `passwd`, `groupadd` lines in auth.log.
Service and unit changes: `journalctl _COMM=systemctl` and `journalctl -u <unit>`.

## Correlating
- Match `sshd[PID]` across lines to tie the accept, session open and close.
- `Accepted publickey ... SHA256:<fingerprint>` identifies which key was used; map fingerprints to `authorized_keys` entries with `ssh-keygen -lf`.
- Compare logins with `last -F` output; gaps or a truncated wtmp suggest tampering.

## Centralise
Forward with rsyslog/syslog-ng or an agent to the SIEM; local logs are the first thing an
intruder with root deletes. Journald: set `Storage=persistent` or logs vanish at reboot.

## Gotchas
- Log timestamps in classic syslog format have no year and no time zone; record the host TZ.
- Log rotation compresses old files: search `auth.log.*` and `zgrep` the `.gz` ones.
- `LogLevel VERBOSE` in sshd_config is needed to log key fingerprints on older OpenSSH.
- An attacker with root can edit text logs; the forwarded copy is the evidence of record.

## Verify
- [ ] Findings cross-checked between the local log and the SIEM copy.
- [ ] Time zone and log rotation coverage stated for the period investigated.
