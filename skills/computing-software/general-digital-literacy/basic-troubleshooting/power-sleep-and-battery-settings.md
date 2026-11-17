---
id: computing-software.general-digital-literacy.basic-troubleshooting.power-sleep-and-battery-settings
name: power-sleep-and-battery-settings
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, os-settings, power-settings, sleep-settings, battery-saver, power-mode, lid-close]
level: intro
status: draft
description: "Set screen-off and sleep timers, power modes, battery saver and lid-close actions on Windows and Mac, and fix a computer that won't sleep or wakes up by itself."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power, sleep and battery settings

**Goal:** the laptop lasts the day, sleeps when idle, and wakes instantly.

## Windows 11
- Settings › System › **Power & battery**:
  - *Screen, sleep & hibernate timeouts*: e.g. screen off 5 min on battery / 10 plugged in; sleep 15 / 30.
  - **Power mode**: Best power efficiency, Balanced, Best performance.
  - **Energy Saver/Battery saver**: turn on automatically at 20%.
- Lid and power button: Control Panel › Power Options › **Choose what closing the lid does** (Sleep, Hibernate, Shut down, Do nothing). Hibernate saves to disk; useful for long breaks.
- Won't sleep? Run `powercfg /requests` (admin terminal) to see what's blocking it (media playing, open file shares). Wakes up by itself: `powercfg /lastwake` and `powercfg /waketimers`; in Device Manager untick *Allow this device to wake the computer* for the mouse or network adapter.
- Battery report: `powercfg /batteryreport` writes `battery-report.html` showing design vs full charge capacity.

## Mac
- System Settings › **Battery**: *Low Power Mode* (Always, Only on battery), Options › *Prevent automatic sleeping when the display is off* (plugged in), *Wake for network access*.
- **Lock Screen** settings: *Turn display off on battery when inactive*.
- Battery health: Battery › **Battery Health** (i); *Optimised Battery Charging* limits wear.
- Won't sleep: `pmset -g assertions` in Terminal lists apps preventing sleep.

## Good defaults
- Sleep, not shut down, for daily use; restart at least weekly for updates.
- Keep laptops between 20-80% when possible; avoid heat.

## Verify
- [ ] Leave the computer idle: screen turns off and it sleeps at the set times; wakes with a key press.
