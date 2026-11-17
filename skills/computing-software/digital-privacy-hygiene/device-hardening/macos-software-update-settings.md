---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-software-update-settings
name: macos-software-update-settings
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-software-update, automatic-updates, rapid-security-response]
level: practitioner
status: draft
description: "Set macOS Software Update to install security responses and updates automatically, use softwareupdate from Terminal, and know which macOS versions get fixes."
sources:
  - "https://support.apple.com/guide/mac-help/keep-your-mac-up-to-date-mchlpx1065/mac"
  - "https://support.apple.com/en-us/100100"
  - "https://ss64.com/mac/softwareupdate.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# macOS Software Update settings

**Goal:** every security fix lands quickly without you remembering to check.

## System Settings > General > Software Update > (i) Automatic updates
| Toggle | Set |
|---|---|
| Check for updates | On |
| Download new updates when available | On |
| Install macOS updates | On |
| Install application updates from the App Store | On |
| Install Security Responses and system files | On (rapid security fixes and XProtect data) |

## Terminal
```
softwareupdate -l              # list available updates
sudo softwareupdate -ia -R     # install all and restart
softwareupdate --history       # what was installed when
```

## Which versions are patched
Apple's security releases page (support.apple.com/100100) lists fixes per release. Only the current macOS gets
every fix; the previous two usually get many but not all. Older hardware stuck on old macOS gets fewer fixes:
plan replacement.

## Major upgrades
Major versions appear as "Upgrade Now" separately; updates within your current version keep coming. Wait a week or
two if you depend on specific apps, but don't skip for long.

## Gotchas
- Laptops postpone installs on battery or when the lid is closed; plug in overnight.
- Third-party apps outside the App Store need their own updaters (Homebrew `brew upgrade`, Sparkle-based apps).
