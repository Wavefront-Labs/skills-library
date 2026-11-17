---
id: computing-software.general-digital-literacy.basic-troubleshooting.app-keeps-crashing
name: app-keeps-crashing
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, mobile-devices, app-crashing, force-stop, clear-app-cache, offload-app, repair-app]
level: intro
status: draft
description: "Fix an app that keeps crashing or freezing on iPhone, Android, Windows or Mac: force close, update, clear cache, reinstall, free storage, and report the bug."
sources:
  - https://support.apple.com/guide/iphone/welcome/ios
  - https://support.google.com/android
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App keeps crashing

**Goal:** the app opens and stays open, without losing your data.

## Steps (stop when fixed)
1. **Force close and reopen.** iPhone: swipe up from the bottom and pause, swipe the app away. Android: Recent apps › swipe away, or Settings › Apps › app › **Force stop**. Windows: `Ctrl+Shift+Esc` › End task. Mac: `Cmd+Option+Esc` › Force Quit.
2. **Restart the device.**
3. **Update the app and the system.** Crashes right after a system update are often fixed by an app update a few days later.
4. **Free storage.** Under ~1-2 GB free, apps crash; delete videos, clear downloads.
5. **Clear cache** (Android): Settings › Apps › app › Storage › **Clear cache** (safe). *Clear storage/data* resets the app and deletes local data; sign-ins and offline files go.
6. **Offload or reinstall.** iPhone: Settings › General › iPhone Storage › app › **Offload App** (keeps documents and data) › Reinstall. Otherwise delete and reinstall; check data is backed up/synced first (WhatsApp chats, game progress, authenticator codes).
7. **Windows Store apps:** Settings › Apps › Installed apps › app › Advanced options › **Repair**, then **Reset**.
8. **Check the service:** status pages or Downdetector; sometimes the server is down, not your device.

## Report it
In-app *Help/Report a problem*, store review, or the developer's support page; include device model, system version and what you did before it crashed. Windows Reliability Monitor (`perfmon /rel`) and Mac Console › Crash Reports show the crash details.

## Gotchas
- One app crashing: app problem. Many apps crashing: storage, system update or hardware.
- Uninstalling an authenticator app before moving its accounts locks you out of logins.

## Verify
- [ ] App runs a full session without crashing; your data is intact.
