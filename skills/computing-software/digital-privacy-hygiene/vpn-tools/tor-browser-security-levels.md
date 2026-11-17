---
id: computing-software.digital-privacy-hygiene.vpn-tools.tor-browser-security-levels
name: tor-browser-security-levels
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, tor-security-level, tor-browser, tor, javascript, safest-mode, new-circuit, add-ons, opsec]
level: practitioner
status: docs-checked
description: "Choose Tor Browser's Standard, Safer or Safest level, request a new circuit, and avoid habits (add-ons, personal logins, opening downloads online) that undo Tor's anonymity."
sources:
  - "https://support.torproject.org/security-settings/"
  - "https://ssd.eff.org/module/how-to-use-tor"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tor Browser security levels and habits

**Goal:** use Tor Browser so its protections actually hold.

## Security levels (shield icon, then Settings)
| Level | What changes | Use when |
|---|---|---|
| Standard (default) | All browser and website features enabled | Everyday anonymous browsing |
| Safer | JavaScript off on non-HTTPS sites; some fonts and math symbols off; audio/video click-to-play | Cautious use |
| Safest | Only features needed for static sites and basic services; JavaScript off by default on all sites; some fonts, icons, math symbols and images off | Higher risk; EFF says it guards against well-funded attackers and unknown bugs but can make some sites unusable |

On Android: three-dot menu, Privacy and security, Security Level, pick a level, Save and restart. Levels can be reverted the same way.

## Circuits
- The circuit button in the URL bar (next to the lock) shows your three relays and lets you request new ones.
- Exit nodes may be monitored; that reveals the exit operator's view, not who you are. HTTPS and Tor are complementary (HTTPS-only mode is on by default).

## Habits that break anonymity
- Logging in or entering personal information: the site can identify you and learn you use Tor.
- Installing extra add-ons: they can de-anonymise you, and Tor already ships privacy rules (no extra ad or tracker blockers needed).
- Opening downloaded documents while online: some load internet resources outside Tor and can reveal your IP address.
- Expecting other apps to be covered: only activity inside Tor Browser is anonymised.
- Downloading Tor Browser from anywhere but the official Tor Project site, or accepting alternative certificates when prompted.

## Gotchas
- `.onion` addresses are not tied to a public IP and give end-to-end encryption.

## Checked
Method: 2026-11-08 read both cited pages. Levels table and Android steps follow the Tor support page; circuit, add-on, login, download and onion points follow the EFF page. Dropped as unsupported by either page: the JavaScript-exploit history claim, New Identity details, letterboxing/resizing, torrenting, check.torproject.org, CAPTCHAs.
