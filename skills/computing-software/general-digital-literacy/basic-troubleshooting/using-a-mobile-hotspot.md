---
id: computing-software.general-digital-literacy.basic-troubleshooting.using-a-mobile-hotspot
name: using-a-mobile-hotspot
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, wifi, connectivity, mobile-hotspot, tethering, personal-hotspot, data-allowance, usb-tethering, metered-connection]
level: intro
status: draft
description: "Share your phone's mobile data with a laptop via personal hotspot or USB tethering, keep it secure, and avoid burning through your data allowance."
sources:
  - https://support.apple.com/guide/iphone/welcome/ios
  - https://support.google.com/android
  - https://support.microsoft.com/en-us/windows
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using a mobile hotspot

**Goal:** get a laptop online through your phone when Wi-Fi is down or untrustworthy.

## Turn it on
- **iPhone:** Settings › **Personal Hotspot** › Allow Others to Join; note the Wi-Fi password (change
  it to something strong). Macs/iPads on the same Apple Account can join without the password.
- **Android:** Settings › Network & internet › **Hotspot & tethering** › Wi-Fi hotspot › on; set name,
  security WPA2/WPA3 and password.
- On the laptop, join the hotspot network like any Wi-Fi.
- **USB tethering** (more stable, charges the phone): plug in › Android: Hotspot & tethering › USB
  tethering; iPhone: Personal Hotspot on, then trust the computer.

## Save data
- Windows: Settings › Network & internet › Wi-Fi › the hotspot › **Metered connection** on (pauses
  big updates and OneDrive sync). Mac: Wi-Fi details › Low Data Mode.
- Rough use: video call ~1 GB/hour (HD more), email/web ~50-150 MB/hour, Windows/macOS updates
  several GB. Check your plan's hotspot allowance; some plans cap or slow tethering.

## Gotchas
- Hotspots drain the phone battery fast; plug it in.
- Turn it off when done; nearby devices may auto-join and use your data.
- A hotspot is safer than open café Wi-Fi for banking.

## Verify
- [ ] Laptop shows the hotspot connection as metered; phone shows connected device count.
