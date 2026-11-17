---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-lockdown-mode
name: macos-lockdown-mode
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, macos-lockdown-mode, lockdown-mode, macos-security]
level: practitioner
status: draft
description: "Enable Lockdown Mode on a Mac: what it blocks in Messages, Safari, FaceTime, profiles and accessories, how to exclude sites, and why each device needs it."
sources:
  - "https://support.apple.com/en-us/105120"
  - "https://ssd.eff.org/module/how-to-enable-lockdown-mode-on-iphone"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# macOS Lockdown Mode

**Goal:** shrink the Mac's attack surface if you may be targeted by mercenary spyware.

## Turn on
System Settings > Privacy & Security > **Lockdown Mode** > Turn On > Turn On & Restart. Each Apple device needs it
separately (iPhone, iPad, Mac, Watch).

## What changes
| Area | Restriction |
|---|---|
| Messages | Most attachment types except some images blocked; link previews off |
| Safari/web | Just-in-time JavaScript compilation and some web features disabled unless site excluded |
| FaceTime | Incoming calls from people you haven't called before are blocked |
| Shared albums | Removed; invitations blocked |
| Configuration profiles/MDM | Can't install new profiles or enrol in MDM |
| Wired accessories | Mac laptops with Apple silicon need approval to connect accessories while unlocked |
| Apple services | Incoming invitations blocked unless you've invited first |

## Exclusions
Safari > Settings > Websites > Lockdown Mode: turn off for a specific trusted site that breaks. Per-app
exclusions aren't available on Mac the way they are for web views on iOS.

## Who should use it
Journalists, activists, human-rights defenders, officials and anyone told by Apple threat notifications they may
be targeted.

## Gotchas
- Fonts and some web pages render oddly; expect minor breakage.
- It doesn't replace updates: keep macOS current.
