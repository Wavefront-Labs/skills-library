---
id: computing-software.cybersecurity-defensive.system-hardening.scheduled-job-review
name: scheduled-job-review
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [scheduled-job-review, cron, systemd-timers, scheduled-tasks, persistence, linux-hardening, windows-hardening]
level: practitioner
status: draft
description: "Review scheduled jobs on Linux and Windows (cron, systemd timers, at, Task Scheduler): enumerate, check owners and permissions, spot persistence, and restrict who can schedule."
sources: ["https://attack.mitre.org/techniques/T1053/", "https://man7.org/linux/man-pages/man5/crontab.5.html", "https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/get-scheduledtask", "https://www.cisecurity.org/cis-benchmarks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scheduled job review

Scheduled jobs are both an operational risk (scripts running as root from writable paths) and a favourite
persistence mechanism (ATT&CK T1053). Review them as part of hardening and periodically.

## Linux: enumerate
```bash
ls -la /etc/crontab /etc/cron.d /etc/cron.{hourly,daily,weekly,monthly}
for u in $(cut -d: -f1 /etc/passwd); do crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
ls -la /var/spool/cron/ /var/spool/cron/crontabs/ 2>/dev/null
systemctl list-timers --all
atq                      # pending at jobs
```
Also anacron (`/etc/anacrontab`) and user systemd timers (`systemctl --user list-timers` per user,
`~/.config/systemd/user/`).

## Linux: what to check
- Every job has an owner and purpose (CMDB or comment); unknown jobs investigated.
- Scripts and their directories are owned by root and not writable by others (a root cron job running a
  world-writable script is privilege escalation): `stat -c '%U %a %n' <script>`.
- No jobs fetching and executing remote content (`curl ... | sh`), base64 blobs, or binaries in `/tmp`,
  `/dev/shm`.
- CIS permissions: `/etc/crontab` 600 root:root, `/etc/cron.*` 700, and **allowlists**: create
  `/etc/cron.allow` and `/etc/at.allow` (root only plus named service users), remove `cron.deny`/`at.deny`.

## Windows: enumerate
```powershell
Get-ScheduledTask | Where-Object {$_.TaskPath -notlike '\Microsoft\*'} |
  Select-Object TaskPath, TaskName, State, @{n='RunAs';e={$_.Principal.UserId}}, @{n='Action';e={$_.Actions.Execute + ' ' + $_.Actions.Arguments}}
schtasks /query /fo LIST /v
```
Check: tasks running as SYSTEM or admins whose executable/script path is user-writable (`icacls`), encoded
PowerShell commands, tasks in unusual paths, hidden tasks (missing security descriptor registry tricks can
hide tasks from the UI; compare with `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree`).

## Monitoring
- Linux: auditd watches on `/etc/crontab`, `/etc/cron.d/`, `/var/spool/cron/`, systemd unit directories.
- Windows: Security event 4698 (task created), 4702 (updated), 4699 (deleted) with "Audit Other Object Access
  Events"; Microsoft-Windows-TaskScheduler/Operational 106.
- Compare against a baseline from config management; alert on new jobs.

## Verify
Every job in the inventory has an owner; no job runs a writable script as a privileged user; cron.allow exists;
creating a test task triggers a 4698 or auditd alert in the SIEM.
