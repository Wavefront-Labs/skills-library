---
id: computing-software.systems-network-administration.linux.migrate-cron-jobs-to-systemd-timers
name: migrate-cron-jobs-to-systemd-timers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cron-to-timer, systemd-timer, cron, oncalendar, persistent-timer, job-migration]
level: practitioner
status: docs-checked
description: "Convert crontab entries to systemd service+timer pairs: translating schedules to OnCalendar, environment and user differences, logging, overlap prevention and missed-run catch-up."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html
  - https://wiki.archlinux.org/title/Systemd/Timers#As_a_cron_replacement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating cron jobs to systemd timers

**Why:** journal logging, an already-active unit is not restarted when the timer elapses, dependencies (`After=network-online.target`), resource
limits, `Persistent=` catch-up after downtime, `systemctl list-timers` visibility.

## Translate the schedule
| crontab | OnCalendar |
|---|---|
| `*/15 * * * *` | `*:0/15` |
| `0 3 * * *` | `*-*-* 03:00:00` |
| `0 0 * * *` | `daily` (= `*-*-* 00:00:00`) |
| `30 2 * * 1-5` | `Mon..Fri *-*-* 02:30` |
| `0 0 1 * *` | `*-*-01 00:00` / `monthly` |
| `@reboot` | `OnBootSec=1min` (no OnCalendar) |
Validate: `systemd-analyze calendar 'Mon..Fri *-*-* 02:30' --iterations=3`.

## Example: `30 2 * * * backup /usr/local/bin/db-backup.sh >> /var/log/db-backup.log 2>&1`
`/etc/systemd/system/db-backup.service`
```ini
[Unit]
Description=Nightly DB backup
Wants=network-online.target
After=network-online.target
[Service]
Type=oneshot
User=backup
ExecStart=/usr/local/bin/db-backup.sh
Nice=10
IOSchedulingClass=idle
```
`/etc/systemd/system/db-backup.timer`
```ini
[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true
RandomizedDelaySec=10min
[Install]
WantedBy=timers.target
```
`systemctl daemon-reload && systemctl enable --now db-backup.timer`; then remove the cron line.
Test immediately: `systemctl start db-backup.service; journalctl -u db-backup -e`.

## Differences that break jobs
- Environment: no crontab variables or shell profile — set `Environment=`/`EnvironmentFile=` in the service.
- Output goes to the journal, not mail: use `OnFailure=` pointing at a unit you define for alerts (cron's MAILTO equivalent).
- If the unit is already active when the timer elapses it is left running, not started again.
- Timezone: the calendar event uses the current time zone unless you append one (`... 02:30 Europe/London`).

## Verify
- [ ] `systemctl list-timers db-backup.timer` shows NEXT; a manual start succeeds; the cron entry is gone (`crontab -l -u backup`).

## Checked

Checked against systemd.time(7), systemd.timer(5), systemd.exec(5), systemd.service(5) and systemd-analyze(1) sources in the systemd repository (man/*.xml, current main).
Confirmed: `daily`, `monthly` and `weekly` expansions, `Mon..Fri` weekday ranges, `*:0/15` style repetition, `OnBootSec=`, `Persistent=`, `RandomizedDelaySec=`, an already-active unit is not restarted, timezone suffix in calendar events, `systemd-analyze calendar --iterations=`, `Type=oneshot`, `IOSchedulingClass=`, `EnvironmentFile=`.
Removed as unconfirmed: the `notify@%n.service` template (it is not a shipped unit) and the sandboxing benefit claim.

Method: documentation only; no commands were run.
