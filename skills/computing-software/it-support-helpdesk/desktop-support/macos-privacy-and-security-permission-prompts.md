---
id: computing-software.it-support-helpdesk.desktop-support.macos-privacy-and-security-permission-prompts
name: macos-privacy-and-security-permission-prompts
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, macos-privacy-permissions, tcc, pppc, screen-recording, full-disk-access, accessibility]
level: practitioner
status: draft
description: "Sort out macOS privacy prompts (TCC): which permission an app needs, granting or resetting it, what MDM PPPC can and cannot pre-approve, and recurring screen-recording prompts."
sources:
  - "https://support.apple.com/guide/mac-help/control-access-to-screen-and-system-audio-recording-mchld6aa7d23/mac"
  - "https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web"
  - "https://ss64.com/mac/tccutil.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-privacy-and-security-permission-prompts

## Map symptom to permission (System Settings > Privacy & Security)
| Symptom | Permission |
|---|---|
| Others see a black/grey screen when the user shares in Teams/Zoom, remote tool sees wallpaper only | Screen & System Audio Recording |
| Remote tool cannot click/type, automation tools fail | Accessibility |
| Backup/AV/EDR cannot read user folders | Full Disk Access |
| No video/audio in calls | Camera / Microphone |
| Hotkey or text expander apps dead | Input Monitoring |

Grant the toggle, then **quit and reopen** the app (screen recording often needs it).

## Reset a stuck entry
```bash
tccutil reset ScreenCapture com.microsoft.teams2
tccutil reset All com.vendor.app
```
The app prompts again on next use. Find a bundle ID with `osascript -e 'id of app "AppName"'`.

## What MDM can do (PPPC profile)
- Can pre-approve Accessibility, Full Disk Access, and many others for a signed app.
- Cannot silently grant Camera, Microphone, or Screen Recording; for Screen Recording it
  can only let standard users approve it themselves ("Allow Standard User to Set System
  Service"). Users still click once.
- Profile must match the app's bundle ID and code requirement exactly.

## Recurring prompts
Recent macOS versions periodically ask users to re-confirm screen recording for apps
that use it. That is expected; explain it rather than troubleshooting it.

## Gotchas
- Non-admin users cannot toggle some panes without MDM help.
- Apps updated with a new signing identity lose their grants.
- Terminal and scripting tools need Full Disk Access themselves when scripts touch
  protected folders.

## Verify
The app works for the feature in question after relaunch and the permission shows
enabled in Privacy & Security (or delivered by the MDM profile).
