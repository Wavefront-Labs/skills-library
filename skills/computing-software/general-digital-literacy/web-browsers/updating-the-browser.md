---
id: computing-software.general-digital-literacy.web-browsers.updating-the-browser
name: updating-the-browser
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-settings, update-browser, browser-version, relaunch-to-update]
level: intro
status: docs-checked
description: "Check the browser version and update Chrome and Edge, what the relaunch keeps, Chrome's operating system requirements, and where update problems are covered."
sources:
  - https://support.google.com/chrome/answer/95414
  - https://support.microsoft.com/en-us/edge/what-to-do-if-microsoft-edge-isn-t-working
  - https://support.microsoft.com/en-us/Edge/troubleshooting-tips-for-downloading-installing-and-updating-microsoft-edge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Update the browser

Chrome's help says updates bring the latest security protections. Updating regularly is one of the simplest protections.

## Chrome
- On a computer: More > Help > **About Google Chrome** (the version number is shown under the heading; Chrome checks for updates on this page). Select **Relaunch** to apply. No Relaunch button means you are on the latest version.
- Chrome saves open tabs and windows and reopens them after the restart; Incognito windows do not reopen. Select Not now to apply the update at the next restart.
- Windows: close all Chrome windows and relaunch. Mac: "Automatically update Chrome for all users" is on the About page when Chrome is in the Applications folder. Linux: use the package manager. Chromebook: update the Chromebook operating system.
- System requirements (Chrome Help, October 2026): Windows 10 and up on Intel (with an SSE3-capable processor), Windows 11 and up on ARM, macOS 13 Ventura and up, and 64-bit Linux distributions such as Ubuntu 18.04+, Debian 10+, openSUSE 15.5+ or Fedora 39+. On an older operating system Chrome cannot update; the operating system must be upgraded.

## Edge
Settings and more > Settings > **About Microsoft Edge**; apply the update offered there. Microsoft keeps separate guidance on installing and updating problems (link in sources). If Edge will not open or work, Settings > Apps > Installed apps > Microsoft Edge > Modify > Repair is Microsoft's repair step; Microsoft says browser data and settings should not be affected.

## Verify
- [ ] The About page says the browser is up to date after the relaunch.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Update Google Chrome" and Microsoft Support "What to do if Microsoft Edge isn't working", read in October 2026. Confirmed: the About paths, Relaunch behaviour, tab restore, the system requirements and the Edge update path. Removed as unconfirmed: the "coloured Update button", Chrome update error numbers, claims about patch frequency and infection rates, and the Firefox, Safari and phone steps.
Method: documentation only; no commands were run.
