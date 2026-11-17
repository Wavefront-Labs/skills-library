---
id: computing-software.systems-network-administration.linux.systemd-monotonic-timers
name: systemd-monotonic-timers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd-timer, onbootsec, onunitactivesec, onunitinactivesec, onactivesec, monotonic-timer, interval-jobs]
level: practitioner
status: docs-checked
description: "Run jobs at intervals relative to boot or last run with OnBootSec/OnUnitActiveSec/OnUnitInactiveSec, combine with OnCalendar, and avoid timers that never fire."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monotonic systemd timers

**Goal:** "every 15 minutes after the last run", "5 minutes after boot" — interval jobs that don't
pile up and don't care about wall-clock time.

## Directives
| Directive | Relative to |
|---|---|
| `OnBootSec=` | kernel boot |
| `OnStartupSec=` | when the service manager started |
| `OnActiveSec=` | timer unit activation |
| `OnUnitActiveSec=` | last time the service was **started** |
| `OnUnitInactiveSec=` | last time the service **finished** — guarantees a gap even if runs are long |

```ini
# /etc/systemd/system/sync.timer
[Timer]
OnBootSec=5min
OnUnitInactiveSec=15min
AccuracySec=30s
RandomizedDelaySec=60
[Install]
WantedBy=timers.target
```
`systemctl enable --now sync.timer`; `systemctl list-timers sync.timer` shows NEXT/LEFT/LAST.

## Why timers "never fire"
- Only `OnUnitActiveSec=`/`OnUnitInactiveSec=` with nothing to start the service first: they are relative to the service's last activation or deactivation, so pair them with `OnBootSec=` or `OnActiveSec=`.
- Timer enabled but not started (`enable` without `--now`): it begins at the next boot.

## Monotonic vs realtime
- Monotonic timers use the monotonic clock, which generally pauses during suspend unless `WakeSystem=` is set; `Persistent=` only has an effect on `OnCalendar=` timers.
- Mixing is allowed: `OnCalendar=daily` + `OnBootSec=10min` = daily and also shortly after each boot.

## Verify
- [ ] `systemctl list-timers` shows a NEXT time; after it passes, `journalctl -u sync.service` shows the run and NEXT moved ≥15 min after completion.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: the five monotonic directives and their reference points (`OnUnitActiveSec=` last activation, `OnUnitInactiveSec=` last deactivation); `AccuracySec=` and `RandomizedDelaySec=`; combining calendar and monotonic timers; the suspend/`WakeSystem=` note; `Persistent=` only for `OnCalendar=`. Removed the unconfirmed extra boot-run remark.

Method: documentation only; no commands were run.
