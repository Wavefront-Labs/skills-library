---
id: computing-software.general-digital-literacy.basic-troubleshooting.running-older-programs-in-compatibility-mode
name: running-older-programs-in-compatibility-mode
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-software, program-compatibility, compatibility-mode, legacy-software]
level: intro
status: docs-checked
description: "Make an older app run on Windows 11: update it, run the Program Compatibility Troubleshooter, update drivers, and keep the built-in antivirus on."
sources:
  - https://support.microsoft.com/en-us/windows/apps/make-older-apps-or-programs-compatible-with-the-latest-version-of-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run older programs on current Windows

## Try in this order (Microsoft's guidance)
1. **Check for updates.** Microsoft Store apps: update from the Store (Library / Get updates). Other apps: look on the publisher's website for a new or updated version; searching for "Windows compatibility" plus the app name helps.
2. **Program Compatibility Troubleshooter:** Settings > System > **Troubleshoot** > **Other troubleshooters** > *Program Compatibility Troubleshooter* > **Run**, then follow the prompts. (Windows 10: Settings > Update & Security > Troubleshoot > Additional troubleshooters.)
3. **App runs with glitches** (flickering windows, unresponsive, problems during remote use, or a message that it might not work correctly): run the troubleshooter again and update device drivers to the latest versions through Windows Update.
4. If you cannot install your usual antivirus yet, the built-in Windows Security antivirus protects the PC.

## When it still fails
- Ask the publisher for a Windows-compatible version, or replace the program with a current alternative.
- Do not turn off security features to make an old program run.

## Verify
- [ ] The program starts, saves and prints normally after the troubleshooter's chosen settings.

## Checked
Checked 2026-10-27 against Microsoft Support "Make older apps or programs compatible with the latest version of Windows" (Windows 11 and 10 sections). Confirmed: update-first guidance, troubleshooter path, driver update advice, Windows Security note, the "This app or game can't run on your device" style message. Removed unconfirmed claims (Properties > Compatibility tab options, reduced colour and 640x480 modes, high DPI override, run as administrator, 16-bit installers, virtual machine, DOSBox and VueScan advice, old-software security advice).
Method: documentation only; no commands were run.
