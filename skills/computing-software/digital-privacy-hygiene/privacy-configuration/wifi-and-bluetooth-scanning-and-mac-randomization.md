---
id: computing-software.digital-privacy-hygiene.privacy-configuration.wifi-and-bluetooth-scanning-and-mac-randomization
name: wifi-and-bluetooth-scanning-and-mac-randomization
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, wifi-bluetooth-scanning, mac-randomization, location, android, ios, windows, bluetooth]
level: intro
status: docs-checked
description: "Limit tracking across Wi-Fi networks with MAC address randomization on iPhone, Mac and Android: what each setting does, defaults, and when to turn it off."
sources:
  - "https://support.apple.com/en-us/102509"
  - "https://source.android.com/docs/core/connect/wifi-mac-randomization-behavior"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi MAC address randomization

**Goal:** stop networks and sensors recognising the same device everywhere. Sources: Apple Support "Use private
Wi-Fi addresses on Apple devices" (published 2025-12-05) and the Android Open Source Project page "MAC randomization
behavior".

## Why
A device identifies itself to a Wi-Fi network with a MAC address. Apple: if it always used the same MAC across
networks, operators and observers could relate the address to the device's activity and location over time. Android:
MAC addresses are transmitted without encryption and the factory MAC is globally unique and static, so it can be
used to track location.

## Apple devices (iOS 14 and later; the three-way setting needs iOS 18, macOS Sequoia 15)
- By default the device uses a different private address for each Wi-Fi network.
- iPhone: Settings > Wi-Fi > More Info button next to the network (tap Edit first if not connected) > Private Wi-Fi
  Address. On iOS 18 choose Off, Fixed or Rotating; earlier versions have an on/off toggle.
- Mac (macOS Sequoia 15 or later): System Settings > Wi-Fi > Details/More Info next to the network > Private Wi-Fi
  Address.
- **Off** uses the hardware MAC. **Fixed** uses a private address that does not rotate; it is the default on a new
  network with WPA2 or stronger security. **Rotating** changes the private address every 2 weeks; it is the default on
  a network with weak or no security.
- Resetting network settings or erasing the device produces a new private address next time. From iOS 18, forgetting
  a network also forgets its address unless the network was forgotten less than 24 hours ago.
- If a network will not work, Apple says to install the latest updates and retry before turning the feature off;
  organisations can use an MDM profile to disable it.

## Android
- Android 10 and later use a randomized MAC address by default. Settings > the network's details screen lets you
  enable or disable randomization for each network; disabling it uses the factory MAC.
- Default is persistent randomization: an address derived from the network profile (SSID, security type) that stays
  the same until a factory reset, even if you forget and re-add the network. Networks that rely on a stable MAC
  (remembering your device, skipping a login page, parental controls) need this.
- From Android 12, non-persistent randomization (a new address at the start of connections, re-randomized after
  certain DHCP-lease or 24-hour conditions) is used when a network suggestion app requests it, or for open networks
  only if a device overlay is enabled (off by default). On Android 11 and higher you can force it for all networks
  via Settings > Developer Options > Wi-Fi non-persistent MAC randomization.

## Use the real MAC only where required
Turn randomization off for a specific network only if it needs a known MAC (for example MAC filtering).

## Verify
- [ ] Private Wi-Fi Address (Apple) or randomized MAC (Android) is on for every network except those that need it.

## Checked
Checked 2026-11-08 against the full text of both cited pages. The EFF Android settings guide was read and contains
nothing on Wi-Fi scanning or MAC randomization, so it was dropped from sources. This revision is limited to
MAC randomization; the earlier sections on Android background Wi-Fi/Bluetooth scanning, iPhone System Services,
Windows 11 random hardware addresses and Bluetooth habits are not supported by these pages and were removed.
Method: documentation only; no commands were run.
