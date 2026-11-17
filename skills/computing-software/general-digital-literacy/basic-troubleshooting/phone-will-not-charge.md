---
id: computing-software.general-digital-literacy.basic-troubleshooting.phone-will-not-charge
name: phone-will-not-charge
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-mobile, phone-not-charging, charging-port, battery-health]
level: intro
status: draft
description: "Fix a phone that will not charge or charges slowly: test cable, brick and outlet, clean lint from the port safely, check moisture warnings and battery health."
sources:
  - https://support.apple.com/en-us/102357
  - https://support.google.com/pixelphone/answer/7158570
  - https://www.samsung.com/uk/support/mobile-devices/what-to-do-if-my-phone-is-not-charging/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Phone will not charge

## Isolate the part
1. Different **outlet** (not a laptop's sleepy USB port or a cheap power strip).
2. Different **cable** (cables fail first, especially at the ends).
3. Different **charger** — use a decent USB-C PD brick (20 W+ for iPhone fast charge).
4. Wireless charging works but cable doesn't → the port.

## Clean the port
- Pocket lint packs into Lightning/USB-C ports so the plug no longer clicks in fully.
- Power off. Look in with a torch. Gently scrape with a **wooden toothpick** or plastic interdental pick along the walls, not the centre contacts. No metal pins, no compressed air blasting straight in, no liquids.

## Other causes
- **Moisture detected** (Samsung/iPhone liquid alert): unplug, let it dry for a few hours; don't use rice or a hairdryer. Emergency override exists but risks corrosion.
- **Too hot/cold**: charging pauses above ~35°C; *Charging on Hold* message. Let it cool.
- **Optimised/Adaptive charging** holds at 80% overnight — normal. iPhone 15+ can set an 80% limit.
- Software: force restart; update OS.
- Accessory not supported (iPhone): non-certified cable; use MFi or USB-C cables.

## Battery
- iPhone: Settings › Battery › **Battery Health** (below 80% = replace). Android: Settings › Battery (Samsung Members app › Diagnostics; Pixel › Battery diagnostics).
- Swollen battery (case bulging, screen lifting): stop charging, don't puncture, take to a repairer.

## Verify
- [ ] Plugging in shows the charging symbol immediately and the percentage rises within minutes.
