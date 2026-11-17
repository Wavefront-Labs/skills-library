---
id: computing-software.digital-privacy-hygiene.device-hardening.hotel-room-device-security
name: hotel-room-device-security
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, hotel-device-security, travel-security, evil-maid, physical-security]
level: practitioner
status: draft
description: "Protect laptops and phones in hotel rooms and while travelling: power-off encryption state, carrying vs safes, hotel Wi-Fi, charging and TV casting hygiene."
sources:
  - "https://ssd.eff.org/module/things-consider-when-crossing-us-border"
  - "https://www.cisa.gov/secure-our-world"
  - "https://www.ncsc.gov.uk/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hotel room device security

**Goal:** don't let a room left alone for a day become access to your devices.

## Leaving the room
- **Take devices with you** when practical. If not, shut them **fully down** (not sleep): full-disk encryption only
  protects data at rest, and a powered-off phone is in its strongest (before first unlock) state.
- Room safes have master override codes and are not a strong barrier against staff or a determined intruder; they
  deter casual theft only.
- Optionally photograph the laptop's position and screws, or use tamper-evident tape on the case, to notice
  tampering.
- Set a firmware password and Secure Boot so the laptop can't be booted from USB.

## In the room
- Hotel Wi-Fi: use a VPN; avoid logging into new accounts; prefer your phone's hotspot.
- Room TVs with casting or app logins: sign out of Netflix/YouTube before checkout; prefer casting from your phone
  over logging into the TV.
- Charging: use your own charger and the wall socket; avoid unknown USB ports or cables (use a data blocker if you
  must).
- Don't use the business centre PC for anything requiring a login.

## Signs of tampering
Device warm, rebooted, in a different position, new USB device listed, unexpected disk unlock prompts. Treat the device
as potentially compromised; change passwords from another device.

## Higher risk
Journalists and executives in high-risk countries: travel with a clean loaner device and minimal accounts.
