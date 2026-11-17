---
id: computing-software.digital-privacy-hygiene.vpn-tools.stripping-tracking-parameters-from-links
name: stripping-tracking-parameters-from-links
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, tracking-parameters, tracker-blocking, enhanced-tracking-protection]
level: practitioner
status: draft
description: "Remove utm, fbclid, gclid, si and similar tracking parameters from links you click and share, with browser features, uBO filters and manual cleaning."
sources:
  - "https://github.com/gorhill/uBlock/wiki/Static-filter-syntax#removeparam"
  - "https://support.mozilla.org/kb/enhanced-tracking-protection-firefox-desktop"
  - "https://webkit.org/blog/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Stripping tracking parameters from links

**Goal:** links you click and share don't carry identifiers that tie you (or the person you share with) to a click.

## Common parameters
`utm_source/medium/campaign`, `fbclid` (Meta), `gclid`/`gbraid`/`wbraid` (Google Ads), `msclkid` (Microsoft),
`mc_eid` (Mailchimp), `igshid`/`igsh` (Instagram), `si` (YouTube/Spotify share links), `ttclid` (TikTok),
`_hsenc` (HubSpot).

## Automatic
- **Firefox:** Enhanced Tracking Protection **Strict** strips known tracking parameters (also in private windows).
  "Copy Clean Link" in the link context menu.
- **Safari:** Advanced Tracking and Fingerprinting Protection (all browsing) removes known parameters.
- **Brave:** query parameter filtering and debouncing on by default.
- **uBlock Origin:** enable the "AdGuard/uBlock filters - URL Tracking Protection" list (Filter lists >
  Privacy). Custom: `*$removeparam=utm_source`.

## Manual when sharing
Delete everything from `?` onward, then check the link still works (some sites need `?v=` or `?id=` to function,
e.g. YouTube `watch?v=ID` must keep `v`).

## Gotchas
- Some tracking IDs are in the path (`/ref=...`) or shortened via redirect services; expand short links first.
- Email links often go through click-tracking redirect domains; parameter stripping doesn't remove that hop.
