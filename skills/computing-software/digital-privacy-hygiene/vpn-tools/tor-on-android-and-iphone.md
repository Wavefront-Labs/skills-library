---
id: computing-software.digital-privacy-hygiene.vpn-tools.tor-on-android-and-iphone
name: tor-on-android-and-iphone
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, orbot, onion-browser, tor-browser-android, tor, tor-mobile, bridges, ios]
level: practitioner
status: docs-checked
description: "Use Tor on phones: Tor Browser on Android, Onion Browser (with or without Orbot) on iPhone, bridges, security levels and their limits."
sources:
  - "https://ssd.eff.org/module/how-to-use-tor-on-android-and-iphone"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tor on Android and iPhone

**Goal:** anonymous or censorship-resistant browsing from a phone.

## Android
- Install the Tor Browser app from the Google Play Store, or from the links on Tor's official download page.
  Searching app stores turns up many for-profit apps that the Tor Project may not endorse and that can bundle
  unvetted VPNs.
- Open it and tap Connect. Only browsing inside the app goes through Tor; other apps are not routed through it.
- Security level: three-dot menu, Settings, Security Level. Standard blocks many known issues and uses HTTPS-only
  mode and NoScript by default. Safest disables many website features, protects against well-funded attackers and
  unknown bugs in those features, but can make some sites unusable.
- If Tor is blocked, three-dot menu, Settings, Tor Network, Config Bridge offers obfs4, Snowflake (looks like a
  video or voice call) and meek-azure (looks like browsing a Microsoft site; very slow, a last resort). You can also
  enter a bridge address from a trusted source, such as the Tor Project's bridge list.

## iPhone
- Tor does not make a Tor Browser for iPhone because of iOS limitations. The Tor Project recommends Onion Browser,
  an open-source browser that connects to Tor directly in the app or through a second app, Orbot, which creates a
  VPN profile to route the device's traffic through Tor (Orbot is not a VPN provider and is free).
- Apple requires iOS browsers to use WebKit, so Onion Browser alone cannot match Tor Browser's protections on other
  platforms. Orbot can shore up some leaks in how iOS handles audio and video and protect your IP address better,
  but adds technical setup. Choose "Use built-in Tor" for the simpler path.
- The shield icon offers Gold, Silver and Bronze levels. EFF recommends Gold where possible: it disables
  JavaScript, protecting against sites using JavaScript to find your IP address, but breaks some sites.
- EFF's page carried a warning dated 5 August 2026 about a WebKit flaw that can expose real IP addresses, including
  in Onion Browser, advising against Onion Browser on iOS for highly sensitive browsing until Apple fixes it.
  Re-check the current EFF page before relying on it.

## Gotchas
- Logging in or filling forms with personal information lets a site identify you and know you use Tor.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense page "How to use Tor on Android and iPhone" (page text read from the intro warning through the Onion Browser security-level section). Dropped as unconfirmed: Orbot per-app routing on Android, F-Droid and Guardian Project distribution, the iOS memory-limit claim, one-VPN-at-a-time and battery notes, advertising-ID/SIM identifiers, and the check.torproject.org and Orbot verification steps. The Guardian Project and onionbrowser.com sources were removed because they were not read.
