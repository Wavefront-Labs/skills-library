---
id: computing-software.digital-privacy-hygiene.device-hardening.disabling-2g-on-phones
name: disabling-2g-on-phones
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, disable-2g, android-security, lockdown-mode]
level: practitioner
status: draft
description: "Turn off 2G to resist cell-site simulators and downgrade attacks on Android and via iPhone Lockdown Mode, and weigh the coverage trade-off."
sources:
  - "https://support.google.com/pixelphone/answer/12452581"
  - "https://www.eff.org/deeplinks/2023/01/google-adds-option-disable-2g-android"
  - "https://support.apple.com/en-us/105120"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Disabling 2G on phones

**Goal:** a fake base station (IMSI catcher, "Stingray") can't force your phone onto 2G, whose weak or absent
encryption allows interception and tracking.

## Android (12+ on supported devices, e.g. Pixel)
Settings > Network & internet > SIMs > [SIM] > **Allow 2G**: off.
Some carriers/OEMs hide the toggle; Android 14+ also lets enterprises enforce it. Emergency calls can still use 2G.

## iPhone
No standalone toggle; **Lockdown Mode** (iOS 17+) disables 2G cellular support along with its other restrictions.

## Trade-offs
| Factor | Effect |
|---|---|
| Rural/remote areas | Some regions still rely on 2G for coverage; you may lose signal |
| Travel | Many countries have shut 2G down already (no loss) |
| IoT/old phones | Unaffected (this is per device) |

## Also consider
- Cellular network security notifications (newer Android) warn about unencrypted connections or identifier
  requests on supported hardware.
- For protests/high-risk events: airplane mode plus Wi-Fi, or leave the phone.

## Gotchas
- Turning off 2G doesn't stop all cell-site simulator techniques (4G/5G-capable simulators exist); it removes the
  easiest downgrade.
- Re-check after SIM swaps/carrier changes; the setting is per SIM.
