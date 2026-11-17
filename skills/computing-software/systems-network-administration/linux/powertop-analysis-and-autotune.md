---
id: computing-software.systems-network-administration.linux.powertop-analysis-and-autotune
name: powertop-analysis-and-autotune
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, powertop, power-management, auto-tune, wakeups, laptop, energy-efficiency]
level: practitioner
status: docs-checked
description: "Find power hogs and tune with powertop: calibrate, read wakeups and device stats, --auto-tune and making tunables persistent via a systemd unit, with USB autosuspend pitfalls."
sources:
  - https://github.com/fenrus75/powertop
  - https://raw.githubusercontent.com/fenrus75/powertop/master/doc/powertop.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# powertop

## Measure
```bash
powertop --calibrate          # on battery; cycles devices for better estimates (screen flickers)
powertop                      # interactive mode; Tab and BackTab switch tabs, Space or Return activates an item
powertop --html=report.html --time=60   # HTML report for 60 s
```
Overview: processes and devices by estimated power and wakeups per second; frequent wakeups keep the CPU out of deep
C-states.

## Tune
The Tunables tab lists `Bad`/`Good` entries; Space or Return toggles the selected one. `powertop --auto-tune` sets all tunables to their good setting without interaction;
`--auto-tune-dump` prints the equivalent commands instead of running them (review them first).

Persist as a service:
```ini
# /etc/systemd/system/powertop.service
[Unit]
Description=Powertop tunings
[Service]
Type=oneshot
ExecStart=/usr/sbin/powertop --auto-tune   # adjust to the path from `command -v powertop`
[Install]
WantedBy=multi-user.target
```

## Pitfalls
- Auto-tuning changes every tunable at once; if a peripheral misbehaves afterwards, toggle its tunable back in the
  Tunables tab and persist only the ones you want.
- Do not combine blindly with other power-management tools; they may set the same knobs.

## Verify
- [ ] Measured power draw on battery drops and peripherals still work.

## Checked

Documentation check. Checked 2026-10-27 against the powertop(8) man page from the project repository (dated 2026-05-13) and README: `--auto-tune` (set all tunables to their good setting), `--auto-tune-dump`, `-c`/`--calibrate` (needs battery, cycles display levels and USB activity), `--html[=filename]`, `--time[=seconds]`, and that no arguments starts interactive mode. Removed the list of what auto-tune changes, the USB sysfs and SATA remarks, the TLP and tuned remarks and the 500 wakeups figure, none of which the man page states. Removed the named list of tabs, which the man page does not give; it lists the Tab, BackTab, Space and Return keys.
Method: documentation only; no commands were run.
