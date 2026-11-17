---
id: computing-software.it-support-helpdesk.desktop-support.mobile-battery-drain-and-overheating
name: mobile-battery-drain-and-overheating
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, mobile-device-support, mobile-battery-drain, battery-health, overheating, swollen-battery, background-app-refresh, ios, android, comptia-a-plus]
level: intro
status: draft
description: "Diagnose phone and tablet battery drain and overheating: battery usage by app, battery health/maximum capacity, background activity, charging faults, and swollen battery safety."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://support.google.com/android/"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mobile-battery-drain-and-overheating

Goal: separate "an app is draining it" from "the battery is worn" from "the
battery is dangerous".

## Safety first
Swollen battery (screen lifting, back bulging, case no longer flat), smell,
or device too hot to hold → power off, don't charge, don't puncture, keep
away from flammables, send for replacement/recycling. Never press a
swollen phone flat.

## Usage evidence
- iOS: Settings → Battery — per-app usage and "Activity" (screen on vs
  background) for 24 h / 10 days.
- Android: Settings → Battery → Battery usage — per app, plus "Adaptive
  battery".
An app with high background use = misbehaving (location, sync loops).
Common corporate culprits: VPN apps always-on, MDM agents retrying a
failing check-in, Outlook syncing a huge mailbox, Teams with bad
connectivity.

## Battery health
- iOS: Settings → Battery → Battery Health → Maximum Capacity; < 80 % is
  "significantly degraded"; "Peak performance capability" messages mean
  throttling.
- Android: varies — Samsung Members → Diagnostics, Pixel Settings → Battery
  → Battery health (newer models), or dialer codes on some vendors.
Batteries are consumables (~500 full cycles); replace instead of chasing
settings.

## Fixes for drain
1. Update OS and apps.
2. Restrict background activity for the top offenders (iOS: Background App
   Refresh off per app; Android: Battery → app → Restricted).
3. Location → "While using" instead of "Always" for apps that don't need it.
4. Poor signal areas burn battery (radio at max power) — common in
   basements; Wi-Fi calling helps.
5. If drain persists after a restart and offender fix: backup and restore
   (iOS) or check for a rogue profile/app.

## Overheating
Heavy use while charging, direct sun, car dashboards, thick cases during
fast charge. Fast-charge heat is normal-ish; heat when idle and not charging
is not → check battery usage for a runaway app, then hardware.

## Charging faults
Lint in Lightning/USB-C port (wooden toothpick, power off), damaged cable,
uncertified chargers; "Accessory not supported" = cable. Test with known
good cable/charger.

## Verify
Over the next normal day the device ends with > 20 % and no app dominates
background usage; health above replacement threshold or replacement booked.
