---
id: computing-software.digital-privacy-hygiene.vpn-tools.configuring-brave-shields
name: configuring-brave-shields
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, brave-shields, brave, privacy-browser, browser-hardening, fingerprinting-protection, content-filtering, brave-rewards, telemetry, chromium]
level: intro
status: draft
description: "Configure Brave for privacy: Shields aggressive blocking, fingerprinting protection, disabling Rewards/Wallet/Leo/news extras, telemetry off, and per-site exceptions."
sources:
  - "https://www.privacyguides.org/en/desktop-browsers/#brave"
  - "https://github.com/brave/brave-browser/wiki/"
  - "https://brave.com/shields/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuring Brave Shields

**Goal:** a Chromium browser (site compatibility) with strong built-in blocking, minus
the add-ons that aren't about privacy.

## Shields defaults (`brave://settings/shields`)
- Trackers & ads blocking: **Aggressive** (Standard allows first-party ads).
- Upgrade connections to HTTPS: **Strict**.
- Block scripts: off by default (breaks too much); use per site.
- Block fingerprinting: **Standard** (Brave randomises/"farbles" values per site and
  session). Strict breaks more.
- Block cookies: **Block cross-site cookies**.
- Forget me when I close this site: per site, for sites you never want to remember you.

## Content filtering (`brave://settings/shields/filters`)
Enable relevant regional lists and "Fanboy's Annoyances" or cookie-notice lists if you
want banners hidden.

## Turn off extras (Privacy Guides recommendations)
- `brave://settings/privacy`: disable "Allow privacy-preserving product analytics (P3A)",
  "Automatically send daily usage ping", "Automatically send diagnostic reports".
- WebRTC IP handling policy: "Disable non-proxied UDP".
- Hide/disable Brave Rewards, Brave Wallet (if unused), Brave News, Leo AI, VPN
  upsell, Brave Talk (`brave://settings/appearance` and each feature's page).
- Search: Brave Search or another private engine.
- Sync: Brave Sync uses a sync chain code; it's end-to-end encrypted.

## Per-site
Click the lion icon > adjust for a broken site (allow cookies or scripts temporarily);
prefer per-site exceptions over lowering global settings.

## Verify
- [ ] Lion icon shows a count of blocked items on a news site.
- [ ] `brave://settings/privacy` analytics toggles all off.
