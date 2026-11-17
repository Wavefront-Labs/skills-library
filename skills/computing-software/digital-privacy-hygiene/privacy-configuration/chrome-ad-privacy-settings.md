---
id: computing-software.digital-privacy-hygiene.privacy-configuration.chrome-ad-privacy-settings
name: chrome-ad-privacy-settings
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, chrome-ad-privacy, ad-tracking-controls, privacy-sandbox, ad-topics, site-suggested-ads, ad-measurement, third-party-cookies, chrome-sync]
level: intro
status: draft
description: "Turn off Chrome's Ad privacy features (ad topics, site-suggested ads, ad measurement), block third-party cookies, and review sync and Safe Browsing choices."
sources:
  - "https://support.google.com/chrome/answer/13355898"
  - "https://support.google.com/chrome/answer/95647"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chrome ad privacy settings

**Goal:** if you stay on Chrome, at least stop the browser itself profiling you for ads.

## Settings > Privacy and security
1. **Ad privacy** (the Privacy Sandbox controls):
   - Ad topics: **off** (Chrome infers interests from browsing).
   - Site-suggested ads: **off**.
   - Ad measurement: **off**.
   Google has changed and wound down parts of Privacy Sandbox; turn off whatever is listed.
2. **Third-party cookies**: **Block third-party cookies** (explicitly; Chrome kept them by
   default after abandoning its deprecation plan).
3. **Send a "Do Not Track" request**: low value; GPC isn't native in Chrome, use an
   extension or a different browser if you want GPC.
4. **Security** > Safe Browsing: Standard is a reasonable default; Enhanced sends more
   browsing data to Google in exchange for better phishing protection (a trade-off).
5. **Preload pages**: off if you want fewer speculative requests.

## Google account side
- Sync: decide what syncs (history feeds Web & App Activity if enabled).
- myadcenter.google.com: Personalised ads off.

## Better
For stronger protection, switch to Firefox or Brave (see the browser hardening skills);
Chrome has no strong built-in tracker blocking and limited uBlock support under MV3.

## Verify
- [ ] Ad privacy page shows all toggles off; third-party cookies blocked.
