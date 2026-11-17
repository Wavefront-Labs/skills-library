---
id: computing-software.digital-privacy-hygiene.vpn-tools.safari-privacy-settings
name: safari-privacy-settings
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, safari-privacy, browser-hardening, icloud-private-relay]
level: practitioner
status: draft
description: "Configure Safari's privacy settings on Mac and iPhone: tracking and fingerprinting protection in all browsing, Hide IP, profiles, search engine and locked private tabs."
sources:
  - "https://support.apple.com/guide/safari/prevent-cross-site-tracking-sfri40732/mac"
  - "https://support.apple.com/guide/iphone/browse-the-web-privately-iphb01fc3c85/ios"
  - "https://webkit.org/blog/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Safari privacy settings

**Goal:** turn on Safari's strongest built-in protections, most of which default to private browsing only.

## macOS (Safari > Settings)
- **Privacy:** Prevent cross-site tracking on; **Hide IP address** from trackers (or trackers and websites with
  iCloud Private Relay).
- **Advanced:** "Use advanced tracking and fingerprinting protection" set to **in all browsing** (default is
  Private Browsing only). This also strips known tracking parameters from links.
- **Search:** search engine DuckDuckGo; turn off "Include search engine suggestions" and "Safari Suggestions" if
  you don't want queries shared.
- **Websites:** camera, mic, location, notifications set to Ask/Deny.
- **Profiles:** separate Personal/Work profiles with separate cookies and history.

## iPhone (Settings > Apps > Safari)
- Prevent Cross-Site Tracking on; Hide IP Address.
- Advanced > **Advanced Tracking and Fingerprinting Protection: All Browsing**.
- **Require Face ID to Unlock Private Browsing** on.
- Search engine; Search Engine Suggestions off.
- Content blockers: add a blocker app (see content-blocker skill).

## Verify
Visit a page with UTM parameters from a link in Messages/Mail; the parameters are removed. Privacy Report (shield
icon) shows blocked trackers.

## Gotchas
- Fingerprinting protection in all browsing can break a few sites; toggle "Reload Without Privacy Protections" per
  page.
- Hide IP with Private Relay needs iCloud+.
