---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-local-network-access
name: vpn-local-network-access
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-lan-access, vpn-configuration, kill-switch]
level: practitioner
status: draft
description: "Reach printers, NAS and casting devices while a VPN is on: local network sharing toggles, kill-switch interaction, and the public Wi-Fi risk."
sources:
  - "https://mullvad.net/en/help/using-mullvad-vpn-app"
  - "https://protonvpn.com/support/allow-lan-connections"
  - "https://developer.android.com/develop/connectivity/vpn"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VPN local network access

**Goal:** keep the VPN on at home without breaking printing, AirPlay/Chromecast, NAS shares or the router admin page.

## Settings by client
- **Mullvad:** Settings > VPN settings > **Local network sharing** on.
- **Proton VPN:** Settings > Advanced/Connection > **Allow LAN connections** (with kill switch, Advanced Kill
  Switch may still block; check).
- **WireGuard raw config:** exclude the LAN from `AllowedIPs` or rely on OS route for the directly connected subnet;
  the Windows client's "Block untunneled traffic" also blocks LAN.
- **Android:** "Block connections without VPN" blocks LAN for many apps unless the VPN app permits local traffic.
- **iOS:** VPN apps may set `excludeLocalNetworks`; behaviour depends on the app.

## Risk trade-off
| Network | LAN sharing |
|---|---|
| Home | On |
| Office/hotel/café | Off (others on the LAN can reach your device) |

## Troubleshooting casting
mDNS/SSDP discovery needs multicast on the LAN; even with sharing on, some clients block multicast. Test casting
with the VPN paused to confirm the VPN is the cause.

## Gotchas
- LAN sharing allows RFC1918 ranges; if your café uses the same range as your home LAN you're exposed there too:
  turn it off when you leave home.
- Router admin pages at 192.168.x.1 need LAN sharing.
