---
id: computing-software.digital-privacy-hygiene.vpn-tools.android-system-wide-tracker-blocking
name: android-system-wide-tracker-blocking
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, android-tracker-blocking, tracker-blocking, android-private-dns]
level: practitioner
status: draft
description: "Block trackers across all Android apps using Private DNS blocklists or local-VPN firewalls like RethinkDNS, and handle the VPN-slot conflict."
sources:
  - "https://www.privacyguides.org/en/dns/"
  - "https://rethinkdns.com/"
  - "https://trackercontrol.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Android system-wide tracker blocking

**Goal:** block tracking and ad domains inside apps, not just in the browser.

## Option 1: Private DNS with a filtering resolver (simplest)
Settings > Network & internet > **Private DNS** > Private DNS provider hostname:
- `dns.adguard-dns.com` (ads/trackers), `<id>.dns.nextdns.io` (your own blocklists), `dns.mullvad.net`
  variants (`adblock.dns.mullvad.net`).
Works with a VPN app at the same time (unless the VPN forces its own DNS).

## Option 2: Local-VPN firewall apps
- **RethinkDNS:** DNS blocklists + per-app firewall (block an app's internet, or only on mobile data).
- **TrackerControl:** shows which companies each app contacts; blocks trackers per app.
- **AdGuard for Android:** paid, filtering + HTTPS filtering (avoid HTTPS filtering for privacy-sensitive apps).
These occupy Android's single VPN slot; you can't run them alongside a real VPN unless the app chains to a
WireGuard upstream (RethinkDNS supports WireGuard proxies).

## Choose
| Need | Pick |
|---|---|
| Set-and-forget | Private DNS filtering |
| Per-app visibility and blocking | RethinkDNS / TrackerControl |
| Also using a VPN | Private DNS or VPN provider's blocking |

## Gotchas
- DNS blocking can't block trackers served from the same domain as content (first-party).
- Some apps break (login, payments); allowlist domains in the resolver dashboard.
- Private DNS hostnames must support DNS-over-TLS.
