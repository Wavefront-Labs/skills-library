---
id: computing-software.digital-privacy-hygiene.vpn-tools.nextdns-profile-with-blocklists
name: nextdns-profile-with-blocklists
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, nextdns, dns-privacy, encrypted-dns, dns-blocklists, tracker-blocking, parental-controls, android-private-dns, ios-dns-profile, dns-logs]
level: practitioner
status: draft
description: "Set up a NextDNS profile with privacy blocklists, logging off or short retention, and install it on phones, computers and the router, with an allowlist for breakages."
sources:
  - "https://help.nextdns.io/"
  - "https://www.privacyguides.org/en/dns/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NextDNS profile with blocklists

**Goal:** network-wide tracker/ad/malware blocking that follows your devices off the
home network, with encrypted DNS.

## Profile setup
1. Create an account at `my.nextdns.io` (alias email fine). Each **configuration** has an
   ID like `abc123`.
2. **Security** tab: threat intelligence feeds, Google Safe Browsing, cryptojacking,
   typosquatting, newly registered domains (aggressive but effective), parked domains.
3. **Privacy** tab: add blocklists, start with one solid list (e.g. "NextDNS Ads &
   Trackers" or "OISD"); stacking many lists adds breakage. Enable **native tracking
   protection** for your device brands (Apple, Samsung, Windows, etc.).
4. **Settings** tab: **Logs** off, or on with short retention (1 hour - 1 day) and storage
   location chosen; logs are useful for debugging breakage.
5. Optional **Parental Control** tab for children's devices (separate configuration).

## Install
- **Android**: Settings > Network > Private DNS > hostname `abc123.dns.nextdns.io`.
- **iOS/macOS**: download the configuration profile from `apple.nextdns.io` and install.
- **Windows**: NextDNS app, or Windows DoH with the configuration's DoH URL.
- **Router**: NextDNS CLI on OpenWrt/Ubiquiti or linked IP; gives per-device names.
Name devices (e.g. `abc123-pixel` style hostnames or via the app) so logs show who's who.

## Handle breakage
Logs > find blocked domain at the time of the failure > **Allowlist** it. Typical
culprits: email link trackers (click redirect domains), shopping sites' CDNs.

## Gotchas
- Free tier has a monthly query cap; heavy households need the paid plan.
- A VPN's own DNS overrides Private DNS on Android when connected; choose one.

## Verify
- [ ] `test.nextdns.io` shows status "ok" and your configuration ID on each device.
- [ ] A known tracker domain fails to resolve.
