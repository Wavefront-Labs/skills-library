---
id: computing-software.digital-privacy-hygiene.device-hardening.ios-local-network-permission
name: ios-local-network-permission
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, local-network-permission, ios-privacy, app-permissions, macos-sequoia]
level: practitioner
status: draft
description: "Review which iPhone and Mac apps may scan your local network, why apps ask, and when to deny Local Network access to limit device fingerprinting."
sources:
  - "https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Local network permission on iOS

**Goal:** stop apps quietly mapping your home network (devices, names, models), which can fingerprint your household.

## What it gates
Since iOS 14, apps must ask before using Bonjour, multicast or connecting to devices on the local network. macOS 15
Sequoia added the same permission for Mac apps. Apps legitimately need it to cast to TVs, control smart home devices,
print, or sync with a NAS.

## Review
- iPhone/iPad: Settings > Privacy & Security > **Local Network**: toggle per app.
- Mac (15+): System Settings > Privacy & Security > Local Network.

## Decide
| Allow | Deny |
|---|---|
| Casting apps you use (YouTube, Spotify for Chromecast/AirPlay targets), smart home controllers, printer apps, NAS/Plex | Social media, shopping, games, news, banking |

If something stops working (casting target missing, device not found), enable it for that app only.

## Why it matters
A device list (TV model, router, printer names like "Sarah's MacBook") is a stable identifier for your home and can
reveal names. Ad SDKs have been caught scanning LANs for this reason.

## Gotchas
- Denying doesn't block normal internet access; it blocks only local discovery.
- Corporate MDM may pre-approve some apps.
