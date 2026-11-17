---
id: computing-software.digital-privacy-hygiene.vpn-tools.always-on-vpn-on-android-and-ios
name: always-on-vpn-on-android-and-ios
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, always-on-vpn, vpn-on-demand, kill-switch, vpn-configuration, block-connections-without-vpn, android, ios, wireguard]
level: practitioner
status: draft
description: "Make the VPN mandatory on phones: Android Always-on + Block connections without VPN, and iOS On Demand rules, plus the leaks each platform still has."
sources:
  - "https://support.google.com/android/answer/9089766"
  - "https://developer.android.com/develop/connectivity/vpn#always-on"
  - "https://support.apple.com/guide/deployment/vpn-overview-depae3d361d0/web"
  - "https://mullvad.net/en/blog/android-leaks-connectivity-check-traffic"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Always-on VPN on Android and iOS

**Goal:** no traffic leaves the phone outside the tunnel, including during reconnects.

## Android
1. Settings > Network & internet > **VPN** > gear icon next to your VPN app.
2. **Always-on VPN**: on. **Block connections without VPN**: on (this is the OS kill switch).
3. In the VPN app, disable its own "local network" or "split tunnel" exceptions unless needed.
Known caveat: Android sends some **connectivity checks** and certain system traffic
outside the tunnel even with blocking enabled (documented by Mullvad, 2022). Disable
"Wi-Fi connectivity check" where the ROM allows (GrapheneOS does).

## iOS / iPadOS
- Most VPN apps install a profile with **Connect On Demand** rules (connect automatically
  on any network). Turn on in the app ("Auto-connect", "Always on") or Settings > VPN >
  (i) > Connect On Demand.
- iOS has no user-facing full kill switch; some apps enable Apple's
  `includeAllNetworks` mode (labelled "Kill switch") which routes all traffic through
  the tunnel but can break AirDrop/CarPlay/local network features. Known issue: existing
  connections may persist outside the tunnel after it's established; researchers
  reported this for years.
- Supervised devices (MDM) can enforce Always On VPN.

## Gotchas
- Battery optimisations can kill the VPN app on some Android OEMs; exempt it.
- Captive portals (hotel Wi-Fi) need the VPN paused briefly to log in; re-enable.

## Verify
- [ ] Android: disable VPN in the app; internet stops (blocked).
- [ ] Both: IP check site shows VPN IP after reboot without opening the app.
