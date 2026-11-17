---
id: computing-software.digital-privacy-hygiene.privacy-configuration.icloud-private-relay-setup
name: icloud-private-relay-setup
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, icloud-private-relay, apple, icloud-plus, ip-address, safari, dns]
level: intro
status: docs-checked
description: "Understand what iCloud Private Relay does: two-relay design, encrypted DNS, Safari scope, and the sign-in friction it can cause."
sources:
  - "https://support.apple.com/en-us/102602"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iCloud Private Relay setup

**Goal:** know what Private Relay protects, so you can decide whether it fits your threat model.

## How it works
- Private Relay is part of an iCloud+ subscription and protects browsing in Safari.
- Design aim: when you browse in Safari, no single party, not even Apple, can see both who you are and which
  sites you visit.
- Requests go through two separate relays:
  - The first relay is operated by Apple. Your IP address is visible to your network provider and to this relay.
    Your DNS records are encrypted, so neither can see the address of the site you want.
  - The second relay is operated by a third-party content provider. It generates a temporary IP address, decrypts
    the site name you requested, and connects you to the site.

## Limits to plan for
- Not available in all countries or regions.
- Without your IP address, some websites may need extra steps to sign in or access content.
- Private Relay uses a single secure connection, so multi-connection network speed tests can read lower while it
  is on; Apple says real browsing stays fast.
- Apple publishes separate guidance for website owners, network administrators and app developers on supporting
  Private Relay users. That page was not read.

## Verify
- [ ] You know it covers Safari browsing, not a device-wide tunnel.

## Checked
2026-11-09. Confirmed against Apple Support "About iCloud Private Relay" (read in full). Removed: all menu paths,
the IP location setting names, the per-network setting, coverage of other apps and browsers, the blocked-domain
note, the VPN comparison and the CAPTCHA advice, because the Apple page does not state them. Dropped sources: the
Apple December 2021 PDF (unreadable as text) and the Privacy Guides VPN page (not about this product).
Method: documentation only; no commands were run.
