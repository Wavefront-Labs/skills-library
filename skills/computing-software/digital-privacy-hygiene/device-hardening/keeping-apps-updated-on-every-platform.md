---
id: computing-software.digital-privacy-hygiene.device-hardening.keeping-apps-updated-on-every-platform
name: keeping-apps-updated-on-every-platform
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, app-updates, automatic-updates, winget, homebrew, play-store, app-store, flatpak]
level: intro
status: draft
description: "Turn on automatic app updates on Windows, macOS, Android, iOS and Linux, and catch the apps that do not self-update (winget, Homebrew, sideloaded tools)."
sources:
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade"
  - "https://support.google.com/googleplay"
  - "https://www.cisa.gov/secure-our-world"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keeping apps updated on every platform

**Goal:** most exploited bugs are in browsers, office suites, PDF readers and chat apps, not the OS.
Apps must update as reliably as the OS does.

## Turn on auto-update
- **iPhone/iPad:** Settings > App Store > App Updates on.
- **Android:** Play Store > profile icon > Settings > Network preferences > Auto-update apps > Over any
  network (or Wi-Fi only if data is metered).
- **macOS:** System Settings > General > Software Update > (i) next to Automatic Updates > Install application
  updates from the App Store.
- **Windows:** Microsoft Store > profile > Settings > App updates on.
- **Browsers** update themselves but only apply on relaunch: restart Chrome/Edge/Firefox when the
  update badge appears; do not leave a browser open for weeks.

## Apps outside the stores
Windows (winget ships with Windows 11):
```powershell
winget upgrade              # list outdated apps winget knows about
winget upgrade --all --silent
```
macOS Homebrew: `brew update && brew upgrade && brew upgrade --cask --greedy` (`--greedy` includes casks that
claim to self-update). Linux: `sudo apt update && sudo apt upgrade`, `flatpak update`, `snap refresh`.

## Prune instead of patch
- Uninstall apps you have not opened in months; each one is attack surface and a data collector.
- Abandoned apps (no update in 2+ years, removed from the store) get no fixes: replace them.
- Sideloaded APKs and portable `.exe` tools never auto-update; keep a list and check monthly.

## Gotchas
- Auto-update can be silently off after a store sign-out or a "storage almost full" state.
- Old versions of Java, Flash-era plug-ins, and bundled updaters (Adobe, Zoom) are common leftovers; check
  Apps & features for duplicates.

## Verify
- [ ] Store auto-update on for every device.
- [ ] `winget upgrade` / `brew outdated` show nothing important pending.
- [ ] No app on the device you could not name the purpose of.
