---
id: computing-software.digital-privacy-hygiene.vpn-tools.fixing-site-breakage-from-blockers
name: fixing-site-breakage-from-blockers
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, site-breakage, ublock-origin, tracker-blocking, content-blocking]
level: practitioner
status: draft
description: "Diagnose which blocker breaks a site, fix it per site with uBlock Origin, Firefox tracking protection or Brave Shields, and report filter bugs."
sources:
  - "https://github.com/gorhill/uBlock/wiki/Quick-guide:-popup-user-interface"
  - "https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop"
  - "https://brave.com/shields/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fixing site breakage per site

**Goal:** keep strict blocking everywhere and loosen it only where needed.

## Find the cause
1. Reload in a private window with extensions off (Firefox: private windows run only allowed extensions). Works?
   Then a blocker is the cause.
2. Toggle blockers one at a time: uBlock Origin, then browser tracking protection (Firefox shield icon / Brave
   Shields), then any privacy extension or DNS filter.
3. DNS-level filters (NextDNS, Pi-hole) break things too: check their logs for the blocked domain.

## Fix with the smallest change
- **uBlock Origin:** open the popup, open the **logger** (list icon), reproduce, look for red rows. Then either
  - in medium mode, set the needed third-party domain to noop (grey) for this site and click the padlock to save; or
  - add an exception in My filters: `@@||cdn.example.net^$domain=shop.example`.
  As a last resort, click the big power button to disable uBO for the site.
- **Firefox:** shield icon > turn off Enhanced Tracking Protection for this site (with Strict mode).
- **Brave:** Shields icon > lower trackers/ads to "allow", or turn Shields down for this site only.
- **DNS filter:** allowlist the specific domain, not the whole blocklist.

## Report it
uBlock filter issues: the popup's "Report a filter issue" link opens a prefilled uBlockOrigin/uAssets issue.
EasyList and Firefox (webcompat.com) take reports too, so the fix reaches everyone.

## Gotchas
- Payment and login flows often need a third-party domain (e.g. a 3-D Secure bank frame); allow it only on the
  checkout site.
- Fingerprinting resistance (Firefox `privacy.resistFingerprinting`) breaks time zones and canvas-based sites; that
  is a setting problem, not a filter problem.
