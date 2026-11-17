---
id: computing-software.general-digital-literacy.basic-troubleshooting.upgrading-macos
name: upgrading-macos
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-updates, macos-upgrade, macos-compatibility, software-update]
level: intro
status: docs-checked
description: "Update or upgrade a Mac through Software Update: check compatibility, back up with Time Machine, set automatic updates, other download methods, and what to do if startup stalls."
sources:
  - https://support.apple.com/en-us/108382
  - https://support.apple.com/en-us/102662
  - https://support.apple.com/guide/mac-help/keep-your-mac-up-to-date-mchlpx1065/mac
  - https://support.apple.com/en-us/102535
  - https://support.apple.com/guide/mac-help/back-up-files-mh35860/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade macOS

As of Apple's pages dated 14 September 2026, the current major release is **macOS 27 Golden Gate**; Apple lists macOS Tahoe 26, Sequoia 15, Sonoma 14, Ventura 13, Monterey 12, Big Sur 11 and Catalina 10.15 as recent releases with compatibility pages.

## Before
1. **Compatibility:** Software Update only shows updates compatible with your Mac model; if it says your Mac is up to date, no newer compatible macOS is offered. Apple publishes a compatibility page for each release.
2. **Back up** (Apple suggests this before installing new software): connect an external drive and set up Time Machine (Time Machine menu bar icon > Open Time Machine Settings > Add Backup Disk). Time Machine does not back up system files or apps installed with macOS.
3. Plug in power. Do not sleep the Mac or close the lid during installation.

## Install
- System Settings > General > **Software Update**. If software is available, click the button to update, upgrade or restart now. To check again, click **Check for Updates** or close and reopen Software Update. You are asked for your administrator password. The Mac may restart and show a progress bar or blank screen several times.
- Automatic updates: Software Update > the button next to *Automatic Updates*: *Download new updates when available*, *Install macOS updates*, *Install Security Responses and system files*. Laptops must be plugged in to download automatically.
- Other ways to get macOS: macOS Recovery, Terminal (`softwareupdate --list-full-installers` lists versions available for your Mac; `softwareupdate --fetch-full-installer --full-installer-version <number>` downloads one, no earlier than the version that came with your Mac), a bootable installer, or the App Store for some older versions.

## Stuck or failing
- The Apple logo or progress bar can last much longer than usual during an update, and the bar can pause for long periods; Apple recommends starting in the evening.
- If startup never gets past the logo: hold the power button up to 10 seconds, turn on again; then unplug nonessential accessories; then start from macOS Recovery to repair the startup disk with Disk Utility; then reinstall macOS from Recovery. Reinstalling from Recovery keeps your files and user settings.
- Start macOS Recovery: **Apple silicon** - choose Apple menu > Shut Down, then press and hold the power button until startup options appear, choose Options and Continue. **Intel** - restart and immediately hold Command-R (current version), Option-Command-R (latest compatible), or Option-Shift-Command-R (original version).

## Verify
- [ ] Software Update says the Mac is up to date and the Apple menu > About This Mac shows the expected version.

## Checked
Checked 2026-10-27 against Apple Support "Update macOS on Mac" (108382, published 14 Sep 2026), "How to download and install macOS" (102662), "If your Mac starts up to an Apple logo or progress bar" (102535) and the Mac User Guide pages "Keep your Mac up to date", "Back up your files with Time Machine" and "Reinstall macOS". Confirmed: release list, Software Update path and behaviour, automatic update options, Terminal commands, Recovery key combinations and what a Recovery reinstall keeps. Removed unconfirmed claims (about two more years of security updates for unsupported Macs, 32-bit apps stopping at Catalina, 20 to 35 GB free space, Time Machine menu path through General settings, intermediate App Store step for older Macs).
Method: documentation only; no commands were run.
