---
id: computing-software.digital-privacy-hygiene.vpn-tools.auditing-and-minimising-browser-extensions
name: auditing-and-minimising-browser-extensions
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, extension-audit, malicious-extensions, tracker-blocking, browser-permissions, extension-ownership-change, site-access, chrome-extensions, firefox-addons]
level: practitioner
status: draft
description: "Review every installed browser extension's permissions, publisher and update history, cut to the minimum, and restrict site access so a sold or hijacked extension can't read everything."
sources:
  - "https://www.privacyguides.org/en/browser-extensions/"
  - "https://support.google.com/chrome_webstore/answer/2664769"
  - "https://support.mozilla.org/en-US/kb/permission-request-messages-firefox-extensions"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auditing browser extensions

**Goal:** an extension with "read and change all your data on all websites" sees every
password page and bank statement. Extensions are bought by adware companies and
pushed malicious updates silently.

## Audit (every 6 months)
1. Open `chrome://extensions` / `about:addons` / `edge://extensions`.
2. For each extension ask:
   - Used in the last month? If not, **remove** (don't just disable).
   - Publisher still the same, open source, many users, recent reviews not complaining of
     ads/redirects? Sudden 1-star reviews often mean a hostile ownership change.
   - Permissions: "all sites" needed? Coupon, PDF, screenshot, "VPN" and free AI helper
     extensions are classic data harvesters.
3. Keep a short list: password manager, uBlock Origin, maybe one or two others.
Privacy Guides' position: avoid extensions that duplicate browser protections; they
add fingerprint surface.

## Restrict site access
- Chrome/Edge: Details > **Site access** > "On click" or "On specific sites".
- Firefox: Manage > Permissions > optional "Access your data for all websites" toggle
  (MV3 add-ons), and per-site access from the extensions button.
Password managers and blockers need broad access; most others don't.

## Signs of a compromised extension
New tabs/ads, search engine changed, redirects through affiliate links, browser slow,
unknown "managed by your organisation" message (check `chrome://policy`).

## Gotchas
- Sync re-installs removed extensions from another device; remove everywhere.
- Enterprise policies can force-install extensions; on a personal device, any forced
  extension you didn't add is malware.

## Verify
- [ ] Extension count reduced; each remaining one justified.
- [ ] Non-essential extensions limited to "on click".
