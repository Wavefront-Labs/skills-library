---
id: computing-software.digital-privacy-hygiene.vpn-tools.hardening-chrome-settings
name: hardening-chrome-settings
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, chrome-privacy-settings, browser-hardening, chrome-ad-privacy]
level: practitioner
status: draft
description: "Tighten Chrome's privacy and security settings beyond ad privacy: sync, Safe Browsing mode, preloading, search suggestions, site permissions and secure DNS."
sources:
  - "https://support.google.com/chrome/answer/114836"
  - "https://support.google.com/chrome/answer/9890866"
  - "https://www.privacyguides.org/en/desktop-browsers/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hardening Chrome settings

**Goal:** if you must use Chrome (work, compatibility), reduce what it sends to Google and sites.

## Settings > You and Google
- Sync: choose what syncs; consider a sync **passphrase** (end-to-end encrypts synced data except payment methods
  from Google Pay).
- Sync and Google services > **Improve search suggestions** off; **Make searches and browsing better** off;
  **Help improve Chrome** off.

## Privacy and security
| Setting | Recommend |
|---|---|
| Third-party cookies | Block (see ad privacy skill for Topics etc.) |
| Safe Browsing | Standard (Enhanced sends more URLs/downloads to Google; choose it if phishing risk outweighs) |
| Use secure DNS | On, choose a provider |
| Preload pages | Off (prefetch contacts sites you didn't visit) |
| Site settings > Notifications | Don't allow sites to send notifications (or "Use quieter messaging") |
| Site settings > Location, Camera, Mic | Ask; review allowed list |
| Always use secure connections | On (HTTPS-First) |

## Autofill and passwords
If you use a separate password manager, turn off "Offer to save passwords" and address/payment autofill.

## Search engine
Settings > Search engine: set DuckDuckGo/Startpage/Brave Search.

## Verify
`chrome://settings/privacy` review; Privacy Guide (Settings > Privacy and security > Privacy Guide) walks through
key items.

## Gotchas
- Signing in to a Google site can sign Chrome in; turn off "Allow Chrome sign-in" if you don't want that.
- Managed/work Chrome may lock settings via policy (`chrome://policy`).
