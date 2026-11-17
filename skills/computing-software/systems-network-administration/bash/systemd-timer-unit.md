---
id: computing-software.systems-network-administration.bash.systemd-timer-unit
name: systemd-timer-unit
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, systemd-timer-unit, oncalendar, shell-scripting]
level: practitioner
status: docs-checked
description: "Replace cron with a systemd timer and oneshot service for shell scripts, with calendar expressions, Persistent and logs."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html
  - https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing cron with a systemd timer
**Goal:** scheduled script with logging and catch-up.
```ini
# /etc/systemd/system/backup.service
[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
# /etc/systemd/system/backup.timer
[Timer]
OnCalendar=*-*-* 02:15:00
Persistent=true
RandomizedDelaySec=300
```
```bash
systemctl daemon-reload
systemctl start backup.timer
systemctl list-timers
journalctl -u backup.service
journalctl -t backup --since "1 hour ago"
systemd-analyze calendar '*-*-* 02:15'    # parse an expression, show next elapse
```
- `foo.timer` activates `foo.service` by default; `Unit=` overrides that.
- `Persistent=true` stores the last trigger time on disk and triggers the service on activation if a run was missed while the timer was inactive. It only affects `OnCalendar=` timers and is still subject to `RandomizedDelaySec=`.
- If the service is already active when the timer elapses it is not restarted; there are no extra instances.
- `AccuracySec=` defaults to 1min, so a timer may fire up to a minute late; set `1us` for best accuracy. `RandomizedDelaySec=` defaults to 0 and spreads firing times.
- `OnCalendar=` timers wait for time-sync.target; a calendar event missed during suspend is run once on resume (multiple missed events give a single activation).
- `systemd-analyze calendar` takes the same input as `OnCalendar=`; `--iterations=` shows more elapse times.
- Enabling the timer at boot needs an `[Install]` section; see systemd.unit(5).
- Self-check: `systemd-analyze calendar` shows the next elapse you expect.

## Checked
Checked 2026-11-08 against systemd.timer (defaults, Persistent, Unit=, RandomizedDelaySec, AccuracySec, suspend behaviour), systemd-analyze (calendar, --iterations) and journalctl (-u, -t, --since). Removed claims the pages do not give: that the journal captures output automatically, that services get a clean environment, and the `WantedBy=timers.target` and `enable --now` lines.

Method: docs-only read of cited pages, 2026-11-08
