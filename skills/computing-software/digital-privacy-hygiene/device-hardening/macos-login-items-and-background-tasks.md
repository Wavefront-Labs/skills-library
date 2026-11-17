---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-login-items-and-background-tasks
name: macos-login-items-and-background-tasks
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, login-items, launchagents, launchdaemons, macos, persistence, background-items, knockknock]
level: practitioner
status: draft
description: "Review macOS Login Items and background tasks, find LaunchAgents/Daemons used by adware and stealers for persistence, and remove them safely."
sources:
  - "https://support.apple.com/guide/mac-help/welcome/mac"
  - "https://support.apple.com/guide/deployment/welcome/web"
  - "https://objective-see.org/products/knockknock.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS login items and background tasks

**Goal:** know everything that starts automatically on a Mac; that list is where adware, infostealers and
leftover helper tools persist.

## Review in Settings
System Settings > General > **Login Items & Extensions** (Login Items on older releases):
- **Open at Login**: apps launched at sign-in. Remove what you do not need daily.
- **Allow in the Background**: helpers and agents. Toggle off unknown entries; the (i) button reveals the file in Finder.
macOS also shows a **"Background Items Added"** notification when something registers; treat an unexpected one as an alert.

## Look at the files
Persistence plists live in:
```
~/Library/LaunchAgents       # per-user
/Library/LaunchAgents        # all users, run as the user
/Library/LaunchDaemons       # run as root
```
```bash
ls -la ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons
launchctl list | grep -v com.apple          # loaded non-Apple jobs
sudo sfltool dumpbtm | less                 # Background Task Management database
```
Suspicious signs: random names (`com.abcxyz.plist`), programs in `/tmp`, `~/Library/Application Support/<random>`,
or hidden dot-folders; `ProgramArguments` running `osascript`, `curl` or `bash -c`.

## Remove
```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.bad.agent.plist
rm ~/Library/LaunchAgents/com.bad.agent.plist
```
Delete the referenced binary too, then reboot and recheck. For a known product, use its uninstaller instead.
Free tools: Objective-See **KnockKnock** (inventory) and **BlockBlock** (alerts on new persistence).

## Gotchas
- If you find a stealer (fake app installed from a "cracked" download or fake meeting app), removal is not
  enough: change passwords from a clean device and revoke sessions.

## Verify
- [ ] Every Open at Login / background entry is recognised; no unsigned agents in LaunchAgents folders.
