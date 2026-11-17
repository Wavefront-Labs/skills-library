---
id: computing-software.digital-forensics-incident-response.log-analysis.cron-and-systemd-timer-execution-logs
name: cron-and-systemd-timer-execution-logs
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [cron-logs, systemd-timers, linux-logging, linux-persistence, dfir]
level: practitioner
status: docs-checked
description: "Reconstruct scheduled execution on Linux: where cron and systemd timers are defined, how cron output and logs are routed, and persistence abuse."
sources: ["https://man7.org/linux/man-pages/man8/cron.8.html", "https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html", "https://attack.mitre.org/techniques/T1053/003/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cron and systemd timer execution logs

## Cron: where jobs are defined (cronie)
- `/etc/crontab`: system crontab, empty by default on current systems; daily, weekly and monthly jobs now run through anacron (`/etc/anacrontab`).
- `/etc/cron.d/`: system jobs for different users.
- `/var/spool/cron`: user crontabs created by the `crontab` command, named after accounts in `/etc/passwd`. `crontab` updates the spool directory's modtime on change; cron checks crontab modtimes (or uses inotify) to reload.
- ESXi: jobs must be created directly in the crontab file (for example `/var/spool/cron/crontabs/root`).
- Access control: `/etc/cron.allow` and `/etc/cron.deny`.

## Cron: where output and logs go
- By default job output is mailed to the crontab owner, or to `MAILTO` if set. Check the mailbox for output of executed commands.
- With `-s`, job output is sent to syslog; the page says syslog is used when sendmail is not installed. `-m off` disables mail.
- Where cron execution is logged depends on the syslog configuration; MITRE advises checking `/etc/rsyslog.conf` or `/etc/syslog.conf` and looking in `/var/log`. The cron man page mentions a `/var/log/cron` log. Do not assume file names; confirm on the host.

## systemd timers
- A `foo.timer` activates `foo.service` by default; `Unit=` can name a different unit. Read both files.
- Directives: `OnCalendar=` (calendar time), `OnBootSec=`, `OnStartupSec=`, `OnActiveSec=`, `OnUnitActiveSec=`, `OnUnitInactiveSec=` (monotonic). Several can be combined and the timer fires when any elapses.
- `AccuracySec=` and `RandomizedDelaySec=` mean a firing time can differ from the configured one. `Persistent=` affects catch-up of missed runs.
- Calendar timers can fire at unexpected times if the real-time clock is wrong.
- Timers can also run in the per-user service manager.

## Investigation
1. Enumerate every definition above plus timer and service unit files; note owner and file times.
2. Compare file times with the incident timeline to find when the job was planted.
3. Read mail and syslog or journal records for executions, as configured on the host.
4. Compare content against abuse patterns: MITRE T1053.003 lists jobs fetching payloads from remote infrastructure, `@reboot` entries and per-minute download jobs. Attackers may restore file modification times, so do not trust mtime alone.

## Verify
Each suspicious cron or timer definition has a creation time and at least one execution record, both placed on the incident timeline, with the log source and its configuration stated.

## Checked
Confirmed against the cronie cron(8) man page (files and directories, anacron, mail and `-s` syslog output, modtime/inotify), the systemd.timer page (activation, directives, accuracy, randomised delay, clock caveat) and the MITRE T1053.003 page (abuse, ESXi path, audit advice, example cases, mtime restoration). Removed unconfirmed content: specific syslog line formats (`CRON[pid]`, `crontab[pid] REPLACE`), per-distro log paths, journalctl commands, `systemctl list-timers`, user unit directory paths, `at` job spool path, `debugfs` crtime advice and `SystemMaxUse`.

Method: docs-only read of cited pages, 2026-11-09
