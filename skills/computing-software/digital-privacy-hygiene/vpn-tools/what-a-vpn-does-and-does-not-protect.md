---
id: computing-software.digital-privacy-hygiene.vpn-tools.what-a-vpn-does-and-does-not-protect
name: what-a-vpn-does-and-does-not-protect
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-limitations, vpn, vpn-selection, threat-model, isp-tracking, browser-fingerprinting, tor, anonymity]
level: intro
status: draft
description: "Explain what a commercial VPN actually changes (who sees your traffic metadata) and what it doesn't (logins, cookies, fingerprinting, malware, anonymity), before anyone buys one."
sources:
  - "https://ssd.eff.org/module/choosing-vpn-thats-right-you"
  - "https://www.privacyguides.org/en/basics/vpn-overview/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# What a VPN does and doesn't protect

**Goal:** set expectations so a VPN is bought for the right reason, or not at all.

## What it does
A VPN moves trust from your **local network and ISP** to the **VPN provider**.
- Your ISP / hotel / café Wi-Fi sees only encrypted traffic to the VPN server, not which
  sites you visit (DNS included, if configured correctly).
- Websites see the VPN server's IP, not your home IP: coarse location hidden, IP-based
  rate limits and geo-blocks bypassed.
- Useful on hostile networks, against ISP logging/ad injection, and for censorship
  circumvention (sometimes).

## What it doesn't do
- **Not anonymity**: logged-in accounts, cookies, and browser fingerprinting still
  identify you. The VPN provider itself sees your real IP and destinations.
- **Not security against phishing or malware**; "threat protection" add-ons are basic
  DNS blocklists.
- **Not encryption of the sites themselves**: HTTPS already encrypts content; the VPN
  hides metadata.
- **Not protection from a provider that logs**: you trust their no-logs claim.
- Doesn't stop apps from sending data to their own servers.

## Do you need one?
| Goal | Better tool |
|---|---|
| Hide browsing from ISP / public Wi-Fi | VPN (or encrypted DNS + HTTPS for partial) |
| Anonymity against sites and network | Tor Browser |
| Stop ad tracking | Content blocker, browser choice |
| Watch other-country streaming | VPN (terms of service issues) |
| Secure bank login on café Wi-Fi | HTTPS already does this; VPN optional |

## Verify
- [ ] The person can state which adversary the VPN addresses (ISP/local network) for
      their use case.
