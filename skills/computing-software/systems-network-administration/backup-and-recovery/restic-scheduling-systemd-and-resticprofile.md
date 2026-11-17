---
id: computing-software.systems-network-administration.backup-and-recovery.restic-scheduling-systemd-and-resticprofile
name: restic-scheduling-systemd-and-resticprofile
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, resticprofile, restic-systemd, systemd-timer, backup-automation, healthchecks]
level: practitioner
status: docs-checked
description: "Automate restic with systemd service and timer units or resticprofile: environment files, backup plus retention and check schedules, randomised delay, and dead-man alerts."
sources:
  - https://restic.readthedocs.io/en/stable/080_examples.html
  - https://creativeprojects.github.io/resticprofile/
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling restic with systemd timers and resticprofile

**Goal:** backups, retention and checks that run unattended and alert when they stop.

## systemd units
`/etc/restic/web01.env` (mode 600):
```bash
RESTIC_REPOSITORY=rest:https://backup.example:8000/web01/
RESTIC_PASSWORD_FILE=/etc/restic/password
```
`/etc/systemd/system/restic-backup.service`:
```ini
[Unit]
Description=restic backup
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
EnvironmentFile=/etc/restic/web01.env
ExecStart=/usr/bin/restic backup /etc /srv --exclude-file=/etc/restic/excludes --tag nightly
ExecStartPost=/usr/bin/curl -fsS https://monitor.example/ping/<id>
Nice=10
IOSchedulingClass=idle
```
`/etc/systemd/system/restic-backup.timer`:
```ini
[Timer]
OnCalendar=*-*-* 01:30
RandomizedDelaySec=30m
Persistent=true

[Install]
WantedBy=timers.target
```
```bash
systemctl daemon-reload && systemctl enable --now restic-backup.timer
systemctl list-timers restic-*
journalctl -u restic-backup.service -n 50
```
Add separate units for `forget --prune` (weekly) and `check --read-data-subset` (monthly). `ExecStartPost=` commands run only after `ExecStart=` succeeded, so the ping fires only when restic exits 0 and a missed or failed run raises the dead-man alert at your monitor. A partial backup (exit 3) is a failure for this purpose; decide whether to accept it.

## resticprofile
`profiles.yaml` (resticprofile configuration, format version 1):
```yaml
version: "1"

web01:
  repository: "rest:https://backup.example:8000/web01/"
  password-file: "/etc/restic/password"
  backup:
    source: ["/etc", "/srv"]
    exclude-file: "/etc/restic/excludes"
    schedule: "01:30"
    schedule-permission: system
  retention:
    after-backup: true
    keep-daily: 7
    keep-weekly: 5
    keep-monthly: 12
    prune: true
  check:
    schedule: "monthly"
```
`resticprofile --name web01 schedule` installs the schedules of that profile (`schedule --all` installs every profile). On Linux resticprofile uses systemd if available, otherwise crond; launchd is used on macOS and Task Scheduler on Windows. Scheduling can be set on the `backup`, `check`, `forget`, `prune` and `copy` sections; scheduling `retention` directly is deprecated (use `forget`). With `schedule --all`, choose either user or system mode, not both; `schedule-permission: system` needs a privileged user.

## Verify
Timers listed with next run times, journal shows successful runs, and stopping the job triggers the dead-man alert.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Also: systemd.timer, systemd.service and systemd.exec man sources on GitHub (OnCalendar, RandomizedDelaySec, Persistent defaults, ExecStartPost ordering, Nice, IOSchedulingClass) and resticprofile docs (repo last commit 2026-07-08, release v0.33.1): scheduler selection, schedule command and --all, schedule-permission, deprecation of scheduling retention, version "1" config. Removed the unconfirmed resticprofile read-data-subset key and file path.

Method: documentation only; no commands were run.
