---
id: computing-software.general-digital-literacy.basic-troubleshooting.fixing-stuck-updates
name: fixing-stuck-updates
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, updates, windows-update, stuck-update, update-error, update-troubleshooter, pause-updates, macos-update-stuck, 0x80070002, active-hours]
level: intro
status: docs-checked
description: "Get a failing Windows update going: troubleshooter, free space, disconnect hardware, error codes, DISM and sfc; and handle a Mac stuck on the Apple logo during an update."
sources:
  - https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/troubleshoot-problems-updating-windows
  - https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/windows-update-faq
  - https://support.apple.com/en-us/102535
  - https://support.apple.com/en-us/108382
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Stuck or failing updates

**Goal:** finish an update that hangs or keeps failing, without damaging the system.

## Windows: before you start
Back up your personal files first (Windows backup, or copy them to a USB drive, or OneDrive folder backup). Microsoft says to do this before trying the fixes below.

## Windows update fails (Microsoft's general order, Windows 11)
1. **Troubleshooter:** run the Windows Update troubleshooter in the Get Help app, or Settings > System > **Troubleshoot** > **Other troubleshooters** > Windows Update > **Run**.
2. Plug the device into power and make sure it is connected to the internet (Settings > Network & internet > Wi-Fi).
3. Use an **administrator** account; some updates need it.
4. **Disconnect external hardware:** remove external drives, docks and other unneeded devices, then try again.
5. **Clear the update cache:** `Win+R`, `services.msc`, right-click **Windows Update** > Stop; delete everything inside the `SoftwareDistribution` folder in the Windows folder; right-click **Windows Update** > Start.
6. **Date and time:** Settings > Time & language > Date & time; turn on *Set time automatically* and *Set time zone automatically*, and use **Sync now** under Additional settings if needed.
7. Update third-party drivers from the hardware maker's site.
8. **Free space:** Microsoft says you need at least **16 GB** free to upgrade a 32-bit OS, or **20 GB** for 64-bit.
9. Run Settings > Windows Update > **Check for updates** again, then restart (**Update and restart**).
10. **Repair system files:** in Command Prompt run as administrator, `DISM.exe /Online /Cleanup-image /Restorehealth`, then `sfc /scannow` (wait for 100 percent), then retry the update.
- Error codes listed in the article include `0x8007000d` (update files or cache corrupt), `0x800705b4` (update took too long or was interrupted), `0x800f0922` (insufficient disk space or .NET Framework or other component problems), `0x80070057`, `0x80070005` and `0x80070002`. Look the code up in the article's error table.
- Need to delay updates? Settings > Windows Update > **Pause updates** and pick a length; after the pause limit you must install the latest updates before pausing again. Active hours stop automatic restarts while you work.

## Mac
Software Update is in System Settings > General > **Software Update**. During an update or upgrade, the Apple logo or progress bar can stay up much longer than usual and the bar can pause for long periods; Apple recommends starting in the evening so it can finish overnight. If startup never gets past the logo or progress bar:
1. Press and hold the power button (Touch ID on laptops with it) for up to 10 seconds until the Mac turns off, then turn it on.
2. Still stuck: turn it off again, unplug nonessential accessories (printers, drives, USB hubs), and turn it on.
3. Still stuck: turn it off and start from macOS Recovery to repair the startup disk with Disk Utility, then if needed **Reinstall macOS** from Recovery, which keeps your files and user settings (the Mac needs an internet connection).
4. If it still hangs, the Mac may need service.

## Gotchas
- Allow installation to finish without sleeping the Mac or closing its lid; it may restart several times and show a blank screen.

## Verify
- [ ] Settings > Windows Update > Update history shows the update installed, or the Mac boots to the new version.

## Checked
Checked 2026-10-27 against Microsoft Support "Troubleshoot problems updating Windows" and "Windows Update: FAQ", and Apple Support "If your Mac starts up to an Apple logo or progress bar" (102535), "Update macOS on Mac" (108382) and the Mac User Guide "Reinstall macOS". Confirmed: backup warning, troubleshooter paths, cache clearing steps, 16 or 20 GB, DISM and sfc commands, error codes, pause behaviour, Mac 10-second power-button steps and Recovery reinstall keeping files. Removed unconfirmed claims (1 to 2 hours wait, "Undoing changes" rollback wording, 1 to 5 week pause length, Windows 11 Installation Assistant advice, Mac 20 GB free space, wait one hour).
Method: documentation only; no commands were run.
