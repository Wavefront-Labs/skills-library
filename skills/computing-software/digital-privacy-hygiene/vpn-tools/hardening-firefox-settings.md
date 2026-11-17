---
id: computing-software.digital-privacy-hygiene.vpn-tools.hardening-firefox-settings
name: hardening-firefox-settings
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, firefox-hardening, arkenfox, privacy-browser, browser-hardening, firefox, enhanced-tracking-protection, telemetry]
level: practitioner
status: docs-checked
description: "Harden Firefox from the settings UI: Strict tracking protection, telemetry and search suggestions off, HTTPS-Only, DNS over HTTPS, sanitize on close."
sources:
  - "https://www.privacyguides.org/en/desktop-browsers/#firefox"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening Firefox

**Goal:** a daily browser with strong tracking protection that still works on normal sites. Settings below follow
Privacy Guides' "Recommended Firefox Configuration" (Settings in Firefox).

## Search
- Uncheck **Show search suggestions**: suggestions send everything you type in the address bar to the default
  search engine, even if you never submit a search.
- If the new address-bar options exist, also uncheck **Suggestions from Firefox** and **Suggestions from sponsors**
  (Firefox Suggest); some of it is regional.

## Privacy & Security
- **Enhanced Tracking Protection: Strict.** It blocks social media trackers, fingerprinting scripts, cryptominers
  and cross-site tracking cookies, but not all fingerprinting and not all tracking.
- **Sanitize on close:** check "Delete cookies and site data when Firefox is closed". It removes persistent
  cookies, not cookies gathered during one session. Use Cookies and Site Data > Manage Exceptions to stay logged in
  to chosen sites.
- **Telemetry:** uncheck "Send technical and interaction data to Mozilla", "Allow personalized extension
  recommendations", "Install and run studies", "Send daily usage ping to Mozilla" and "Automatically send crash
  reports".
- **HTTPS-Only Mode:** enable in all windows, so you don't connect to a site over plain HTTP by accident.
- **DNS over HTTPS:** if you use a DoH provider, choose **Max Protection** and a provider. Max Protection enforces
  DoH and shows a warning if Firefox cannot reach the resolver, stopping a network from silently downgrading it.
- **Sync:** Firefox Sync protects synced data with end-to-end encryption (Privacy Guides).

## Arkenfox (advanced)
Arkenfox is a set of Firefox options; some are strict and can break sites, and Privacy Guides strongly recommends
reading its wiki first. It only targets basic fingerprinting scripts and does not make you blend in with a crowd the
way Mullvad Browser or Tor Browser do. Firefox is more flexible (per-site exceptions to stay logged in).
Privacy Guides suggests Mullvad Browser for advanced anti-fingerprinting, or both browsers for different uses.

## Gotchas
- Hardening beyond Firefox's defaults can break sites; change one thing at a time.

## Checked
2026-11-01. Confirmed on Privacy Guides "Desktop Browsers" (Firefox section): every setting above and the Arkenfox
and Mullvad Browser notes. Removed: Global Privacy Control, passwords-off, uBlock Origin advice, Total Cookie
Protection wording, Home page settings, `user.js` update steps and override examples (Arkenfox wiki page read was
only a stub), the verification sites. The Mozilla support page was blocked.
Method: documentation only; no commands were run.
