---
id: computing-software.digital-privacy-hygiene.vpn-tools.cookie-clearing-and-consent-banner-handling
name: cookie-clearing-and-consent-banner-handling
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, cookie-management, cookie-consent-banners, third-party-cookies, total-cookie-protection, delete-on-close, consent-o-matic, reject-all, gdpr, tracker-blocking]
level: intro
status: draft
description: "Set a cookie policy (block third-party, clear on close with exceptions) and deal with consent banners quickly: reject-all habits, auto-reject tools and cosmetic hiding."
sources:
  - "https://support.mozilla.org/en-US/kb/introducing-total-cookie-protection-standard-mode"
  - "https://consentomatic.au.dk/"
  - "https://github.com/gorhill/uBlock/wiki/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cookie management and consent banners

**Goal:** fewer persistent identifiers, and less time spent clicking banners.

## Cookie policy
1. **Block or partition third-party cookies**: Firefox Total Cookie Protection (default
   in Standard/Strict), Safari ITP (default), Brave "block cross-site", Chrome:
   Settings > Privacy > Third-party cookies > Block (Chrome's own defaults have shifted;
   set it explicitly).
2. **Clear on close** with an allowlist of sites you stay logged into:
   - Firefox: Settings > Cookies and Site Data > Delete when Firefox is closed > Manage
     Exceptions > Allow (for your bank, email).
   - Chrome/Edge: Settings > Site settings > Third-party cookies / "Sites that can always
     use cookies" + "Clear cookies and site data when you close all windows".
3. Use separate **profiles/containers** for logged-in identities instead of keeping all
   cookies forever.

## Consent banners
- Habit: **Reject all** / "Only necessary"; under GDPR, rejecting must be as easy as
  accepting, though many sites still use dark patterns ("Manage options" > untick
  "legitimate interest" toggles too).
- Automate: **Consent-O-Matic** extension (Aarhus University) auto-fills your choices on
  common consent platforms; Firefox has a built-in cookie banner reduction in some
  regions; Brave/uBlock "Annoyances" lists hide banners.
- Hiding a banner ≠ rejecting: hidden banners may leave the site's default (sometimes
  tracking). Prefer auto-reject tools over cosmetic hiding when tracking matters.

## Gotchas
- Clearing cookies logs you out and resets "remember this device" 2FA prompts; whitelist
  the accounts where that's annoying.
- GPC signal (Global Privacy Control) is legally binding opt-out in some US states; turn
  it on alongside.

## Verify
- [ ] After browser restart, a non-allowlisted site has no stored cookies (DevTools > Storage).
