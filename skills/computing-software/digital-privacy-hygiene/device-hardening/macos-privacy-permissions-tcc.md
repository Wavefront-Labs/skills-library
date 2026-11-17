---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-privacy-permissions-tcc
name: macos-privacy-permissions-tcc
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-tcc-permissions, macos, tcc, full-disk-access, screen-recording, accessibility, tccutil]
level: practitioner
status: draft
description: "Review and reset macOS privacy permissions (TCC): Full Disk Access, Accessibility, Screen Recording, Input Monitoring, camera, mic and Automation, using Settings and tccutil."
sources:
  - "https://support.apple.com/guide/mac-help/welcome/mac"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://objective-see.org/tools.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS privacy permissions (TCC)

**Goal:** apps on a Mac can only reach protected data and capture input if Transparency, Consent and
Control (TCC) lets them. Keep that list short.

## Review
System Settings > **Privacy & Security**. Highest risk first:
| Permission | What it grants |
|---|---|
| Full Disk Access | Mail, Messages, Safari history, other apps' data, Time Machine |
| Accessibility | Control the Mac: click, type, read UI of other apps |
| Input Monitoring | Read all keystrokes (keylogger power) |
| Screen & System Audio Recording | See everything on screen |
| Automation | Script other apps (e.g. Terminal controlling Finder/Mail) |
| Files and Folders, Photos, Contacts, Calendars, Camera, Microphone, Location | Self-explanatory |
| App Management, Developer Tools | Modify other apps; bypass some checks |

Remove anything you do not recognise or no longer use (select, press minus, or toggle off).

## Gotchas
- Granting **Terminal** or iTerm Full Disk Access gives it to every script and tool you run there.
- Remote support tools (TeamViewer, AnyDesk) request Accessibility + Screen Recording; scammers rely on this.
  Remove them after the session.
- macOS Sequoia re-prompts periodically for screen recording; do not approve by reflex.
- Orange (mic) and green (camera) dots in the menu bar show live use; Control Center names the app.

## Reset with tccutil
```bash
osascript -e 'id of app "zoom.us"'          # get bundle ID -> us.zoom.xos
tccutil reset Camera us.zoom.xos             # one service, one app
tccutil reset All us.zoom.xos                # every permission for that app
tccutil reset ScreenCapture                  # all apps, one service
```
The TCC database itself is protected by SIP; use Settings or tccutil, not direct edits.

## Verify
- [ ] Full Disk Access, Accessibility, Input Monitoring and Screen Recording lists each contain only apps you can justify.
- [ ] No leftover remote-access tools.
