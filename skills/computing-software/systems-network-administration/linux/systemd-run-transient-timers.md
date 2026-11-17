---
id: computing-software.systems-network-administration.linux.systemd-run-transient-timers
name: systemd-run-transient-timers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd-run, transient-timer, systemd-run-timer, on-calendar, one-off-job, at-replacement]
level: practitioner
status: docs-checked
description: "Schedule one-off or temporary jobs with systemd-run --on-active/--on-calendar: transient timer+service pairs, user scope, properties, listing and cancelling them."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transient timers with systemd-run

**Goal:** "run this in 2 hours" or "every 10 minutes until reboot" without writing unit files —
a logged, cgroup-tracked replacement for `at` and ad-hoc cron lines.

## Examples
```bash
systemd-run --on-active=2h --unit=reindex /usr/local/bin/reindex --full
systemd-run --on-calendar='2026-11-01 02:30' --unit=cutover /usr/local/bin/cutover.sh
systemd-run --on-calendar='*:0/10' --unit=probe --timer-property=AccuracySec=1s /usr/local/bin/probe
systemd-run --on-boot=15min /usr/local/bin/task          # 15 minutes after boot
systemd-run --user --on-active=30m /usr/local/bin/remind
```
Properties for the service side: `-p MemoryMax=1G -p CPUQuota=50% -p User=app`, `--setenv=K=V`,
`--working-directory=`. Timer side: `--timer-property=`.

## Manage
```bash
systemctl list-timers --all
systemctl status reindex.timer reindex.service
journalctl -u reindex.service
systemctl stop reindex.timer       # cancel before it fires
```
Without `--unit`, the name is generated (`run-NNNN.service`, as in the manual); name them for operators.

## Gotchas
- `--on-*` options cannot be combined with `--scope` or `--pty`.
- Calendar spec quoting: wrap in single quotes; validate with `systemd-analyze calendar '*:0/10'`.

## Verify
- [ ] `systemctl list-timers` shows the named timer with the right NEXT; after firing, the service log shows exit 0.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `--on-active`, `--on-boot`, `--on-startup`, `--on-unit-active`, `--on-unit-inactive`, `--on-calendar` as shortcuts for `--timer-property`; only the transient timer starts immediately and triggers the service; `--slice=`, `--working-directory=`, `--user`, `--pty`; `-p` properties; generated `run-NNNN.service` names; `systemd-analyze calendar`. Removed the reboot-persistence, clean-environment and repeat-timer remarks.

Method: documentation only; no commands were run.
