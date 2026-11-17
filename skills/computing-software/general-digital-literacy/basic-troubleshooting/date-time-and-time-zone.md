---
id: computing-software.general-digital-literacy.basic-troubleshooting.date-time-and-time-zone
name: date-time-and-time-zone
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-os-settings, date-and-time, time-zone, clock-sync]
level: intro
status: docs-checked
description: "Fix a wrong computer clock: set time and time zone automatically on Windows 11 and Mac, force a Windows sync, and handle daylight saving and the taskbar clock."
sources:
  - https://support.microsoft.com/en-us/windows/experience/personalization/set-time-date-and-time-zone-settings-in-windows
  - https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/troubleshoot-problems-updating-windows
  - https://support.apple.com/guide/mac-help/set-the-date-and-time-automatically-mchlp2996/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date, time and time zone

## Why it matters
Microsoft lists incorrect date and time settings as something that can interfere with Windows Update; Apple notes that a correct time keeps time stamps on emails, messages and files correct.

## Windows 11
- Settings > Time & language > **Date & time**.
- *Set time automatically* **On** for automatic time; **Off** and then **Change** (next to *Set the date and time*) to set it by hand.
- *Set time zone automatically* **On**, or turn it Off and choose from the *Time zone* drop-down.
- Daylight saving: if *Set time zone automatically* is on, daylight saving time is set automatically. If it is off, use *Adjust for daylight saving time automatically*.
- **Sync now** (under Additional settings) forces a time sync.
- Taskbar clock: *Show time and date in the System tray*; *Show seconds in system tray clock* uses more power.

## Mac
System Settings > General > **Date & Time**: turn on *Set time and date automatically* and click Set, enter a network time server for your region and click Done; turn on *Set time zone automatically using your current location*.

## Verify
- [ ] The clock matches a trusted time source and the right zone is shown.

## Checked
Checked 2026-10-27 against Microsoft Support "How to set your time and time zone" and the Windows Update troubleshooting article (Sync now step), and the Apple Mac User Guide "Set the date and time automatically on your Mac". Confirmed: Windows 11 menu path and toggle names, daylight saving rules, taskbar options, Sync now, Mac menu path and options. Removed unconfirmed claims (certificate error text, authenticator codes, time.windows.com and time.apple.com servers, `w32tm` and `net start w32time` commands, CMOS battery advice, Linux dual-boot clock advice, phone menus, secondary clocks).
Method: documentation only; no commands were run.
